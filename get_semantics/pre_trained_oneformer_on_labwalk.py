import rclpy
from rclpy.serialization import deserialize_message, serialize_message
from rosidl_runtime_py.utilities import get_message
import rosbag2_py
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import torch
import numpy as np
from transformers import OneFormerProcessor, OneFormerForUniversalSegmentation

# === MODEL ===
processor = OneFormerProcessor.from_pretrained("shi-labs/oneformer_ade20k_swin_large")
model = OneFormerForUniversalSegmentation.from_pretrained("shi-labs/oneformer_ade20k_swin_large")
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
model.eval()

bridge = CvBridge()

input_bag = "/lustre/nvwulf/home/admanoharan/semantics/dataset/lab_walk/lab_walk_final"
output_bag = "/lustre/nvwulf/home/admanoharan/semantics/dataset/lab_walk_semantics"    # new output — don't overwrite old one
input_topic = "/D435/color/image_raw"
output_topic = "/D435/semantic/image_raw"   # renamed to semantic, not rgb

# === READER ===
reader = rosbag2_py.SequentialReader()
reader.open(
    rosbag2_py.StorageOptions(uri=input_bag, storage_id="sqlite3"),
    rosbag2_py.ConverterOptions("", "")
)

# === WRITER ===
writer = rosbag2_py.SequentialWriter()
writer.open(
    rosbag2_py.StorageOptions(uri=output_bag, storage_id="sqlite3"),
    rosbag2_py.ConverterOptions("", "")
)

topic_types = reader.get_all_topics_and_types()
for topic in topic_types:
    writer.create_topic(topic)

writer.create_topic(
    rosbag2_py.TopicMetadata(
        name=output_topic,
        type="sensor_msgs/msg/Image",
        serialization_format="cdr",
        offered_qos_profiles=""
    )
)

type_map = {t.name: t.type for t in topic_types}

# === PROCESS LOOP ===
count = 0
while reader.has_next():
    topic, data, t = reader.read_next()
    writer.write(topic, data, t)

    if topic != input_topic:
        continue

    # Deserialize image
    msg_type = get_message(type_map[topic])
    img_msg = deserialize_message(data, msg_type)

    # ROS → numpy RGB
    cv_image = bridge.imgmsg_to_cv2(img_msg, desired_encoding='bgr8')
    image_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

    # === Inference ===
    inputs = processor(
        images=image_rgb,
        task_inputs=["semantic"],
        return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)

    segmentation = processor.post_process_semantic_segmentation(
        outputs,
        target_sizes=[image_rgb.shape[:2]]
    )[0]

    # ── Key fix: save raw integer labels, NOT colorized image ──────────────
    label_map = segmentation.cpu().numpy().astype(np.uint8)
    # label_map is shape (H, W), values 0–149 (ADE20K class IDs)
    # DO NOT colorize — Hydra needs the raw integer IDs

    # Convert single-channel label map to ROS Image with mono8 encoding
    seg_msg = bridge.cv2_to_imgmsg(label_map, encoding="mono8")
    seg_msg.header = img_msg.header   # preserve original timestamp and frame_id

    serialized = serialize_message(seg_msg)
    writer.write(output_topic, serialized, t)

    count += 1
    if count % 50 == 0:
        print(f"Processed {count} frames...")

print(f"Done! Processed {count} semantic frames. New bag at {output_bag}")