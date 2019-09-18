'''
Created on Jul 8, 2011

@author: rtaylor
'''
import numpy as np
from numpy.linalg import norm

class Surface:
    '''
    A surface in 3-space defined by a set of parametric equations. Inherited by
    other classes like plane and segment. Provides methods for calculating points
    and normals at parameters u and v.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.tag = 'Surface'
        pass

    def inRange(self,u,v):
        '''
        Are the u and v parameters in the desired range?
        '''
        return True

    def existsInOctant(self,octant):
        '''
        Returns whether the surface exists in the supplied octant ***OUTDATED***
        '''
        return False

    def rayIntersect(self, ray):
        '''
        Returns the first intersection of a ray with the surface
        in parametric form (u,v,t) if such a solution exists.
        Otherwise, returns None.
        '''
        return None

    def x(self,u,v):
        '''
        Parametric equation for x
        '''
        return 0

    def y(self,u,v):
        '''
        Parametric equation for y
        '''
        return 0

    def z(self,u,v):
        '''
        Parametric equation for z
        '''
        return 0

    def du(self,u,v):
        '''
        First partial derivative with respect to u
        '''
        return np.array((0,0,0))

    def dv(self,u,v):
        '''
        First partial derivative with respect to v
        '''
        return np.array((0,0,0))

    def getPoint(self,u,v):
        '''
        Returns a point for parameters u and v
        '''
        return np.array((self.x(u,v),self.y(u,v),self.z(u,v)))

    def getNormal(self,u,v):
        '''
        Returns the unit normal for parameters u and v
        '''
        cross = np.cross(self.du(u,v),self.dv(u,v))
        return cross / norm(cross)
