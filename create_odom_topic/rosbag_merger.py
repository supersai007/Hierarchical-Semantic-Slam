python3 - <<'EOF'
from rosbags.rosbag2 import Reader, Writer
from rosbags.typesys import Stores, get_typestore
import pathlib

src1 = pathlib.Path('/home/vsman/lab_walk')        # original dataset
src2 = pathlib.Path('/home/vsman/lab_walk_odom2')  # new dataset with /odom and /tf topics
dst  = pathlib.Path('/home/vsman/lab_walk_final')  # final dataset

typestore = get_typestore(Stores.ROS2_HUMBLE)

# Topics from odom bag that should OVERRIDE the original bag's versions
ODOM_TOPICS = {'/tf', '/tf_static', '/kiss/odometry'}

with Writer(dst, version=8) as writer:
    conn_map = {}
    for src in [src1, src2]:
        with Reader(src) as reader:
            for conn in reader.connections:
                # For topics that exist in both bags, odom bag wins
                # Skip /tf and /tf_static from src1 if odom bag has them
                if conn.topic in ODOM_TOPICS and src == pathlib.Path('/home/vsman/lab_walk'):
                    continue
                if conn.topic not in conn_map:
                    conn_map[conn.topic] = writer.add_connection(
                        conn.topic, conn.msgtype, typestore=typestore)

    for src in [src1, src2]:
        with Reader(src) as reader:
            for conn, timestamp, data in reader.messages():
                # Skip original bag's TF — use odom bag's TF instead to avoid timestamp conflicts
                if conn.topic in ODOM_TOPICS and src == pathlib.Path('/home/vsman/lab_walk'):
                    continue
                if conn.topic in conn_map:
                    writer.write(conn_map[conn.topic], timestamp, data)

print("Done — merged bag at", dst)
EOF
