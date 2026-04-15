Semantic Segmentation of images from the rosbag

<h1>Script1: Convert rosbag to folders containing images</h1>

1. One folder for each topic
2. Each folder contains a metedata.csv to store metadata for reconstruction
3. Each image in the folder named after timestamp.

Folder structure looks like:

<img width="1030" height="427" alt="topic_folder" src="https://github.com/user-attachments/assets/24705d36-d49f-4522-ac18-cf2284f1048e" />

metdata.csv looks like:

<img width="655" height="433" alt="metadata_csv" src="https://github.com/user-attachments/assets/8465c0a3-db30-4911-b938-dc98fa48c1ee" />


<h1>Script2: Convert the folders back to bag file</h1>
