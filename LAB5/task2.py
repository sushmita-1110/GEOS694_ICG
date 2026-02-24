"""
Compute 2D Gaussian in parallel using multiprocessing.

Structured similarly to the prime-number parallel example.
"""

import os
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor, as_completed

STEP = 0.001


def gaussian2d(x, y, sigma=1.0):
    """Return 2D Gaussian value at (x, y)."""
    return (1 / (2 * np.pi * sigma**2)) * np.exp(-(x**2 + y**2) / (2 * sigma**2))


def compute_chunk(x_start, x_end, ymin, ymax, sigma=1.0):
    """
    Compute Gaussian for a chunk of the x-domain.
    Equivalent to get_prime(i, j) in the prime example.
    """
    X = np.arange(x_start, x_end, STEP)
    Y = np.arange(ymin, ymax, STEP)

    Z = []
    for x in X:
        row = [gaussian2d(x, y, sigma) for y in Y]
        Z.append(row)

    return x_start, np.array(Z)


def main(xmin, xmax, ymin, ymax):
    """Parallel Gaussian computation."""
    nproc = os.cpu_count()
    print(f"Using {nproc} processes")

    x_values = np.arange(xmin, xmax, STEP)
    total_points = len(x_values)

    step = total_points // nproc  

    futures = []
    start = time.time()

    with ProcessPoolExecutor(max_workers=4) as executor:

        for i in range(0, total_points, step):
            x_start = x_values[i]
            x_end = x_values[min(i + step, total_points - 1)]
            futures.append(
                executor.submit(compute_chunk, x_start, x_end, ymin, ymax)
            )

    # Collect results
    results = []

    for future in as_completed(futures):
        results.append(future.result())

    # Sort results by x_start to maintain order
    results.sort(key=lambda x: x[0])

    # Combine chunks
    ZZ = np.vstack([chunk for _, chunk in results])

    elapsed = time.time() - start
    print(f"Total Elapsed: {elapsed:.2f}s")

    # Plot final figure
    plt.imshow(ZZ.T)
    plt.gca().invert_yaxis()
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"2D Gaussian Parallel ({nproc} cores)")
    plt.gca().set_aspect(1)
    plt.show()


if __name__ == "__main__":
    start = time.time()
    main(-2, 2, -2, 2)
    elapsed = time.time() - start
    print(f"Overall Runtime: {elapsed:.2f}s")
