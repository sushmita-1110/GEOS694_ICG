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

class StreamGuage:
    units = "ft"

    def __init__(self, fid, station_id, station_name, starttime):
        self.fid = fid
        self.station_id = station_id
        self.station_name = station_name
        self.starttime = starttime
        self.time = []
        self.hgt = []

    def read_guage_file(self):
        time, hgt = read_guage_file(self.fid)
        self.time = time
        self.hgt = hgt

    def plot(self):
        plt.figure()
        plt.plot(self.time, self.hgt, '-o', linewidth=0.5)

        title = (
            f"Stream Guage {self.station_id} | "
            f"{self.station_name} | "
            f"Start: {self.starttime} | "
            f"Max: {np.max(self.hgt):.2f} {self.units}"
        )

        plt.title(title)
        plt.xlabel("Time (minutes since start of record)")
        plt.ylabel(f"Guage height ({self.units})")
        plt.show()


if __name__ == "__main__":
    fid = "phelan_creek_stream_guage_2024-09-07_to_2024-09-14.txt"
    sg = StreamGuage(fid=fid, station_id="15478040", 
                     station_name="PHELAN CREEK", starttime="2024-09-07 00:00")
    assert(len(sg.hgt) == 0)  # check that we haven't read data yet
    
    sg.read_guage_file()
    assert(len(sg.time) == len(sg.hgt))  # check that data and time are equal

    sg.plot()