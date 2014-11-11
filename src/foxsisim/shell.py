'''
Created on Jul 11, 2011

@author: rtaylor
'''
from segment import Segment
from segmentp import Segmentp
from segmenth import Segmenth

from math import tan, pi


class Shell:
    '''
    A shell consists of two segments, one in the front and one behind.
    The base location of the front segment has a smaller z value than that
    of the back segement. Thus, rays coming from sources in the negative 
    z range will enter the front end first.
    '''

    def __init__(self,
                 base=[0, 0, 0],
                 seglen=30.0,
                 ang=0.00643732691573,  # focal length of 2m
                 r=5.151,
                 focal=200.0, conic=False):
        '''
        Constructor

        Parameters:
            base:    the center point of the wide end of the segment
            seglen:  the axial length of each segment
            ang:     angle between the shell axis and the side of the front
                     segment
            r:       radius of the shell where the two segments meet
        '''
        if conic is False:
            # Paraboloid segment
            self.front = Segmentp(base=base, focal=focal, seglen=seglen, ang=ang, r1=r)
            backBase = [base[0], base[1], base[2] + seglen]
            # Hyperboloid segment
            self.back = Segmenth(base=backBase, focal=focal, seglen=seglen, ang=ang, r0=r)
        else:
            self.front = Segment(base=base, seglen=seglen, ang=ang, r1=r)
            backBase = [base[0], base[1], base[2]+seglen]
            self.back = Segment(base=backBase, seglen=seglen, ang=3*ang, r0=r)

    def getSurfaces(self):
        '''
        Returns a list of surfaces
        '''
        return [self.front, self.back]

    def plot2D(self, axes, color='b'):
        '''
        Plots a 2d cross section of the shell
        '''
        self.front.plot2D(axes, color)
        self.back.plot2D(axes, color)

        # plot rays
        ang = self.front.ang
        r = self.back.r1
        z = self.back.base[2]
        d = r * tan((pi / 2) - 4 * ang)
        axes.plot((2 * z, 2 * z + d), (r, 0), 'y:')
        axes.plot((2 * z, 2 * z + d), (-r, 0), 'y:')

    def plot3D(self, axes, color='b'):
        '''
        Generates a 3d plot of the shell in the given figure
        '''
        self.front.plot3D(axes, color)
        self.back.plot3D(axes, color)

    def targetFront(self, a, b):
        '''
        Takes two list arguments of equal size, the elements of which range
        from 0 to 1. Returns an array of points that exist on the circle
        defined by the wide end of the shell.
        '''
        return self.front.targetFront(a, b)

    def targetBack(self, a, b):
        '''
        Takes two list arguments of equal size, the elements of which range
        from 0 to 1. Returns an array of points that exist on the circle
        defined by the small end of the shell.
        '''
        return self.back.targetBack(a, b)