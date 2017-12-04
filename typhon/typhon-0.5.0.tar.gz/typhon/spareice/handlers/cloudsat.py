from datetime import datetime, timedelta
import warnings

from netCDF4 import Dataset
import numpy as np
import pandas as pd
from pyhdf import HDF, VS, V
from typhon.spareice.array import Array
from typhon.spareice.geographical import GeoData

from .. import handlers

__all__ = [
    'C2CICE',
]


class C2CICE(handlers.FileHandler):
    mapping = {
        "lat": "Latitude",
        "lon": "Longitude"
    }

    def __init__(self, **kwargs):
        # Call the base class initializer
        super().__init__(**kwargs)

    def get_info(self, filename, **kwargs):
        with Dataset(filename, "r") as file:
            info = handlers.FileInfo()
            start = datetime.strptime(file.start_time, "%Y%m%d%H%M%S")
            end = datetime.strptime(file.end_time, "%Y%m%d%H%M%S")
            info["times"] = [start, end]
            return info

    def read(self, filename, fields=None):
        """Reads and parses NetCDF files and load them to a xarray.

        See the parent class for further documentation.
        """

        if fields is None:
            fields = ["time", "lat", "lon"]
        else:
            fields = list(set(fields + ["time", "lat", "lon"]))

        dataset = GeoData(name="2C-ICE")

        # The files are in HDF4 format therefore we cannot use the netCDF4
        # module. This code is taken from
        # http://hdfeos.org/zoo/OTHER/2010128055614_21420_CS_2B-GEOPROF_GRANULE_P_R04_E03.hdf.py
        # and adapted by John Mrziglod. A description about all variables in
        # CloudSat 2C-ICE dataset can be found in
        # http://www.cloudsat.cira.colostate.edu/data-products/level-2c/2c-ice?term=53.

        try:
            file = HDF.HDF(filename)
            vs = file.vstart()

            for field, dimensions in self.parse_fields(fields):
                data = None

                # The time variable has to be handled as something special:
                if field == "time":
                    # This gives us the starting time of the first profile in
                    # seconds since 1st Jan 1993.
                    first_profile_time_id = vs.attach(vs.find('TAI_start'))
                    first_profile_time_id.setfields('TAI_start')
                    nrecs, _, _, _, _ = first_profile_time_id.inquire()
                    first_profile_time = \
                        first_profile_time_id.read(nRec=nrecs)[0][0]
                    first_profile_time_id.detach()

                    # This gives us the starting time of all other profiles in
                    # seconds since the start of the first profile.
                    profile_times_id = vs.attach(vs.find('Profile_time'))
                    profile_times_id.setfields('Profile_time')
                    nrecs, _, _, _, _ = profile_times_id.inquire()
                    profile_times = profile_times_id.read(nRec=nrecs)
                    profile_times_id.detach()
                    profile_times = np.asarray(profile_times).flatten()

                    start_time = datetime(1993, 1, 1) + timedelta(
                        seconds=first_profile_time)

                    # Put all times together so we obtain one full timestamp
                    # (date + time) for each data point
                    data = Array(
                        pd.to_datetime(
                            profile_times, unit='s',
                            origin=pd.Timestamp(start_time)
                        ).to_pydatetime(),
                        dims=["time_id"]
                    )
                else:
                    # All other data (including latitudes, etc.)

                    if field in self.mapping:
                        field_id = vs.find(self.mapping[field])
                    else:
                        field_id = vs.find(field)

                    if field_id == 0:
                        # Field was not found.
                        warnings.warn(
                            "Field '{0}' was not found!".format(field),
                            RuntimeWarning)
                        continue

                    field_id = vs.attach(field_id)
                    #field_id.setfields(field)

                    nrecs, _, _, _, _ = field_id.inquire()
                    raw_data = field_id.read(nRec=nrecs)
                    data = Array(raw_data).flatten()
                    data.dims = ["time_id"]
                    field_id.detach()

                # Add the field data to the dataset.
                dataset[field] = self.select(data, dimensions)

        except Exception as e:
            raise e
        finally:
            file.close()

        return dataset
