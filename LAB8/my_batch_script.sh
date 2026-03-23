#!/bin/bash
#SBATCH --partition=debug
#SBATCH --nodes=2
#SBATCH --ntasks=2
#SBATCH --job-name="hello world!"
#SBATCH --output=%j_%x.out
#SBATCH --time=00:00:05

srun echo "Hello"
srun hostname
srun echo "Nodes allocated: $SLURM_NODELIST"
srun echo "CPUs per node: $SLURM_CPUS_ON_NODE"
srun sleep 10
srun echo "World"
