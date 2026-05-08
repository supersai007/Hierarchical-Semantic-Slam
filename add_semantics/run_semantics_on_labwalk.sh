#!/bin/bash
#SBATCH --partition=b40x4
#SBATCH --gpus=1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --mem=64G
#SBATCH --time=08:00:00
#SBATCH --output=/lustre/nvwulf/home/admanoharan/semantics/logs/oneformer_train_%j.txt

# 1. CRITICAL: Clear all inherited Python paths to avoid 3.13 conflicts
unset PYTHONPATH
module load slurm
module load miniconda/3

# 2. Initialize and Activate your Lustre Environment
source $(conda info --base)/etc/profile.d/conda.sh
conda activate /lustre/nvwulf/home/admanoharan/envs/ros2_humble_env

# 3. Manual Fix for ROS 2 Paths (since ros_env_setup.sh is missing)
# This ensures 'import rclpy' finds the .so files in your 3.12 environment
export LD_LIBRARY_PATH=/lustre/nvwulf/home/admanoharan/envs/ros2_humble_env/lib:$LD_LIBRARY_PATH
export PYTHONPATH=/lustre/nvwulf/home/admanoharan/envs/ros2_humble_env/lib/python3.12/site-packages:$PYTHONPATH
export ROS_DISTRO=humble

# 4. GPU Memory Management Fixes
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

# 5. EXECUTE using the ABSOLUTE PATH to your Environment's Python
# This is the most important part to avoid the ModuleNotFoundError
/lustre/nvwulf/home/admanoharan/envs/ros2_humble_env/bin/python /lustre/nvwulf/home/admanoharan/semantics/pre_trained_oneformer_on_labwalk.py
