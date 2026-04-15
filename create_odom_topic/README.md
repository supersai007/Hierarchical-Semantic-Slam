<h1> Need for a odometry topic</h1>
 
 The dataset needs a source of odometry — something populating the pose of the camera for every image timestamp via TF. (https://github.com/MIT-SPARK/Hydra-ROS/)
 
 The lab dataset has no /tesse/odom equivalent. We need a LiDAR odometry node running separately to publish odom → base_link in TF before Hydra will work.

<h1> Issues with the original dataset: </h1>

<h2> 1. Timestamp Issue </h2>

 Original dataset bag_pcd_topics.bag (https://drive.google.com/file/d/1tzW6thTRXQ0bI0ww_szm42AGpsbLk6Ay/view?usp=sharing) cannot be played as it is because ros 2 expects the bag file to be a folder which contains metadata.yaml and a .db3 or .mcap file. Hence I converted the bagfile to the required format using:

 ```
rosbags-convert --src path/to/office.bag --dst path/to/office
```

| lab_walk | lab_walk_odom |
| --- | --- |
| <img width="512" height="210" alt="lab_Walk" src="https://github.com/user-attachments/assets/5fc8aa97-9847-48c7-9a5a-309ad81a03e1" />| <img width="512" height="311" alt="lab_walk_odom" src="https://github.com/user-attachments/assets/6b3bcc2e-60e0-4051-ba9e-564373768438" /> |

The converted dataset lab_walk starts in 1970 → why ??

I created a new dataset with an odometry topic(/kiss/odometry) by subscribing to /livox/lidar. The new dataset lab_walk_odom starts in 2026. So while merging these two bags, there is a mismatch in the timestamps.

<h2> 2. Format issue </h2>

lab_walk_odom → .mcap format but lab_walk → .db3 format

<h1> Fix: </h1>

Terminal 1:

```
ros2 bag play ~/lab_walk --clock --qos-profile-overrides-path ~/.tf_overrides.yaml
```

Terminal 2: 

(Packages like FAST-LIO can also be used to publish odom topic, but kiss-icp (https://github.com/prbonn/kiss-icp) is easy to install and run)

```
ros2 launch kiss_icp odometry.launch.py \
  topic:=/livox/lidar \
  use_sim_time:=true
```

Terminal 3:

Record ONLY the odometry/TF output

```
ros2 bag record \
  /kiss/odometry \
  /tf \
  /tf_static \
  --use-sim-time \
  -o ~/lab_walk_odom2
```

<h1>Results:</h1>

<img width="512" height="299" alt="lab_walk_odom2" src="https://github.com/user-attachments/assets/9c2d0e38-c5c9-4f20-a292-dcac4d680792" />


Then merge datasets using rosbag_merger.py.


<img width="512" height="379" alt="lab_walk_final" src="https://github.com/user-attachments/assets/76990d2c-14e4-4dfd-8666-86bd3c6eb442" />


