**Note: In remote_segmentation_node.py, change subscription topic to a topic from the dataset which is being played.**

<h1>Steps to run segmentation on colab </h1>

1. Run wsl-colab.ipynb
2. Terminal 1: Once server starts, play rosbag 
3. Terminal 2:
```
source ~/hydra_ws/install/setup.bash
ros2 launch semantic_inference_ros remote_segmentation.launch.yaml **(for both office/lab dataset)**
(or)
ros2 launch hydra_ros uhumans2_remote.launch.yaml use_gt_semantics:=false **(only for office)**
```
<h1>New files to add in hydra_ws:</h1>

```
/hydra_ws/src/semantic_inference/semantic_inference_ros/launch/remote_segmentation.launch.yaml
/hydra_ws/src/hydra_ros/launch/datasets/uhumans2_remote.launch.yaml (for gt_semantic:=false)
semantic_inference/semantic_inference_ros/semantic_inference_ros/remote_segmentation_node.py
```
<h1>Observations:</h1>
1. Newly published topics include: <br>/tesse/left_cam/semantic/image_raw <br>/tesse/left_cam/semantic/mask<br>
2. The server segmentation output is in black and white even though the input image is colored.<br>
3. While running <br>
<b>ros2 launch hydra_ros uhumans2_remote.launch.yaml use_gt_semantics:=false</b>
The 3D mesh is incomplete and also in black and white.
<img width="1907" height="669" alt="image" src="https://github.com/user-attachments/assets/5b91b453-1b00-4746-af58-ded85c53ffd9" />


Sample input and server segmentation output:

| Image | Reality |
| --- | --- |
| ![](https://github.com/user-attachments/assets/1e4c7295-bc88-4c6e-876e-17cbccc6abcf) | ![](https://github.com/user-attachments/assets/0b841e28-f4e1-4aa4-9b05-22001555b08d) |

<img width="720" height="480" alt="image" src="https://github.com/user-attachments/assets/1e4c7295-bc88-4c6e-876e-17cbccc6abcf" />

<img width="720" height="480" alt="reality" src="https://github.com/user-attachments/assets/0b841e28-f4e1-4aa4-9b05-22001555b08d" />

**Note that these are the colored, resized version of the output mask, the original output is very small and in black and white.**
