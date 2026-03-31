#!/bin/bash
#SBATCH --job-name=is_prime
#SBATCH --partition=debug
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=00:05:00
#SBATCH --array=0-1
#SBATCH --output=%j_%a.out

source ~/miniforge3/etc/profile.d/conda.sh
conda activate GEOS694

python is_prime.py $SLURM_CPUS_PER_TASK
