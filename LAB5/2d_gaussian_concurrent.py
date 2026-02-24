"""
2D Gaussian computation using multiprocessing
with concurrent.futures.

This version splits the x-domain into 4 parts,
computes them in parallel, and visibly stacks
them into one final figure.
"""

import os
import time
import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor

# Step size
#STEP = 0.001

STEP = 0.0004

def gaussian2D(x, y, sigma):
    """
    Compute the value of 2D gaussian function at (x, y).
    """
    return (1 / (2 * np.pi * sigma**2)) * np.exp(
        -(x**2 + y**2) / (2 * sigma**2)
    )


def compute_chunk(args):
    """
    Compute 2D Gaussian over a chunk of x values.
    """
    xmin, xmax, ymin, ymax, sigma, index = args

    X = np.arange(xmin, xmax, STEP)
    Y = np.arange(ymin, ymax, STEP)

    Z = []

    for x in X:
        for y in Y:
            Z.append(gaussian2D(x, y, sigma))

    chunk = np.array(Z).reshape(len(X), len(Y))

    print(f"Chunk {index} finished: {xmin} to {xmax}")

    return chunk


def main(xmin, xmax, ymin, ymax, sigma=1, max_workers=4):

    # Split x-domain into equal chunks
    x_splits = np.linspace(xmin, xmax, max_workers + 1)

    tasks = []
    for i in range(max_workers):
        tasks.append(
            (x_splits[i], x_splits[i + 1], ymin, ymax, sigma, i)
        )

    # Run multiprocessing
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(compute_chunk, tasks))

    # Stack chunks vertically (x-direction)
    final = np.vstack(results)

    # Plot final stacked image
    plt.figure()
    plt.imshow(final.T)
    plt.gca().invert_yaxis()

    # Draw white lines to show stack boundaries
    chunk_height = results[0].shape[0]
    for i in range(1, max_workers):
        plt.axhline(i * chunk_height, color="white", linewidth=1)

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"{final.shape} points (4 stacked)")
    plt.gca().set_aspect(1)

    return final


if __name__ == "__main__":
    print(f"CPU count: {os.cpu_count()}")

    # Create output directory 
    output_dir = "task4_image"
    os.makedirs(output_dir, exist_ok=True)

    worker_list = list(range(1, 13))  # adjust as needed
    runtimes = []

    for workers in worker_list:
        print(f"\nRunning with {workers} workers...")
        start = time.time()

        main(-2, 2, -2, 2, max_workers=workers)

        elapsed = time.time() - start
        runtimes.append(elapsed)

        print(f"Workers: {workers}, Time: {elapsed:.2f} s")

    # Save scaling plot
    plt.figure()
    plt.plot(worker_list, runtimes, marker="o")
    plt.xlabel("max_workers")
    plt.ylabel("Runtime (s)")
    plt.title(f"Scaling of 2D Gaussian (STEP={STEP})")
    plt.grid(True)

    scaling_path = os.path.join(
        output_dir, f"scaling_STEP_{STEP}.png"
    )
    plt.savefig(scaling_path, dpi=300)
    print(f"Scaling plot saved to {scaling_path}")

    plt.show()

    """
    # Plot scaling curve
    plt.figure()
    plt.plot(worker_list, runtimes, marker="o")
    plt.xlabel("max_workers")
    plt.ylabel("Runtime (s)")
    plt.title("Scaling of 2D Gaussian (Multiprocessing)")
    plt.grid(True)
    plt.show()
    
    """



    """
    Task 3
    start = time.time()

    main(-2, 2, -2, 2, max_workers=4)

    elapsed = time.time() - start
    print(f"Elapsed Time: {elapsed:.2f} s")

    plt.show()
    
    """


