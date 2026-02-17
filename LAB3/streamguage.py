import numpy as np
import matplotlib.pyplot as plt

def read_guage_file(fid):
    """
    Read USGS Guage data and convert date and time to minutes since start

    parameters
    fid (str): phelan_creek_stream_guage_2024-09-07_to_2024-09-14.txt

    returns
    timestamp (list): 
    time in the minutes
    hgt (np.array): guage height in ft
    """

    date, time, hgt = np.loadtxt(fid, skiprows=28, usecols=[2,3,5], 
                                    dtype=str).T

    hgt = hgt.astype(float)
    days = [float(d[-2:]) for d in date]  # get DD from YYYY-MM-DD
    hours = [float(t.split(":")[0]) for t in time]  # get HH from HH:MM
    mins = [float(t.split(":")[1]) for t in time]  # get MM from HH:MM

    timestamps = []
    for d, h, m in zip(days, hours, mins):
        timestamp = (d * 24 * 60) + (h * 60) + m
        timestamps.append(timestamp)

    return timestamps, hgt
    
def plot(timestamps, hgt):
    plt.figure(figsize=(12, 8))
    plt.plot(timestamps, hgt, '-o', linewidth = 1)
    plt.xlabel("Time (minutes since start of record)")
    plt.ylabel("Guage height (ft)")
    plt.title('Phelan Creek Stream Gauge Data')
    plt.show()

def main():
    # load the data text file
    fid = "phelan_creek_stream_guage_2024-09-07_to_2024-09-14.txt"
    timestamps, hgt = read_guage_file(fid)

    # plot
    plot(timestamps, hgt)

if __name__ == "__main__":
    main()
