# Hierarchical Semantic SLAM using Hydra on Custom Lab Dataset

## Overview
This repository contains my work on integrating a custom RGB-D + LiDAR lab dataset into the [MIT-SPARK Hydra-ROS framework](https://github.com/MIT-SPARK/Hydra-ROS?utm_source=chatgpt.com) for hierarchical semantic SLAM and semantic 3D reconstruction.

The project involved:

1. Understanding Hydra’s internal architecture and dataset requirements
2. Generating odometry from LiDAR using KISS-ICP
3. Integrating semantic segmentation pipelines
4. Reconstructing TF trees for ROS2 compatibility
5. Running Hydra on a completely custom dataset instead of the default uHumans2 dataset
6. Training and evaluating semantic segmentation models

Directory:
1. Notebooks: Notebook files used to explore different segmentation models
2. colab_setup_files: files required to run segmentation on colab
3. conv_bag_to_folders: script to convert bag file to image folders (one folder per topic)
4. create_odom_topic: files required to create odomtery topic to bag file
5. get_semantics: files required to create semantic topic from color image topic and merge with existing bag
6. sem1_final_setup: contains final versions of launch and config files for semester 1
7. training_on_uhumans: files required to train one_former model on uhumans dataset (refer to access_to_AI_cluster.txt for NvWulf cluster access)

## System Architecture
Sensor Setup
RGB-D Cameras
Intel RealSense D435
Intel RealSense D455
LiDAR
Livox LiDAR
Odometry

Generated using:

[KISS-ICP](https://github.com/prbonn/kiss-icp)
[Steps to create odom](https://github.com/supersai007/Hierarchical-Semantic-Slam/tree/main/create_odom_topic)

## ROS Topics Used

#### RGB / Depth
```sh
/D435/color/image_raw
/D435/color/camera_info
/D435/aligned_depth_to_color/image_raw
/D435/aligned_depth_to_color/camera_info
```
#### Semantic Segmentation
```sh
/D435/semantic/image_raw
```
#### LiDAR + Odometry
```sh
/livox/lidar
/kiss/odometry
```
#### TF
```sh
/tf
/tf_static
```

## Final TF Structure
```
odom_lidar
   └── livox_frame
           └── D435_color_optical_frame
```
Hydra configuration:
1. odom_frame = odom_lidar
2. robot_frame = livox_frame
3. sensor_frame = D435_color_optical_frame

## Hydra Integration

#### Custom Launch File
```sh
hydra_ros/launch/datasets/my_dataset.launch.yaml
```
Features:
1. Topic remapping
2. TF publishing
3. Odometry integration
4. Semantic topic integration
5. Hydra visualizer support

#### Custom Dataset Config
```sh
hydra_ros/config/my_dataset_config.yaml
```
Features:
1. Live camera intrinsic reading from camera_info
2. Extrinsics read dynamically from TF
3. TSDF + semantic integration tuning
4. PGMO backend configuration

## Semantic Segmentation Work
#### Models Evaluated
1. EfficientViT
Hydra default segmentation model. Tried to implement the model by setting colab as server.(https://github.com/supersai007/Hierarchical-Semantic-Slam/tree/main/colab_setup_files)
2. OneFormer (shi-labs/oneformer_ade20k_swin_large)
3. SegFormer (nvidia/segformer-b5-finetuned-ade-640-640)
4. Mask2Former (facebook/mask2former-swin-large-ade-semantic)

#### OneFormer Training
Training pipeline on uHumans GT labels
Fine-tuning pipeline for scene parsing datasets

## Dataset info

uhumans2_office dataset: [https://drive.google.com/file/d/1Aqai_bhiL5viFu_wEMqURN2hPSW5-MkD/view?usp=sharing ](https://drive.google.com/file/d/1S4SiKUMylpYF9KxNLKE9AcwWhtFi2Zp6/view?usp=sharing)

original lab dataset: [https://drive.google.com/file/d/1tzW6thTRXQ0bI0ww_szm42AGpsbLk6Ay/view?usp=sharing ](https://drive.google.com/drive/folders/1DKlsfPSnPgcTCvmx3LkXUU9TNChw3TUD)

```
Files:             lab_walk_7526.db3
Bag size:          11.3 GiB
Storage id:        sqlite3
ROS Distro:        rosbags
Duration:          111.075027584s
Start:             Feb 17 1970 22:02:52.393971168 (4158172.393971168)
End:               Feb 17 1970 22:04:43.468998752 (4158283.468998752)
Messages:          68298
Topic information: Topic: /D435/accel/sample | Type: sensor_msgs/msg/Imu | Count: 10948 | Serialization Format: cdr
                   Topic: /D435/aligned_depth_to_color/camera_info | Type: sensor_msgs/msg/CameraInfo | Count: 608 | Serialization Format: cdr
                   Topic: /D435/aligned_depth_to_color/image_raw | Type: sensor_msgs/msg/Image | Count: 608 | Serialization Format: cdr
                   Topic: /D435/color/camera_info | Type: sensor_msgs/msg/CameraInfo | Count: 3030 | Serialization Format: cdr
                   Topic: /D435/color/image_raw | Type: sensor_msgs/msg/Image | Count: 3030 | Serialization Format: cdr
                   Topic: /D435/gyro/sample | Type: sensor_msgs/msg/Imu | Count: 21743 | Serialization Format: cdr
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

lab dataset with d435 semantics: https://drive.google.com/drive/folders/1cVhyTfSwNS9K3XPlIv7vX096oGBpYikr?usp=sharing
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
lab dataset with d455 semantics: https://drive.google.com/drive/folders/1HzE-JjuQW9Z4knpmpmrOJ0x-1N_37d2m?usp=drive_link
```
Files:             lab_walk_7526_wsemantics_0.db3
Bag size:          11.7 GiB
Storage id:        sqlite3
ROS Distro:        unknown
Duration:          111.075027584s
Start:             Feb 17 1970 22:02:52.393971168 (4158172.393971168)
End:               Feb 17 1970 22:04:43.468998752 (4158283.468998752)
Messages:          69829
Topic information: Topic: /D435/accel/sample | Type: sensor_msgs/msg/Imu | Count: 10948 | Serialization Format: cdr
                   Topic: /D435/aligned_depth_to_color/camera_info | Type: sensor_msgs/msg/CameraInfo | Count: 608 | Serialization Format: cdr
                   Topic: /D435/aligned_depth_to_color/image_raw | Type: sensor_msgs/msg/Image | Count: 608 | Serialization Format: cdr
                   Topic: /D435/color/camera_info | Type: sensor_msgs/msg/CameraInfo | Count: 3030 | Serialization Format: cdr
                   Topic: /D435/color/image_raw | Type: sensor_msgs/msg/Image | Count: 3030 | Serialization Format: cdr
                   Topic: /D435/gyro/sample | Type: sensor_msgs/msg/Imu | Count: 21743 | Serialization Format: cdr
                   Topic: /D455/aligned_depth_to_color/camera_info | Type: sensor_msgs/msg/CameraInfo | Count: 975 | Serialization Format: cdr
                   Topic: /D455/aligned_depth_to_color/image_raw | Type: sensor_msgs/msg/Image | Count: 975 | Serialization Format: cdr
                   Topic: /D455/color/camera_info | Type: sensor_msgs/msg/CameraInfo | Count: 1522 | Serialization Format: cdr
                   Topic: /D455/color/image_raw | Type: sensor_msgs/msg/Image | Count: 1531 | Serialization Format: cdr
                   Topic: /D455/semantic/image_raw | Type: sensor_msgs/msg/Image | Count: 1531 | Serialization Format: cdr
                   Topic: /livox/imu | Type: sensor_msgs/msg/Imu | Count: 22215 | Serialization Format: cdr
                   Topic: /livox/lidar | Type: sensor_msgs/msg/PointCloud2 | Count: 1110 | Serialization Format: cdr
                   Topic: /tf_static | Type: tf2_msgs/msg/TFMessage | Count: 3 | Serialization Format: cdr
Service:           0
Service information:
```
## Running hydra

Terminal 1 — Launch Hydra
```
source ~/hydra_ws/install/setup.bash
ros2 launch hydra_ros uhumans2.launch.yaml
```
With semantics: 
```
ros2 launch hydra_ros uhumans2.launch.yaml use_gt_semantics:=true
```
Terminal 2 — Play the bag (with performance fix)
```
source ~/rosbags_env/bin/activate
source /opt/ros/jazzy/setup.bash
ros2 bag play ~/office_bag   --clock   --qos-profile-overrides-path ~/.tf_overrides.yaml   --read-ahead-queue-size 20000 -l
```

uHumans office dataset structure:

<img width="1072" height="571" alt="image" src="https://github.com/user-attachments/assets/5a1b2995-5750-48fe-95ca-8d9a491f6613" />

