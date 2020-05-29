"""
Created on Jun, 2020

@author: milo
"""
from foxsisim.plane import Plane
import numpy as np
from numpy.linalg import norm

dtf = np.dtype('f8')


class Annulus(Plane):
    """
    An annular surface defined by an origin point, a normal, a radius, and a thickness.
    """

    def __init__(self, center=[0, 0, 0], normal=[0, 0, 1], radius=1, thickness=0.025):
        """
        Constructor

        Parameters:
            center:     center location of circle
            normal:     surface normal of circle
            radius:     radius of sieve
            thickness:  thickness of sieve
        """
        # normal should be length 1
        normal = normal / norm(normal)

        # create rectangular dimensions
        if normal[0] == 0 and normal[2] == 0:  # normal is in y direction
            sign = normal[1]  # 1 or -1
            ax1 = sign * np.array((0, 0, 1), dtf)
            ax2 = sign * np.array((0, 1, 0), dtf)
        else:
            ax1 = np.cross([0, 1, 0], normal)  # parallel to xz-plane
            ax2 = np.cross(normal, ax1)

        Plane.__init__(self, origin=center, ax1=ax1, ax2=ax2)
        self.center = np.array(center, dtf)
        self.normal = np.array(normal, dtf)
        self.radius = radius
        self.thickness = thickness

    def inRange(self, u, v):
        """
        Are the u and v parameters in the desired range?
        """
        if (self.radius <= norm(self.getPoint(u, v) - self.center) <= (self.radius + self.thickness)):
            return True
        else:
            return False
