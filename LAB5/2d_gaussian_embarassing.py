"""
2D Gaussian computation (serial version)

This script computes and plots a 2D Gaussian distribution
using nested loops (serial implementation).

Run this script multiple times with different X ranges
"""

import sys
import time
import numpy as np
import matplotlib.pyplot as plt

# Step size
STEP = .001

def gaussian2D(x, y, sigma):
    """
    Compute the value of 2D gausssian function at (x, y).
    Parametrs: x: X-coordinate
    y: Y-coordinate
    sigma: standard deviation of gaussian
    """
    
    return (1 / (2 * np.pi * sigma**2)) * np.exp(
        -(x**2 + y**2) / (2 * sigma**2))

def plot(z):
    """
    Plot a 2D array using imshow.
    """
    plt.imshow(z.T)
    plt.gca().invert_yaxis()  # flip axes to get imshow to plot representatively
    plt.xlabel("X"); 
    plt.ylabel("Y"); 
    plt.title(f"{z.shape} points")
    plt.gca().set_aspect(1)

def compute_chunk(xmin: float, xmax: float,
         ymin: float, ymax: float,
         sigma: float = 1) -> None:
    """
    Compute 2D Gaussian over a grid and plot it.
    """
    X = np.arange(xmin, xmax, STEP)
    Y = np.arange(ymin, ymax, STEP)

    Z = []

    for x in X:
        for y in Y:
            Z.append(gaussian2D(x, y, sigma))

    return np.array(Z).reshape(len(X), len(Y))


def save_plot(data, xmin, xmax):
    """
    Save figure for this chunk.
    """
    plt.figure()
    plt.imshow(data.T)
    plt.gca().invert_yaxis()
    #plt.title(f"X range: {xmin} to {xmax}")
    plt.gca().set_aspect(1)
    plt.savefig(f"gaussian_{xmin}_{xmax}.png")
    plt.close()


if __name__ == "__main__":
    # Expect xmin and xmax from command line
    if len(sys.argv) != 3:
        print("Usage: python 2d_gaussian_embarrassing.py xmin xmax")
        sys.exit(1)

    xmin = float(sys.argv[1])
    xmax = float(sys.argv[2])

    start = time.time()
    chunk = compute_chunk(xmin, xmax, -2, 2)
    save_plot(chunk, xmin, xmax)
    elapsed = time.time() - start

    print(f"Chunk {xmin} to {xmax} completed in {elapsed:.2f} s")

