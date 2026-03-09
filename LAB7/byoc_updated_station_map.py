"""
Plot Alaska (AK) seismic stations on a topographic map using PyGMT.

This script reads station coordinates from text file
and generates a map of Alaska showing station locations and labels.

Input
-----
- gmap-stations-AK.txt
  Text file containing at least the following columns:
    - Station
    - Latitude
    - Longitude

Output
------
- AK_station_alaska_map.png
  A PNG image of the Alaska AK(network) station map.

How to run
----------
1. Install the required packages:
   pip install pandas 
   conda install -c conda-forge pygmt

2. Place the input file `gmap-stations-AK.txt` in the same directory
   as this script.

3. Run the script:
   
"""

from pathlib import Path

import pandas as pd
import pygmt


INPUT_FILE = Path("gmap-stations-AK.txt")
OUTPUT_FILE = Path("AK_station_alaska_map.png")

REGION = [-170, -135, 51, 70]
PROJECTION = "L-150/62/55/65/12c"
RELIEF_GRID = "@earth_relief_03m"
MAP_TITLE = "Alaska Stations"


def load_station_data(file_path: Path) -> pd.DataFrame:
    """
    Load station data from a pipe-delimited text file.

    Parameters
    ----------
    file_path : Path
        Path to the station data file.

    Returns
    -------
    pd.DataFrame
        DataFrame containing station names, latitudes, and longitudes.

    Raises
    ------
    FileNotFoundError
        If the input file does not exist.
    ValueError
        If required columns are missing.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    station_df = pd.read_csv(file_path, sep="|")

    required_columns = {"Station", "Latitude", "Longitude"}
    missing_columns = required_columns - set(station_df.columns)
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {', '.join(sorted(missing_columns))}"
        )

    return station_df


def create_station_map(station_df: pd.DataFrame) -> pygmt.Figure:
    """
    Create a PyGMT figure showing Alaska station locations.

    Parameters
    ----------
    station_df : pd.DataFrame
        DataFrame containing station data with Station, Latitude,
        and Longitude columns.

    Returns
    -------
    pygmt.Figure
        
    """
    figure = pygmt.Figure()

    figure.grdimage(
        grid=RELIEF_GRID,
        region=REGION,
        projection=PROJECTION,
        shading=True,
        cmap="geo",
    )

    figure.coast(
        region=REGION,
        projection=PROJECTION,
        shorelines="0.6p,black",
        borders=["1/0.5p,black", "2/0.25p,gray40"],
        rivers="a/0.25p,blue",
        lakes="lightblue",
        resolution="i",
    )

    figure.plot(
        x=station_df["Longitude"],
        y=station_df["Latitude"],
        style="i0.14c",
        fill="red",
        pen="0.25p,black",
    )

    figure.text(
        x=station_df["Longitude"],
        y=station_df["Latitude"],
        text=station_df["Station"],
        font="1.5p,Helvetica-Bold,black",
        justify="LT",
        offset="0.05c/0.05c",
        fill="white",
    )

    figure.basemap(frame=["af", f"+t{MAP_TITLE}"])

    return figure


def save_and_show_map(figure: pygmt.Figure, output_file: Path) -> None:
    """
    Save the map to disk and display it.

    Parameters
    ----------
    figure : pygmt.Figure
        The PyGMT figure to save and display.
    output_file : Path
        Path where the output image will be written.
    """
    figure.savefig(output_file, dpi=600)
    figure.show()


def main():
    station_df = load_station_data(INPUT_FILE)
    figure = create_station_map(station_df)
    save_and_show_map(figure, OUTPUT_FILE)


if __name__ == "__main__":
    main()