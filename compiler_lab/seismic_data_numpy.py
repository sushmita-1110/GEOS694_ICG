from obspy import read
import numpy as np
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
    tr = get_example_data(plot=False)
    t = tr.times()            # seconds relative to trace start
    x = tr.data.astype(float)

    nsta = int(tr.stats.sampling_rate * 0.5)   # 0.5 s STA
    nlta = int(tr.stats.sampling_rate * 10.0)  # 10 s LTA
    ratio = stalta_numpy(x, nsta, nlta)
    time_numpy, result_numpy = benchmark(
    stalta_numpy, x, nsta, nlta
    )

    print(f"NumPy: {time_numpy:.3E} seconds")

    fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    ax[0].plot(t, x, color="k", lw=0.6)
    ax[0].set_ylabel("Amplitude")
    ax[0].set_title(f"{tr.id}  fs={tr.stats.sampling_rate} Hz")

    ax[1].plot(t, ratio, color="C3")
    ax[1].axhline(3.0, color="r", ls="--", lw=1)  # threshold
    ax[1].set_ylabel("STA/LTA")
    ax[1].set_xlabel("Time (s)")

    plt.tight_layout()
    plt.show()