import numpy as np
import matplotlib.pyplot as plt


def read_gauge_file(fid):
    """
    Read USGS gauge data and convert date and time to minutes since start.

    Parameters
    ----------
    fid : str
        Path to gauge file.

    Returns
    -------
    timestamps : list
        Time in minutes since start of record.
    hgt : np.array
        Gauge height in feet.
    """

    date, time, hgt = np.loadtxt(
        fid,
        skiprows=28,
        usecols=[2, 3, 5],
        dtype=str
    ).T

    hgt = hgt.astype(float)

    days = [float(d[-2:]) for d in date]  # get DD from YYYY-MM-DD
    hours = [float(t.split(":")[0]) for t in time]  # get HH from HH:MM
    mins = [float(t.split(":")[1]) for t in time]  # get MM from HH:MM

    timestamps = []
    for d, h, m in zip(days, hours, mins):
        timestamp = (d * 24 * 60) + (h * 60) + m
        timestamps.append(timestamp)

    return timestamps, hgt


class StreamGauge:
    """Class for handling USGS stream gauge data."""

    def __init__(self, fid, station_id, station_name, starttime, units="ft"):
        self.fid = fid
        self.station_id = station_id
        self.station_name = station_name
        self.starttime = starttime
        self.units = units
        self.time = []
        self.hgt = []

    def read_gauge_file(self):
        """Read gauge data into class attributes."""
        self.time, self.hgt = read_gauge_file(self.fid)

    def plot(self):
        """Plot stream gauge data."""
        plt.figure()
        plt.plot(self.time, self.hgt, "-o", linewidth=0.5)

        title = (
            f"Stream Gauge {self.station_id} | "
            f"{self.station_name} | "
            f"Start: {self.starttime} | "
            f"Max: {np.max(self.hgt):.2f} {self.units}"
        )

        plt.title(title)
        plt.xlabel("Time (minutes since start of record)")
        plt.ylabel(f"Gauge height ({self.units})")
        plt.tight_layout()
        plt.show()

    def convert(self):
        """
        Convert gauge height from feet to meters.
        Updates units attribute.
        """
        if self.units == "ft":
            self.hgt = self.hgt * 0.3048
            self.units = "m"

    def demean(self):
        """Subtract mean value from gauge height."""
        self.hgt = self.hgt - np.mean(self.hgt)

    def shift_time(self, minutes):
        """
        Shift time axis by a specified number of minutes.
        """
        self.time = [t + minutes for t in self.time]


if __name__ == "__main__":

    fid = "phelan_creek_stream_guage_2024-09-07_to_2024-09-14.txt"

    sg = StreamGauge(
        fid,
        "15478040",
        "PHELAN CREEK",
        "2024-09-07 00:00",
        "ft"
    )

    sg.read_gauge_file()
    sg.plot()  # original data

    sg.convert()
    sg.demean()
    sg.shift_time(-100)
    sg.plot()  # processed data