#!/bin/bash

python 2d_gaussian_embarassing.py -2 0 &
python 2d_gaussian_embarassing.py 0 2 &

wait
echo "All chunks completed."