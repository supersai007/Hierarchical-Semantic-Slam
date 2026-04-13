# Hierarchical-Semantic-Slam

uhumans2_office dataset: [https://drive.google.com/file/d/1Aqai_bhiL5viFu_wEMqURN2hPSW5-MkD/view?usp=sharing ](https://drive.google.com/file/d/1S4SiKUMylpYF9KxNLKE9AcwWhtFi2Zp6/view?usp=sharing)

lab dataset: https://drive.google.com/file/d/1tzW6thTRXQ0bI0ww_szm42AGpsbLk6Ay/view?usp=sharing 

Running hydra

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
