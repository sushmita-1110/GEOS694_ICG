#!/bin/bash
#SBATCH --job-name=ak_map
#SBATCH --partition=debug
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --time=00:10:00
#SBATCH --output=%j.out

source ~/miniforge3/etc/profile.d/conda.sh
conda activate GEOS694

python alaska_map.py --input gmap-stations-AK.txt --output AK_station_alaska_map.png
