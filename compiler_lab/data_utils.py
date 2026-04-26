from obspy import read
import numpy as np

def get_example_data(plot=False):
    """Returns 1 Hz highpassed vertical component seismometer data."""
    st = read()
    st.filter("highpass", freq=1)
    st = st.select(component="Z")
    st.resample(100)
    st.taper(0.05)

    # Pad zeros on front and back to allow STA/LTA to start running average
    n = len(st[0].data)
    data_out = np.hstack([np.zeros(n), st[0].data, np.zeros(n)])

    if plot:
        st.plot()

    return data_out, st[0].stats.sampling_rate