#!/bin/bash
#SBATCH --partition=h200x8
#SBATCH --gpus=1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --mem=64G
#SBATCH --time=08:00:00
#SBATCH --output=/lustre/nvwulf/home/admanoharan/semantics/logs/panst3r/run_panst3r_%j.txt

module load slurm

# 1. Block the ~/.local python3.13 directory from interfering
export PYTHONNOUSERSITE=1

echo "=========================================================="
echo " Running on node: $SLURM_NODENAME"
echo "=========================================================="

# 2. Run using the exact hidden .conda environment path
/lustre/nvwulf/home/admanoharan/.conda/envs/must3r_env/bin/python /lustre/nvwulf/home/admanoharan/semantics/models/panst3r/gradio_panst3r.py \
    --weights /lustre/nvwulf/home/admanoharan/semantics/models/panst3r/panst3r_v1_512_5ds.pth \
    --server_name 0.0.0.0