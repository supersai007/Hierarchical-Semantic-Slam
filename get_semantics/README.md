# Integrating lab_walk dataset into Hydra

I have already created the odometry topic, so only semantics is pending now. I am using oneformer model pretrained on ade20k dataset. On CPU it might take 6-8 hrs to get the semantics, so I am doing this on NVWulf cluster.

## Step1: Send lab_walk_final bag folder to the cluster env.

scp -r "lab_walk_final" <netid>@login.nvwulf.stonybrook.edu:/lustre/nvwulf/home/<netid>/semantics/dataset/lab_walk/

## Step2: Create new env to install ros2-humble to run "run_semantics_on_labwalk.sh"

To run the script (integrate_labwalk_to_hydra\pretrained\pre_trained_oneformer_on_labwalk.py), we need ROS. So I am creating new venv in the cluster to install ros-humble-desktop (ros2 jazzy not available in cluster)

```
module load miniconda/3

# Ensure channels are correct and in order
conda config --add channels conda-forge
conda config --add channels robostack-humble
conda config --set channel_priority strict

# Create the environment without forcing a Python version
conda create --prefix /lustre/nvwulf/home/<netid>/envs/ros2_humble_env ros-humble-desktop -y

conda activate /lustre/nvwulf/home/<netid>/envs/ros2_humble_env

pip install transformers torch torchvision pandas pillow

python -c "import rclpy; print('ROS 2 is ready!')"
```

## Step3: Create pre_trained_oneformer_on_labwalk.py and run_semantics_on_labwalk.sh and run the job in the env

Create the slurm job to run the segmentation in the GPU.
```
cd ~/semantics

# run job
sbatch run_semantics.slurm

### check job status
squeue -u <netid>
```
## Step5: Once job is done verify all topics in new bag and move created bag file back to wsl from cluster

### bag info should include /semantic/ topic. Check if the message counts matches with /D435/color/image_raw

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

### command to send folder back to local
scp -r <netid>@login.nvwulf.stonybrook.edu:/lustre/nvwulf/home/<netid>/semantics/dataset/lab_walk_seg/ bags/lab_walk_completed

## Step5: Create new config file

location: /home/vsman/hydra_ws/src/hydra_ros/hydra_ros/config/my_dataset_config.yaml

reference: integrate_labwalk_to_hydra\my_dataset_config.yaml

## Step6: Create new launch file

location: /home/vsman/hydra_ws/src/hydra_ros/hydra_ros/launch/datasets/my_dataset.launch.yaml

reference: integrate_labwalk_to_hydra\my_dataset.launch.yaml
