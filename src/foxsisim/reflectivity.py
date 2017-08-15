'''
Created on 2014

@author: StevenChriste
'''


from __future__ import absolute_import

__all__ = ["Reflectivity"]

import numpy as np
import glob
import re
from scipy.interpolate import interp2d
import os
import foxsisim
import h5py


class Reflectivity:
    """Provides reflectivities as a function of angle (in degrees) and energy
        (in keV)"""
    def __init__(self, material='Ir'):
        path = os.path.dirname(foxsisim.__file__) + '/data/'
        h = h5py.File(os.path.join(path, "reflectivity_data.hdf5"), 'r')
        self.data = h['reflectivity/' + material.lower()][:]
        self.energy_ax = h['energy'][:]
        self.angle_ax = h['angle'][:]
        self.material = material
        self.func = interp2d(self.angle_ax, self.energy_ax, self.data, kind='cubic')

    def energy_range(self):
        """Return the valid range of energies"""
        return np.array([self.energy_ax.min(), self.energy_ax.max()])

    def angle_range(self):
        """Return the valud range of angles"""
        return np.array([self.angle_ax.min(), self.angle_ax.max()])
