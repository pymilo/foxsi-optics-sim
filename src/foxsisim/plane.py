'''
Created on Jul 27, 2011

@author: rtaylor
'''
from foxsisim.surface import Surface
import numpy as np
from numpy.linalg import norm

dt = np.dtype('f8')

class Plane(Surface):
    '''
    A parallelogram surface defined by two axis vectors and an origin point.
    '''

    def __init__(self, origin = [-1,-1,0], ax1 = [2,0,0], ax2 = [0,2,0]):
        '''
        Constructor

        Parameters:
            ax1:     first edge of parallelogram as a vector
            ax2:     second edge of parallelogram as a vector
            origin:  the origin coordinate for both axes
        '''
        Surface.__init__(self)
        self.origin = np.array(origin,dt)
        self.ax1 = np.array(ax1,dt)
        self.ax2 = np.array(ax2,dt)

    def x(self,u,v):
        '''
        Parametric equation for x
        '''
        return self.origin[0] + u*self.ax1[0] + v*self.ax2[0]

    def y(self,u,v):
        '''
        Parametric equation for y
        '''
        return self.origin[1] + u*self.ax1[1] + v*self.ax2[1]

    def z(self,u,v):
        '''
        Parametric equation for z
        '''
        return self.origin[2] + u*self.ax1[2] + v*self.ax2[2]

    def getPoint(self,u,v):
        '''
        Returns a point for parameters u and v
        '''
        return self.origin + u*self.ax1 + v*self.ax2

    def du(self,u,v):
        '''
        First partial derivative with respect to u
        '''
        return self.ax1

    def dv(self,u,v):
        '''
        First partial derivative with respect to v
        '''
        return self.ax2

    def getWidth(self):
        '''
        Returns the length of the parallelogram's first axis
        '''
        return norm(self.ax1)

    def getHeight(self):
        '''
        Returns the length of the parallelogram's second axis
        '''
        return norm(self.ax2)

    def inRange(self,u,v):
        '''
        Are the u and v parameters in the desired range?
        '''
        if u >= 0 and u <= 1 and v >= 0 and v <= 1:
            return True
        else: return False

    def rayIntersect(self, ray):
        '''
        Returns the first intersection of a ray with the surface
        in parametric form (u,v,t) if such a solution exists.
        Otherwise, returns None.
        '''
        a = np.transpose(np.array((self.ax1, self.ax2, -ray.ori),dt))
        b = np.transpose(ray.pos - self.origin)
        try: x = np.linalg.solve(a,b)
        except np.linalg.LinAlgError:
            # no solution exists (ray is parallel to plane)
            x = None
        if x is not None:
            if not self.inRange(x[0],x[1]):
                x = None
        return x

    def grid(self,a,b):
        '''
        Takes two list arguments of equal size, the elements of which range
        from 0 to 1. Returns an array of points that exist at the corresponding
        locations on the parallelogram.
        '''
        n = len(a)
        pnts = np.zeros((n,3),dt)
        for i in range(n): pnts[i,:] = self.getPoint(a[i],b[i])
        return pnts

    def plot3D(self, axes, color = 'b'):
        '''
        Generates a 3d plot of the plane in the given figure
        '''
        p1 = self.origin
        p2 = self.getPoint(1,0)
        p3 = self.getPoint(1,1)
        p4 = self.getPoint(0,1)
        axes.plot3D([p1[0],p2[0],p3[0],p4[0],p1[0]],
                    [p1[1],p2[1],p3[1],p4[1],p1[1]],
                    [p1[2],p2[2],p3[2],p4[2],p1[2]],
                    '-'+color)
