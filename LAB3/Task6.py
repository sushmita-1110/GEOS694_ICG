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

    def __init__(self, fid, station_id, station_name, starttime, units):
        self.fid = fid
        self.station_id = station_id
        self.station_name = station_name
        self.starttime = starttime
        self.time = []
        self.hgt = []
        self.units = units

    def read_guage_file(self):
        time, hgt = read_guage_file(self.fid)
        self.time = time
        self.hgt = hgt
        #print(self.time)
        #print(self.hgt)

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

    def convert(self):
        if self.units == "ft":
            self.hgt = self.hgt * 0.3048
            self.units = "m"

    def demean(self):
        self.hgt = self.hgt - np.mean(self.hgt)
 
    def shift_time(self, minutes):
        """Shift time axis by defined minutes."""  
        for i in range(len(self.time)):
            self.time[i] = self.time[i] + minutes

    def main(self, convert=True, demean=True, shift=-100):
        """
        Run standard processing steps:
        1. Read data
        2. Convert units
        3. Demean data
        4. Shift time
        5. plot
        """
        self.read_guage_file()

        if convert:
            self.convert()

        if demean:
            self.demean()

        if shift != 0:
            self.shift_time(shift)

        self.plot()


class NOAAStreamGuage(StreamGuage):
    units = "m"  # NOAA data 
    def convert(self):
        # NOAA data is already in meters, so do nothing
        pass

    def read_guage_file(self):
        super().read_guage_file()
        # Add NOAA-specific behavior
        print("NOAA stream guage")

if __name__ == "__main__":
    # USGS StreamGuage
    usgs_fid = "phelan_creek_stream_guage_2024-10-07_to_2024-10-14.txt"
    sg = StreamGuage(usgs_fid, "15478040", "PHELAN CREEK", "2024-10-07 00:00", "ft")
    sg.main(convert=True, demean=True, shift=-100)

    # NOAA StreamGuage
    noaa_fid = "noaa_creek_stream_guage_2024-10-07_to_2024-10-14.txt"
    noaa_sg = NOAAStreamGuage(noaa_fid, "NN0001", "NOAA CREEK", "2024-10-07 00:00", "m")
    noaa_sg.main(convert=False, demean=True, shift=-100)