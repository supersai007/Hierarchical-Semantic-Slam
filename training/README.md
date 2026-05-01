## Training data:

drive link = https://drive.google.com/drive/folders/1X1t48VxJQLnXUQHUv0Yo4SCUoMJmUhGu?usp=sharing 

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

