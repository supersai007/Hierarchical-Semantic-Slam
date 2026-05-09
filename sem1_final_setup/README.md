# Overview:

I am using the semantics from D435 cam only and avoided the D455 topics, to check if the integration pipeline works. 
The final TF map looks like:

<img width="1341" height="442" alt="Screenshot 2026-05-08 063413" src="https://github.com/user-attachments/assets/8ca4cf8d-b06b-4d72-a4b1-a47223286b1b" />

Final demo:

https://github.com/user-attachments/assets/671836cb-34ce-4677-bc63-1648b7926e77

# Step 1: Install Hydra

https://github.com/MIT-SPARK/Hydra-ROS#installation


# Step 2: odom_to_tf package setup


This is a a ROS2 node that converts /kiss/odometry → TF (odom → livox_frame) so Hydra can consume it.


1. Create package
```
cd ~/hydra_ws/src
ros2 pkg create odom_to_tf --build-type ament_python --dependencies rclpy nav_msgs tf2_ros geometry_msgs
```
2. Replace structure
```
odom_to_tf/
  odom_to_tf/
    __init__.py
    odom_to_tf_node.py 
```
3. Edit setup.py
```
entry_points={
    'console_scripts': [
        'odom_to_tf_node = odom_to_tf.odom_to_tf_node:main',
    ],
},
```
4. Build
```
cd ~/hydra_ws
colcon build --packages-select odom_to_tf
source install/setup.bash
```

# Step 2: create launch file for custom dataset:



# file locations:
```
hydra_ws/src/hydra_ros/hydra_ros/launch/datasets/my_dataset.launch.yaml

hydra_ws/src/hydra_ros/hydra_ros/config/my_dataset.config.yaml

hydra_ws/src/odom_to_tf/odom_to_tf/odom_to_tf.py
```
# dataset info
```
Files:             lab_walk_7526_wsemantics_0.db3
Bag size:          13.9 GiB
Storage id:        sqlite3
ROS Distro:        unknown
Duration:          111.075027584s
Start:             Feb 17 1970 22:02:52.393971168 (4158172.393971168)
End:               Feb 17 1970 22:04:43.468998752 (4158283.468998752)
Messages:          71328
Topic information: Topic: /D435/accel/sample | Type: sensor_msgs/msg/Imu | Count: 10948 | Serialization Format: cdr
                   Topic: /D435/aligned_depth_to_color/camera_info | Type: sensor_msgs/msg/CameraInfo | Count: 608 | Serialization Format: cdr
                   Topic: /D435/aligned_depth_to_color/image_raw | Type: sensor_msgs/msg/Image | Count: 608 | Serialization Format: cdr
                   Topic: /D435/color/camera_info | Type: sensor_msgs/msg/CameraInfo | Count: 3030 | Serialization Format: cdr
                   Topic: /D435/color/image_raw | Type: sensor_msgs/msg/Image | Count: 3030 | Serialization Format: cdr
                   Topic: /D435/gyro/sample | Type: sensor_msgs/msg/Imu | Count: 21743 | Serialization Format: cdr
                   Topic: /D435/semantic/image_raw | Type: sensor_msgs/msg/Image | Count: 3030 | Serialization Format: cdr
                   Topic: /D455/aligned_depth_to_color/camera_info | Type: sensor_msgs/msg/CameraInfo | Count: 975 | Serialization Format: cdr
                   Topic: /D455/aligned_depth_to_color/image_raw | Type: sensor_msgs/msg/Image | Count: 975 | Serialization Format: cdr
                   Topic: /D455/color/camera_info | Type: sensor_msgs/msg/CameraInfo | Count: 1522 | Serialization Format: cdr
                   Topic: /D455/color/image_raw | Type: sensor_msgs/msg/Image | Count: 1531 | Serialization Format: cdr
                   Topic: /livox/imu | Type: sensor_msgs/msg/Imu | Count: 22215 | Serialization Format: cdr
                   Topic: /livox/lidar | Type: sensor_msgs/msg/PointCloud2 | Count: 1110 | Serialization Format: cdr
                   Topic: /tf_static | Type: tf2_msgs/msg/TFMessage | Count: 3 | Serialization Format: cdr
Service:           0
Service information:
```
# Running Hydra

Terminal 1:
```
source ~/rosbags_env/bin/activate

source /opt/ros/jazzy/setup.bash

ros2 bag play ~/bags/lab_walk_7526_wsemantics  --clock   --qos-profile-overrides-path ~/.tf_overrides.yaml   --read-ahead-queue-size 20000 -l
```


Instead of merging odom topic to the bag, I run the kiss-icp parallely.
Wait until bag starts publishing values before running icp and Hydra file.


Terminal 2:
```
ros2 launch kiss_icp odometry.launch.py \
topic:=/livox/lidar \
base_frame:=livox_frame \
publish_odom_tf:=false \
use_sim_time:=true 
```

Terminal 3:
```
ros2 bag play ~/bags/lab_walk_7526_wsemantics  --clock   --qos-profile-overrides-path ~/.tf_overrides.yaml   --read-ahead-queue-size 20000 -l
```










