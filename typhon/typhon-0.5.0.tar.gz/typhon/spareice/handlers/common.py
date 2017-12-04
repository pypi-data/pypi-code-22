import csv
from inspect import signature
import pickle

import numpy as np
import typhon.arts.xml
from typhon.spareice.array import ArrayGroup
import xarray

from .. import handlers

__all__ = [
    'CSV',
    'NetCDF4',
    # 'Numpy',
    # 'Pickle',
    # 'XML'
    ]


class CSV(handlers.FileHandler):
    """File handler that can read / write data from / to a ASCII file with
    comma separated values (or by any other delimiter).
    """
    def __init__(
            self, delimiter=None, header=None,
            skip_column=None, skip_header=None,
            **kwargs):
        """Initializes a CSV file handler class.

        Args:
            info_reader: (optional) You cannot use the :meth:`get_info`
                without giving a function here that returns a FileInfo object.
        """
        # Call the base class initializer
        super().__init__(**kwargs)

        self.delimiter = delimiter
        self.header = header
        self.skip_column = skip_column
        self.skip_header = skip_header

    def read(self, filename, fields=None):
        """Reads a CSV file and returns an ArrayGroup object.

        Args:
            filename:
            fields:

        Returns:
            An ArrayGroup object.
        """
        with open(filename, "r") as file:
            column_names = None

            if self.skip_header is not None:
                # Skip the header by ourselves because we may need the names
                # of the columns.
                line_number = 0
                while line_number < self.skip_header:
                    line = next(file)
                    line_number += 1
                    if line_number == self.header:
                        column_names = line.rstrip('\n').split(self.delimiter)

            raw_data = np.genfromtxt(
                (line.encode('utf-8') for line in file),
                delimiter=self.delimiter,
                dtype=None,
            )

            column_data = list(zip(*raw_data))

            table = ArrayGroup()
            if column_names is None:
                column_names = [
                    "col_" + str(c)
                    for c in range(len(column_data))]

            for column, name in enumerate(column_names):
                #name = str(name, 'utf-8')
                table[name] = column_data[column]

            return table


class NetCDF4(handlers.FileHandler):
    """File handler that can read / write data from / to a netCDF4 or HDF5
    file.
    """

    def __init__(self, return_type=None, **kwargs):
        """Initializes a NetCDF4 file handler class.

        Args:
            return_type: (optional) Defines what object should be returned by
                :meth:`read`. Default is *ArrayGroup* but *xarray* is also
                possible.
            info_reader: (optional) You cannot use the :meth:`get_info`
                without giving a function here that returns a FileInfo object.
        """
        # Call the base class initializer
        super().__init__(**kwargs)

        if return_type is None:
            self.return_type = "ArrayGroup"
        else:
            self.return_type = return_type

        # ArrayGroup supports reading from multiple files.
        if self.return_type == "ArrayGroup":
            self.multifile_reader_support = True
            self.reader = ArrayGroup.from_netcdf
        elif self.return_type == "xarray":
            self.multifile_reader_support = False
            self.reader = xarray.open_dataset
        else:
            raise ValueError("Unknown return type '%s'!" % return_type)

    def get_info(self, filename, **kwargs):
        """

        Args:
            filename:

        Returns:

        """
        if self.info_reader is None:
            raise NotImplementedError(
                "The NetCDF4 file handler does not have a native get_info "
                "support. You have to define one via 'info_reader' during "
                "initialization.")
        else:
            # Get info parameters from a file (time coverage, etc)
            return super(NetCDF4, self).get_info(filename, **kwargs)

    def read(self, filename, fields=None):
        """Reads and parses NetCDF files and load them to an ArrayGroup.

        If you need another return value, change it via the parameter
        *return_type* of the :meth:`__init__` method.

        Args:
            filename: Path and name of the file to read. If *return_type* is
                *ArrayGroup*, this can also be a tuple/list of file names.
            fields: (optional) List of field names that should be read. The
                other fields will be ignored.

        Returns:
            An ArrayGroup object.
        """

        if "fields" in signature(self.reader).parameters:
            ds = self.reader(filename, fields)
        else:
            ds = self.reader(filename)
            if fields is not None:
                ds = ds[fields]
        return ds

    def write(self, filename, data, **kwargs):
        """ Writes a data object to a NetCDF file.

        The data object must have a *to_netcdf* method, e.g. as an ArrayGroup
        or xarray.Dataset object.
        """

        if len(signature(data.to_netcdf).parameters) == 2:
            data.to_netcdf(filename)
        else:
            data.to_netcdf(filename, **kwargs)


# class Numpy(handlers.FileHandler):
#     def __init__(self, **kwargs):
#         # Call the base class initializer
#         super().__init__(**kwargs)
#
#     def get_info(self, filename):
#         # Get info parameters from a file (time coverage, etc)
#         ...
#
#     def read(self, filename, fields=None):
#         """ Reads and parses files with numpy arrays and load them to a xarray.
#
#         See the base class for further documentation.
#         """
#         numpy_data = np.load(filename)
#         print(numpy_data.keys())
#         data = xarray.Dataset.from_dict(numpy_data)
#
#         return data
#
#     def write(self, filename, data):
#         """ Writes a xarray to a NetCDF file.
#
#         See the base class for further documentation.
#         """
#
#         # Data must be a xarray object!
#         data_dict = data.to_dict()
#         np.save(filename, data_dict)
#
#
# class Pickle(handlers.FileHandler):
#     def __init__(self, **kwargs):
#         # Call the base class initializer
#         super().__init__(**kwargs)
#
#     def get_info(self, filename):
#         # Get info parameters from a file (time coverage, etc)
#         ...
#
#     def read(self, filename, fields=None):
#         """ Reads and parses files with numpy arrays and load them to a xarray.
#
#         See the base class for further documentation.
#         """
#
#         with open(filename, 'rb') as file:
#             return pickle.load(file)
#
#     def write(self, filename, data):
#         """ Writes a xarray to a NetCDF file.
#
#         See the base class for further documentation.
#         """
#
#         with open(filename, 'wb') as file:
#             pickle.dump(data, file)
#
#
# class XML(handlers.FileHandler):
#     def __init__(self, **kwargs):
#         # Call the base class initializer
#         super().__init__(**kwargs)
#
#     def get_info(self, filename):
#         # Get info parameters from a file (time coverage, etc)
#         ...
#
#     def read(self, filename, fields=None):
#         """ Reads and parses NetCDF files and load them to a xarray.
#
#         See the parent class for further documentation.
#         """
#         #
#         return typhon.arts.xml.load(filename)
#
#     def write(self, filename, data):
#         """ Writes a xarray to a NetCDF file.
#
#         See the base class for further documentation.
#         """
#
#         # Data must be a xarray object!
#         typhon.arts.xml.save(data, filename)