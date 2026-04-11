## to be saved as /hydra_ws/src/semantic_inference/semantic_inference_ros/semantic_inference_ros/remote_segmentation_node (no .py)
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
import cv2
import numpy as np
import requests

from cv_bridge import CvBridge


class RemoteSegmentationNode(Node):

    def __init__(self):
        super().__init__("remote_segmentation")

        self.bridge = CvBridge()

        # Replace with your Colab/ngrok URL later
        self.server_url = "https://substratospheric-neurophysiologically-loreen.ngrok-free.dev/segment"

        self.subscription = self.create_subscription(
            Image,
            "/tesse/left_cam/rgb/image_raw",  # change to --> /D435/color/image_raw while playing lab dataset
            self.image_callback,
            10
        )

        self.mask_publisher = self.create_publisher(
            Image,
            "semantic/mask",
            10
        )
        self.image_publisher = self.create_publisher(
            Image,
            "semantic/image_raw",
            10
        )

        self.get_logger().info("Remote segmentation node started")

    def image_callback(self, msg):

        try:
            image = self.bridge.imgmsg_to_cv2(msg, "rgb8")
        except Exception as e:
            self.get_logger().error(f"Conversion error: {e}")
            return

        try:
            mask = self.send_to_server(image)

            mask = mask.astype(np.uint8)

            mask_msg = self.bridge.cv2_to_imgmsg(mask, encoding="mono8")
            mask_msg.header = msg.header

            self.mask_publisher.publish(mask_msg)
            self.image_publisher.publish(mask_msg)

        except Exception as e:
            self.get_logger().error(f"Inference error: {e}")


    def send_to_server(self, image):

        _, buffer = cv2.imencode(".jpg", image)

        files = {
            "image": ("image.jpg", buffer.tobytes(), "image/jpeg")
        }

        response = requests.post(
            self.server_url,
            files=files,
            timeout=30
        )

        if response.status_code != 200:
            raise RuntimeError("Server returned error")

        nparr = np.frombuffer(response.content, np.uint8)
        mask = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

        return mask


def main(args=None):
    rclpy.init(args=args)
    node = RemoteSegmentationNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
