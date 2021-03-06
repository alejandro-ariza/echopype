"""
This file provides a wrapper for the process object and functions.
Users will not need to know the names of the specific objects they need to create.
"""
import os
import xarray as xr
from echopype.process.azfp import ProcessAZFP
from echopype.process.ek60 import ProcessEK60
from echopype.process.ek80 import ProcessEK80


def Process(nc_path):
    """
    Provides data analysis and computation tools for sonar data in netCDF form.

    Parameters
    ----------
    nc_path : str
        The path to a .nc or .zarr file generated by `echopype`

    Returns
    -------
        Returns a specialized Process object depending on
        the type of echosounder the .nc file was produced with
    """

    fname = os.path.basename(nc_path)
    _, ext = os.path.splitext(fname)

    if fname.endswith('.nc'):
        open_dataset = xr.open_dataset
    elif fname.endswith('.zarr'):
        open_dataset = xr.open_zarr
    else:
        raise ValueError(f"{ext} is not a valid file format.")

    # Open nc file in order to determine what echosounder produced the original dataset
    with open_dataset(nc_path) as nc_file:
        try:
            echo_type = nc_file.keywords
        except AttributeError:
            raise ValueError("This file is incompatible with echopype functions.")

    # Returns specific Process object
    if echo_type == "EK60":
        return ProcessEK60(nc_path)
    elif echo_type == "EK80":
        return ProcessEK80(nc_path)
    elif echo_type == "AZFP":
        return ProcessAZFP(nc_path)
    else:
        raise ValueError("Unsupported file type")
