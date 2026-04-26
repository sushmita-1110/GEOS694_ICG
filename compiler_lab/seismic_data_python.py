import numpy as np
import matplotlib.pyplot as plt

from data_utils import get_example_data
from utils import benchmark


def stalta_python(x, nsta, nlta):
    n = len(x)
    ratio = [0] * nlta  # pad zeros before STA/LTA is valid

    for i in range(nlta, n):
        # STA: mean squared amplitude over short window
        sta = 0.0
        for j in range(i - nsta, i):
            sta += x[j] * x[j]
        sta /= nsta

        # LTA: mean squared amplitude over long window
        lta = 0.0
        for j in range(i - nlta, i):
            lta += x[j] * x[j]
        lta /= nlta

        if lta > 0:
            ratio.append(sta / lta)
        else:
            ratio.append(0)

    return np.array(ratio)


if __name__ == "__main__":
    x, sampling_rate = get_example_data(plot=False)

    t = np.arange(len(x)) / sampling_rate

    nsta = int(sampling_rate * 0.5)    # 0.5 s STA
    nlta = int(sampling_rate * 10.0)   # 10 s LTA

    time_python, result_python = benchmark(stalta_python, x, nsta, nlta)

    print(f"Pure Python: {time_python:.3f} seconds")

    fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    ax[0].plot(t, x, color="k", lw=0.6)
    ax[0].set_ylabel("Amplitude")
    ax[0].set_title(f"Seismic data, fs={sampling_rate} Hz")

    ax[1].plot(t, result_python, color="C3")
    ax[1].axhline(3.0, color="r", ls="--", lw=1)
    ax[1].set_ylabel("STA/LTA")
    ax[1].set_xlabel("Time (s)")

    plt.tight_layout()
    plt.show()