# vsman@DESKTOP-TOTBAC3:~/hydra_ws/src/odom_to_tf/odom_to_tf$ cat odom_to_tf_node.py
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster


class OdomToTF(Node):
    def __init__(self):
        super().__init__('odom_to_tf_node')

        # Parameters
        self.declare_parameter('odom_topic', '/kiss/odometry')
        self.declare_parameter('odom_frame', 'odom_lidar')
        self.declare_parameter('base_frame', 'livox_frame')

        self.odom_topic = self.get_parameter('odom_topic').value
        self.odom_frame = self.get_parameter('odom_frame').value
        self.base_frame = self.get_parameter('base_frame').value

        # TF broadcaster
        self.tf_broadcaster = TransformBroadcaster(self)

        # Subscriber
        self.sub = self.create_subscription(
            Odometry,
            self.odom_topic,
            self.odom_callback,
            10
        )

        self.get_logger().info(f"Listening to {self.odom_topic}")
        self.get_logger().info(f"Publishing TF: {self.odom_frame} -> {self.base_frame}")

    def odom_callback(self, msg: Odometry):
        t = TransformStamped()

        # Use timestamp from odometry
        t.header.stamp = msg.header.stamp
        t.header.frame_id = self.odom_frame
        t.child_frame_id = self.base_frame

        # դիր (position)
        t.transform.translation.x = msg.pose.pose.position.x
        t.transform.translation.y = msg.pose.pose.position.y
        t.transform.translation.z = msg.pose.pose.position.z

        # orientation (quaternion)
        t.transform.rotation = msg.pose.pose.orientation

        # Publish TF
        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = OdomToTF()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
