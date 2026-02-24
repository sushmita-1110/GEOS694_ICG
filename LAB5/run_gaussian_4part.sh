#!/bin/bash

python 2d_gaussian_embarassing.py -2 -1 &
python 2d_gaussian_embarassing.py -1 0 &
python 2d_gaussian_embarassing.py 0 1 &
python 2d_gaussian_embarassing.py 1 2 &

wait
echo "All chunks completed."
