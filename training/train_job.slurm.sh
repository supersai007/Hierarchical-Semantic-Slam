#!/bin/bash
#SBATCH --partition=b40x4          
#SBATCH --gpus=1                   
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12         
#SBATCH --mem=64G                  
#SBATCH --time=8:00:00             
#SBATCH --output=/lustre/nvwulf/home/admanoharan/semantics/logs/oneformer_train_%j.txt

# load module
module load slurm

# Run script
python /lustre/nvwulf/home/admanoharan/semantics/train_oneformer_on_uhumans.py
