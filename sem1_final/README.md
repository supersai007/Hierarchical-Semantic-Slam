Added semantics to images from d435 cam to the original dataset. 

dataset info:
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

Instead of merging odom topic to the bag, I run the kiss-icp parallely.

Final setup:

Terminal 1:
```
source ~/rosbags_env/bin/activate

source /opt/ros/jazzy/setup.bash

ros2 bag play ~/bags/lab_walk_7526_wsemantics  --clock   --qos-profile-overrides-path ~/.tf_overrides.yaml   --read-ahead-queue-size 20000 -l
```

Wait until /clock starts publishing values.

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










