## Training data:

drive link = [uHumans training data](https://drive.google.com/drive/folders/1xH0rSPIK35E8zABI7M5Jygcyna0UKWn4?usp=sharing)

rgb_dir=f"{drive_path}/tesse_left_cam_rgb_image_raw"
seg_dir=f"{drive_path}/tesse_seg_cam_converted_image_raw"

## Download dataset as zip files and send it to cluster env:

scp *.zip <netid>@login.nvwulf.stonybrook.edu:/lustre/nvwulf/home/<netid>/semantics/dataset/uhumans/

## Send bag file to cluster env:

scp -r "lab_walk" <netid>@login.nvwulf.stonybrook.edu:/lustre/nvwulf/home/<netid>/semantics/dataset/lab_walk/

#### create train_job.slurm script to run training script as job

## commands to run training on cluster:

create job
```
sbatch train_job.slurm
```
check status
```
squeue -u <netid>
```

once job is done, check logs at ~/semantics/logs/oneformer_train_<jobid>.txt

## Once training done, send model weights back to local

scp -r <netid>@login.nvwulf.stonybrook.edu:/lustre/nvwulf/home/<netid>/semantics/models/oneformer_ade20k_swin_large/trained_on_uhumans/oneformer_uhumans2_best hydra_ws/model/

# Verifying results

Log loss curve:

<img width="1005" height="547" alt="image" src="https://github.com/user-attachments/assets/1421bc91-908b-43a0-8467-f7985aa5baad" />

Before training:

<img width="1570" height="345" alt="image" src="https://github.com/user-attachments/assets/86cee422-c6f4-4460-95db-5483d5aee8bc" />

After training:

<img width="1569" height="510" alt="image" src="https://github.com/user-attachments/assets/28d3d9c1-a83d-4016-8479-e6d93c1fc75a" />

trained model weights = https://drive.google.com/drive/folders/1zigDFjj9zQt5LS9SSOl8BiHbAy7I8K8Q?usp=sharing
