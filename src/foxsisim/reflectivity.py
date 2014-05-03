from __future__ import absolute_import

__all__ = ["Reflectivity"]

import numpy as np
import glob
import re
from scipy.interpolate import griddata

class Reflectivity:
    """Provides reflectivities as a function of angle (in degrees) and energy (in keV)"""
    def __init__(self, material='Ni'):
        files = glob.glob("/Users/schriste/Dropbox/Developer/python/foxsi-optics-sim/src/foxsisim/data/*.txt")
        # todo: read the energies from the files
        data = np.loadtxt(files[0], skiprows = 2)
        angles = data[:,1]
        energy = int(re.findall(r"\D(\d{2})\D", files[0])[0])
        points = np.column_stack([np.ones(data.shape[0]) * energy, data[:,0]])
        values = data[:,1]
        
        for file in files[1:]:
            data = np.loadtxt(file, skiprows = 2)
            energy = int(re.findall(r"\D(\d{2})\D", file)[0])
            new_points = np.column_stack([np.ones(data.shape[0]) * energy, data[:,0]])
            points = np.vstack([points, new_points])
            values = np.hstack([values, data[:,1]])
        self.points = points
        self.values = values
                       
    def value(self, energy, angle):
        """Given an energy (in keV) and an angle (in degrees) return the reflectivity"""
        return np.power(10, griddata(self.points, np.log(self.values), (energy, angle)))