"""
2D Gaussian computation (serial version)

This script computes and plots a 2D Gaussian distribution
using nested loops (serial implementation).
"""

import time
import numpy as np
import matplotlib.pyplot as plt

# Step size
STEP = .0004

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

def main(xmin: float, xmax: float,
         ymin: float, ymax: float,
         sigma: float = 1) -> None:
    """
    Compute 2D Gaussian over a grid and plot it.
    """
    X = np.arange(xmin, xmax, STEP)
    Y = np.arange(ymin, ymax, STEP)

    Z = []

    # 1D array 
    # Compute gaussian values
      
    for x in X:
        for y in Y:
            Z.append(gaussian2D(x, y, sigma))

    # Convert to 2D array        
    ZZ = np.array(Z).reshape(len(X), len(Y))  
  
    # Plot
    plot(ZZ)

if __name__ == "__main__":
    start = time.time()
    main(-2, 2, -2, 2)
    elapsed = time.time() - start
    print(f"Elapsed Time: {elapsed:.2f} s")
    plt.show()