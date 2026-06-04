# Exploring [panst3r](https://github.com/naver/panst3r) model for panoptic segmentation and 3D reconstruction

This model requires NVIDIA GPU, so I implemented this on [NVWulf cluster](https://rci.stonybrook.edu/HPC/faqs/getting-started-nvwulf). Attached the slurm job script and changes I made in demo_panst3r.py in the repo.

## Implementation steps:
1. Create conda env before installing the model
2. Follow the steps in [https://github.com/naver/panst3r/tree/main#installation](https://github.com/naver/panst3r/tree/main#installation) to install panst3r model.
3. Replace panst3r/tools/demo_panst3r.py with the script attached in the repo.
4. Run the slurm script.
5. Open a second ubuntu terminal, run the command and enter the password:
```
ssh -N -L 7860:h200x8-01:7860 -L 5000:h200x8-01:5000 admanoharan@login.nvwulf.stonybrook.edu
```

## Outputs

