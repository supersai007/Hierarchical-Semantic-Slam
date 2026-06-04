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

<img width="720" height="480" alt="378354899999" src="https://github.com/user-attachments/assets/3083ffbb-f577-45f3-8679-4c2a890a861d" />

<img width="1920" height="964" alt="Screenshot (225)" src="https://github.com/user-attachments/assets/e0161228-943f-47db-841e-75848b3e2ddd" />

<img width="1920" height="962" alt="Screenshot (224)" src="https://github.com/user-attachments/assets/3ae79c88-e440-4668-94a7-fbfe7fe111f2" />

<img width="1920" height="967" alt="Screenshot (223)" src="https://github.com/user-attachments/assets/723bed53-ddd4-464f-8fa4-b2785c2915ec" />

[demo video](https://drive.google.com/file/d/189l74v_TW1MaaD117U4Noknf0zcwIIlO/view?usp=sharing)



