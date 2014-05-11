'''
Created on Jul 27, 2011

@author: rtaylor
'''
from plane import Plane
import numpy as np
from numpy.linalg import norm

dtf = np.dtype('f8')


class Circle(Plane):
    '''
    A circular surface defined by an origin point, a normal, and a radius.
    '''

    def __init__(self, center=[0, 0, 0], normal=[0, 0, 1], radius=1):
        '''
        Constructor

        Parameters:
            center: center location of circle
            normal: surface normal of circle
            radius: radius of circle
        '''
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

    def inRange(self, u, v):
        '''
        Are the u and v parameters in the desired range?
        '''
        if norm(self.getPoint(u, v) - self.center) <= self.radius:
            return True
        else:
            return False

    def plot3D(self, axes, color='b'):
        '''
        Generates a 3d plot of the plane in the given figure
        '''
        pass
