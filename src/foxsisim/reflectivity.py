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


class Reflectivity:
    """Provides reflectivities as a function of angle (in degrees) and energy
        (in keV)"""
    def __init__(self, material='Ni'):
        path = os.path.dirname(foxsisim.__file__) + '/data/'
        files = glob.glob(path + "*.txt")
        data = np.loadtxt(files[0], skiprows=2)
        energy = int(re.findall(r"\D(\d{2})\D", files[0])[0])
        energy_ax = []
        energy_ax.append(energy)
        angle_ax = data[:, 0]
        reflectivities = np.zeros((len(files), len(data[:, 1])))
        reflectivities[0, :] = data[:, 1]
        for i, this_file in enumerate(files[1:]):
            energy = int(re.findall(r"\D(\d{2})\D", this_file)[0])
            energy_ax.append(energy)
            data = np.loadtxt(this_file, skiprows=2)
            reflectivities[i, :] = data[:, 1]

        self.energy_ax = np.array(energy_ax)
        self.angle_ax = np.array(angle_ax)

        self.material = material
        self.func = interp2d(self.angle_ax, self.energy_ax, reflectivities, kind='cubic')

    def energy_range(self):
        """Return the valid range of energies"""
        return np.array([self.energy_ax.min(), self.energy_ax.max()])

    def angle_range(self):
        """Return the valud range of angles"""
        return np.array([self.angle_ax.min(), self.angle_ax.max()])
