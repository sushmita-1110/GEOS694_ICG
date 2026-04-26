import numpy as np
import matplotlib.pyplot as plt
import time
from numba import jit

from data_utils import get_example_data
from utils import benchmark


@jit(nopython=True)
def stalta_numba(x, nsta, nlta):
    n = len(x)
    ratio = np.zeros(n)

    for i in range(nlta, n):
        sta = 0.0
        for j in range(i - nsta, i):
            sta += x[j] * x[j]
        sta /= nsta

        lta = 0.0
        for j in range(i - nlta, i):
            lta += x[j] * x[j]
        lta /= nlta

        if lta > 0:
            ratio[i] = sta / lta
        else:
            ratio[i] = 0.0

    return ratio


if __name__ == "__main__":
    x, sampling_rate = get_example_data(plot=False)

    x = x.astype(np.float64)
    t = np.arange(len(x)) / sampling_rate

    nsta = int(sampling_rate * 0.5)
    nlta = int(sampling_rate * 10.0)

    # First call includes compilation time
    start = time.perf_counter()
    result_numba = stalta_numba(x, nsta, nlta)
    compile_time = time.perf_counter() - start
    print(f"Numba first call (includes compilation): {compile_time:.3f} seconds")

    # Later calls do not include compilation
    time_numba, result_numba = benchmark(stalta_numba, x, nsta, nlta)
    print(f"Numba after warmup: {time_numba:.3f} seconds")

    fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    ax[0].plot(t, x, color="k", lw=0.6)
    ax[0].set_ylabel("Amplitude")
    ax[0].set_title(f"Seismic data, fs={sampling_rate} Hz")

    # STA/LTA output starts at nlta, so use matching time axis
    t_ratio = t[nlta:]
    ax[1].plot(t_ratio, result_numba, color="C3")
    ax[1].axhline(3.0, color="r", ls="--", lw=1)
    ax[1].set_ylabel("STA/LTA")
    ax[1].set_xlabel("Time (s)")

    plt.tight_layout()
    plt.show()