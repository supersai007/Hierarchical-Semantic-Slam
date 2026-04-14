 The datasetneeds a source of odometry — something populating the pose of the camera for every image timestamp via TF. 
 (https://github.com/MIT-SPARK/Hydra-ROS/)
 The lab dataset has no /tesse/odom equivalent. We need a LiDAR odometry node (FAST-LIO2 is the standard choice for Livox) running separately to publish odom → base_link in TF before Hydra will work.
