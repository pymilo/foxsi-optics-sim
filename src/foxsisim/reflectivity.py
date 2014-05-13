from __future__ import absolute_import

__all__ = ["Reflectivity"]

import numpy as np
import glob
import re
from scipy.interpolate import griddata
import os
import foxsisim


class Reflectivity:
    """Provides reflectivities as a function of angle (in degrees) and energy
        (in keV)"""
    def __init__(self, material='Ni'):
        path = os.path.dirname(foxsisim.__file__) + '/data/'

        files = glob.glob(path + "*.txt")
        # todo: read the energies from the files
        data = np.loadtxt(files[0], skiprows=2)
        energy = int(re.findall(r"\D(\d{2})\D", files[0])[0])
        points = np.column_stack([np.ones(data.shape[0]) * energy, data[:, 0]])
        values = data[:, 1]

        for this_file in files[1:]:
            data = np.loadtxt(this_file, skiprows=2)
            energy = int(re.findall(r"\D(\d{2})\D", this_file)[0])
            new_points = np.column_stack([np.ones(data.shape[0]) * energy,
                                          data[:, 0]])
            points = np.vstack([points, new_points])
            values = np.hstack([values, data[:, 1]])
        self._points = points
        self._values = values
        self.material = material

    def value(self, energy, angle):
        """Given an energy (in keV) and an angle (in degrees) return the
        reflectivity"""
        return np.power(10, griddata(self._points, np.log(self._values),
                                     (energy, angle)))

    def energy_range(self):
        """Return the valid range of energies"""
        return np.array([self._points[:, 0].min(), self._points[:, 0].max()])

    def angle_range(self):
        """Return the valud range of angles"""
        return np.array([self._points[:, 1].min(), self._points[:, 1].max()])