import numpy as np
import matplotlib.pyplot as plt

from data_utils import get_example_data
from utils import benchmark
from seismic_data_python import stalta_python
from seismic_data_numpy import stalta_numpy
from seismic_data_numba import stalta_numba
from stalta_cy import stalta_cython


if __name__ == "__main__":
    x, sampling_rate = get_example_data(plot=False)
    x = x.astype(np.float64)

    t = np.arange(len(x)) / sampling_rate
    nsta = int(sampling_rate * 0.5)
    nlta = int(sampling_rate * 10.0)

    # Warm up Numba
    _ = stalta_numba(x, nsta, nlta)

    methods = {
        "Python": stalta_python,
        "NumPy": stalta_numpy,
        "Numba": stalta_numba,
        "Cython": stalta_cython,
    }

    times, results = {}, {}

    for name, func in methods.items():
        times[name], results[name] = benchmark(func, x, nsta, nlta)

    print(f"Pure Python: {times['Python']:.3f} seconds")
    print(f"NumPy:       {times['NumPy']:.3E} seconds")
    print(f"Numba:       {times['Numba']:.3f} seconds")
    print(f"Cython:      {times['Cython']:.3E} seconds\n")

    for name in ["NumPy", "Numba", "Cython"]:
        print(f"Speedup {name} vs Python: {times['Python'] / times[name]:.1f}x")

    print(f"Speedup Cython vs NumPy: {times['NumPy'] / times['Cython']:.1f}x")
    print(f"Speedup Cython vs Numba: {times['Numba'] / times['Cython']:.1f}x")

for name in ["NumPy", "Numba"]:
    np.testing.assert_allclose(
        results["Python"], results[name], rtol=1e-5, atol=1e-8
    )
    np.testing.assert_allclose(
        results["Python"][nlta + 1:],
        results["Cython"][nlta:-1],
        rtol=1e-4,
        atol=1e-1,
    )
    
    print("Results match.")

    fig, ax = plt.subplots(5, 1, figsize=(10, 11), sharex=True)

    ax[0].plot(t, x, color="k", lw=0.6)
    ax[0].set_ylabel("Amplitude")
    ax[0].set_title(f"Seismic data, fs={sampling_rate} Hz")

    for axis, name, color in zip(ax[1:], methods.keys(), ["C0", "C1", "C2", "C3"]):
        axis.plot(t, results[name], color=color)
        axis.axhline(3.0, color="r", ls="--", lw=1)
        axis.set_ylabel(name)

    ax[-1].set_xlabel("Time (s)")
    plt.tight_layout()
    plt.show()