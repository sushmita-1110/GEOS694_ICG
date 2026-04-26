from obspy import read
import numpy as np
import time
from numba import jit
import matplotlib.pyplot as plt
from setup import benchmark

def get_example_data(plot=False):
    """Returns 1Hz highpassed vertical (Z) component seismometer data"""
    st = read()
    st.filter("highpass", freq=1)
    st = st.select(component="Z")
    st.resample(100)  # upsample from 100 Hz
    st.taper(0.05)

        # Pad zeros on front and back to allow STA/LTA to start running average
    #n = len(st[0].data)
    #data_out = np.hstack([np.zeros(n), st[0].data, np.zeros(n)])  # pad zeros
    
    if plot:
        st.plot()
    return st[0]  

@jit(nopython=True)
def stalta_numba(x, nsta, nlta):
    n = len(x)
    ratio = []

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
    tr = get_example_data(plot=False)
    t = tr.times()            # seconds relative to trace start
    x = tr.data.astype(float)

    nsta = int(tr.stats.sampling_rate * 0.5)   # 0.5 s STA
    nlta = int(tr.stats.sampling_rate * 10.0)  # 10 s LTA
    ratio = stalta_numba(x, nsta, nlta)
    time_numba, result_numba = benchmark(
    stalta_numba, x, nsta, nlta
    )

    start = time.perf_counter()
    _ = stalta_numba(x, nsta, nlta)
    compile_time = time.perf_counter() - start
    print(f"Numba first call (includes compilation): {compile_time:.3f} seconds")
    time_numba, result_numba = benchmark(stalta_numba, x, nsta, nlta)
    print(f"Numba (after warmup): {time_numba:.3f} seconds")

    fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    ax[0].plot(t, x, color="k", lw=0.6)
    ax[0].set_ylabel("Amplitude")
    ax[0].set_title(f"{tr.id}  fs={tr.stats.sampling_rate} Hz")

    t_ratio = t[nlta:]
    ax[1].plot(t_ratio, ratio, color="C3")
    ax[1].axhline(3.0, color="r", ls="--", lw=1)  # threshold
    ax[1].set_ylabel("STA/LTA")
    ax[1].set_xlabel("Time (s)")

    plt.tight_layout()
    plt.show()