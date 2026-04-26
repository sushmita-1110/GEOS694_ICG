import numpy as np
import time
import matplotlib.pyplot as plt

def benchmark(func, *args, repeat=5):
    """Run a function several times and return the median runtime in seconds."""
    times = []
    for _ in range(repeat):
        start = time.perf_counter()
        result = func(*args)
        end = time.perf_counter()
        times.append(end - start)
    return np.median(times), result