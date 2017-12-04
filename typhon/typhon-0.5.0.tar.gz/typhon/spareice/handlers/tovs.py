from datetime import datetime, timedelta
import time
import warnings

import h5py
import numpy as np
from typhon.spareice.array import Array
from typhon.spareice.geographical import GeoData
import xarray as xr

from .. import handlers

__all__ = [
    'MHSAAPP',
    ]


class MHSAAPP(handlers.FileHandler):
    """File handler for MHS level 1C HDF files (convert with the AAPP tool.)
    """
    # This file handler always wants to return at least time, lat and lon
    # fields. These fields are required for this:
    standard_fields = [
        "Data/scnlintime", "Data/scnlinyr", "Data/scnlindy",
        "Geolocation/Latitude", "Geolocation/Longitude"]

    mapping = {
        "Geolocation/Latitude": "lat",
        "Geolocation/Longitude": "lon",
    }

    def __init__(self, mapping=None, apply_scaling=True, **kwargs):
        """

        Args:
            mapping: A dictionary of old and new names. The fields are going to
                be renamed according to it.
            apply_scaling: Apply the scaling parameters given in the
                variable's attributes to the data. Default is true.
            **kwargs: Additional key word arguments for base class.
        """
        # Call the base class initializer
        super().__init__(**kwargs)

        self.user_mapping = mapping
        self.apply_scaling = apply_scaling

    def get_info(self, filename, **kwargs):
        with h5py.File(filename, "r") as file:
            start = \
                datetime(int(file.attrs["startdatayr"][0]), 1, 1) \
                + timedelta(days=int(file.attrs["startdatady"][0]) - 1) \
                + timedelta(
                    milliseconds=int(file.attrs["startdatatime_ms"][0]))
            end = \
                datetime(int(file.attrs["enddatayr"]), 1, 1) \
                + timedelta(days=int(file.attrs["enddatady"]) - 1) \
                + timedelta(milliseconds=int(file.attrs["enddatatime_ms"]))

            info = handlers.FileInfo()
            info["times"] = [start, end]

            return info

    def read(self, filename, fields=None):
        """Reads and parses NetCDF files and load them to a GeoData object.

        TODO: Extend documentation.
        """

        if fields is not None:
            fields_to_extract = fields + self.standard_fields
            fields_to_extract = set(fields_to_extract)
            try:
                fields_to_extract.remove("time")
                fields_to_extract.remove("lat")
                fields_to_extract.remove("lon")
            except KeyError:
                pass
            fields_to_extract = list(fields_to_extract)
        else:
            fields_to_extract = fields

        dataset = GeoData.from_netcdf(filename, fields_to_extract)
        dataset.name = "MHS"

        # We do the internal mapping first so we do not deal with difficult
        # names in the following loop.
        dataset.rename(self.mapping, inplace=True)

        # Add standard field "time":
        dataset["time"] = self._get_time_field(dataset)

        # Flat the latitude and longitude vectors:
        dataset["lon"] = dataset["lon"].flatten()
        dataset["lat"] = dataset["lat"].flatten()

        # Some fields need special treatment
        vars_to_drop = []
        for var in dataset.vars(deep=True):
            # Some variables have been loaded only for temporary reasons.
            if (var in self.standard_fields
                    and fields is not None
                    and var not in fields):
                vars_to_drop.append(var)

            if var == "Data/btemps":
                # Unfold the dimension of the brightness temperature variable
                # to the shapes of the time vector.
                dataset[var] = dataset[var].reshape(
                    dataset[var].shape[0] * 90, 5
                )
                dataset[var].dims = ["time_id", "channel"]

            # Some variables are scaled. If the user wants us to do
            # rescaling, we do it and delete the note in the attributes.
            if self.apply_scaling and "Scale" in dataset[var].attrs:
                dataset[var] = dataset[var] * dataset[var].attrs["Scale"]
                del dataset[var].attrs["Scale"]

        dataset.drop(vars_to_drop, inplace=True)

        if self.user_mapping is not None:
            dataset.rename(self.user_mapping)
        return dataset

    def _get_time_field(self, dataset):
        # Interpolate between the start times of each swath to retrieve the
        # timestamp of each pixel.
        swath_start_indices = np.arange(
            0, dataset["Data"]["scnlintime"].size * 90, 90)
        pixel_times = np.interp(
            np.arange((dataset["Data/scnlintime"].size - 1) * 90),
            swath_start_indices, dataset["Data/scnlintime"])

        # Add the timestamps from the last swath here, we could not interpolate
        # them in the step before because we do not have an ending timestamp.
        # We simply extrapolate from the difference between the last two
        # timestamps.
        last_swath_pixels = \
            dataset["Data/scnlintime"][-1] \
            - dataset["Data/scnlintime"][-2] \
            + np.linspace(
                dataset["Data/scnlintime"][-2], dataset["Data/scnlintime"][-1],
                90, dtype="int32", endpoint=False)
        pixel_times = np.concatenate([pixel_times, last_swath_pixels])

        # Convert the pixel times into timedelta objects
        pixel_times = pixel_times.astype("timedelta64[ms]")

        # Convert the swath time variables (year, day of year, miliseconds
        # since midnight) to numpy.datetime objects. These are the start times
        # of each swath, we have to bring them together with the interpolated
        # pixel times.
        swath_times = \
            dataset["Data/scnlinyr"].astype('datetime64[Y]') - 1970 \
            + dataset["Data/scnlindy"].astype('timedelta64[D]') - 1

        swath_times = np.repeat(swath_times, 90)
        times = swath_times + pixel_times

        return times.flatten().astype("O")
