import numpy as np
import matplotlib.pyplot as plt

from data_utils import get_example_data
from utils import benchmark
from seismic_data_python import stalta_python
from seismic_data_numpy import stalta_numpy
from seismic_data_numba import stalta_numba


if __name__ == "__main__":
    x, sampling_rate = get_example_data(plot=False)
    t = np.arange(len(x)) / sampling_rate

    nsta = int(sampling_rate * 0.5)
    nlta = int(sampling_rate * 10.0)

    # Warm up Numba before timing
    _ = stalta_numba(x, nsta, nlta)

    methods = {
        "Python": stalta_python,
        "NumPy": stalta_numpy,
        "Numba": stalta_numba,
    }

    times = {}
    results = {}

    for name, func in methods.items():
        times[name], results[name] = benchmark(func, x, nsta, nlta)

    print(f"Pure Python: {times['Python']:.3f} seconds")
    print(f"NumPy:       {times['NumPy']:.3E} seconds")
    print(f"Numba:       {times['Numba']:.3f} seconds\n")

    np.testing.assert_allclose(results["Python"], results["NumPy"], rtol=1e-5, atol=1e-8)
    np.testing.assert_allclose(results["Python"], results["Numba"], rtol=1e-5, atol=1e-8)

    fig, ax = plt.subplots(4, 1, figsize=(10, 9), sharex=True)

    ax[0].plot(t, x, color="k", lw=0.6)
    ax[0].set_ylabel("Amplitude")
    ax[0].set_title(f"Seismic data, fs={sampling_rate} Hz")

    for axis, name, color in zip(ax[1:], methods.keys(), ["C0", "C1", "C2"]):
        axis.plot(t, results[name], color=color)
        axis.axhline(3.0, color="r", ls="--", lw=1)
        axis.set_ylabel(name)

    ax[-1].set_xlabel("Time (s)")

    plt.tight_layout()
    plt.savefig('plot.png', dpi=300)
    plt.show()