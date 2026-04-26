import numpy as np
import matplotlib.pyplot as plt

from data_utils import get_example_data
from utils import benchmark


def stalta_numpy(x, nsta, nlta):
    """Calculate STA/LTA with NumPy calls only"""
    n  = len(x)
    x2 = x ** 2                    # squared amplitude
    cs = np.cumsum(x2)             # cumulative sum of squared amplitude

    # Prepend a zero so that cs[i] - cs[i-w] gives the sum over w samples
    cs = np.concatenate([[0], cs])

    ratio = np.zeros(n)

    # Valid range: need at least nlta samples behind us
    i = np.arange(nlta, n)

    sta = (cs[i] - cs[i - nsta]) / nsta
    lta = (cs[i] - cs[i - nlta]) / nlta

    valid = lta > 0
    ratio[i[valid]] = sta[valid] / lta[valid]

    return ratio

if __name__ == "__main__":
    x, sampling_rate = get_example_data(plot=False)

    t = np.arange(len(x)) / sampling_rate

    nsta = int(sampling_rate * 0.5)
    nlta = int(sampling_rate * 10.0)
    time_numpy, result_numpy = benchmark(
        stalta_numpy, x, nsta, nlta)

    print(f"NumPy: {time_numpy:.3E} seconds")

    fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    ax[0].plot(t, x, color="k", lw=0.6)
    ax[0].set_ylabel("Amplitude")
    ax[0].set_title(f"Seismic data, fs={sampling_rate} Hz")

    ax[1].plot(t, result_numpy, color="C3")
    ax[1].axhline(3.0, color="r", ls="--", lw=1)
    ax[1].set_ylabel("STA/LTA")
    ax[1].set_xlabel("Time (s)")

    plt.tight_layout()
    plt.show()