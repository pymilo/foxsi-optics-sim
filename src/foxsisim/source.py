'''
Created on Jul 11, 2011

@author: rtaylor
'''
from foxsisim.plane import Plane
from foxsisim.ray import Ray
import numpy as np
from numpy.linalg import norm
from random import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from foxsisim.mymath import genCustomRands
from scipy.integrate import quad

dt = np.dtype('f8')


class Source(Plane):
    '''
    Rays are cast from this source to a target region, usually the front end of
    a module object. The source object can be one of three types: 'atinf'
    (source 'at infinity' projecting parallel rays), 'point' (a point at some
    real coordinate in 3-space), and 'nonpoint' (a rectangle centered at some
    real coordinate in 3-space).
    '''

    def __init__(self,
                 center=[0, 0, -10],
                 width=10.302,  # 2*5.151 (max radius of default module)
                 height=10.302,
                 normal=[0, 0, 1],
                 type='atinf',
                 color=[1, 1, 1],
                 pixels=None,
                 spectrum=None
                 ):
        '''
        Constructor

        Parameters:
            center:    the center location of the source
            width:     the width of the projection rectangle (atinf or nonpoint)
            height:    the height of the projection rectangle (atinf or nonpoint)
            normal:    direction the projection rectangle is facing
            type:      'atinf', 'point', or 'nonpoint'
            color:     color of projected rays
            pixels:    optional numpy array of pixel colors (W x H x 3)
            spectrum:  optional numpy array (2xN) of energy spectrum
        '''
        # normal should be length 1
        normal = normal / norm(normal)

        # check type
        if type not in ['atinf', 'point', 'nonpoint']:
            raise ValueError('invalid source type')

        # check dims
        if type is not 'point' and (width <= 0 or height <= 0):
            raise ValueError('atinf or nonpoint source must have positive area')

        # create rectangular dimensions
        if normal[0] == 0 and normal[2] == 0:  # normal is in y direction
            sign = normal[1]  # 1 or -1
            ax1 = sign * np.array((0, 0, width), dt)
            ax2 = sign * np.array((0, height, 0), dt)
        else:
            ax1 = np.cross([0, 1, 0], normal)  # parallel to xz-plane
            ax2 = height * np.cross(normal, ax1)
            ax1 *= width

        # calc origin
        origin = np.array(center) - (0.5 * ax1 + 0.5 * ax2)

        # instantiate
        Plane.__init__(self, origin, ax1, ax2)
        self.center = np.array(center, dt)
        self.type = type
        self.color = np.array(color, np.dtype('f4'))
        self.pixels = pixels
        self._spectrum = spectrum
        self._maximum_energy = 1000  # this is the maximum energy considered

    def loadImage(self, file=None):
        '''
        Loads an image file and stores the pixel values into source (tested with png).
        Passing None as the file name removes any previously loaded pixels.
        '''
        if file is None:
            self.pixels = None
        else:
            self.pixels = mpimg.imread(file)

    def plotImage(self, figureNum=1):
        '''
        Displays the source background to screen
        In case you loaded an Image as your source
        '''
        plt.figure(figureNum)
        plt.imshow(self.pixels)

    def loadSpectrum(self, spectrum):
        '''Loads a function, f(energy_keV), as the energy spectrum
            for the source
        '''
        if not hasattr(spectrum, '__call__'):
            raise ValueError("Spectrum must be a function, f(energy_keV)")
        # normalize the spectrum function in case it is not already
        norm_factor = quad(spectrum, 0, self._maximum_energy)
        self._spectrum = lambda x: 1 / norm_factor[0] * spectrum(x)

    def colorAtPoint(self, points):
        '''
        Returns the rgb colors for a list of points. Assumes
        each point exists on the source surface.
        '''
        colors = np.zeros((len(points), 3), np.dtype('f4'))

        # if solid color
        if self.pixels is None:
            for i in range(len(points)):
                colors[i, :] = self.color
            return self.color

        # unit vectors of axes
        len1 = norm(self.ax1)
        len2 = norm(self.ax2)
        unit1 = self.ax1 / len1
        unit2 = self.ax2 / len2

        for i in range(len(points)):

            # find pixel
            disp = points[i] - self.origin
            scale1 = np.dot(disp, unit1) / len1  # length ratio of projection to ax1
            scale2 = np.dot(disp, unit2) / len2  # length ratio of projection to ax2
            xpix = self.pixels.shape[1] * scale1
            ypix = self.pixels.shape[0] * (1 - scale2)
            colors[i, :] = self.pixels[ypix, xpix, :]

        # return color
        return colors

    def generateRays(self, targetFunc, n, grid=None):
        '''
        Returns an array of rays, located at a source and pointed to valid
        target points (on a module/shell/segment).

        Parameters:
            targetFunc:    a function that generates points on the target plane
                           (ex: module.targetFront)
            n:             the number of random rays to generate
            grid:          the dimensions of a grid of points to generate
                           (alternative to specifying n)
        '''
        # create rays array
        if grid is None:
            nRays = n
            a = [random() for i in range(n)]  # @UnusedVariable
            b = [random() for i in range(n)]  # @UnusedVariable
        else:
            nRays = grid[0] * grid[1]
            rows = np.linspace(0, 1, grid[0])
            cols = np.linspace(0, 1, grid[1])
            a, b = [], []
            for r in rows:
                for c in cols:
                    a.append(r)
                    b.append(c)
        rays = [Ray() for i in range(nRays)]  # @UnusedVariable

        # source is at infinity
        if self.type == 'atinf':

            # create rays with ori=normal
            srcPnts = self.grid(a, b)
            normal = self.getNormal(0, 0)
            for i, ray in enumerate(rays):
                ray.pos = srcPnts[i, :]
                ray.ori = normal
                ray.src = ray.pos
                ray.hist.append(ray.pos)

        # source is a point
        elif self.type == 'point':

            # connect each with point source
            targPnts = targetFunc(a, b)
            for i, ray in enumerate(rays):
                ray.pos = self.center
                ray.ori = targPnts[i, :] - self.center
                ray.ori = ray.ori / norm(ray.ori)
                ray.src = ray.pos
                ray.hist.append(ray.pos)

        # source is a nonpoint (has thickness)
        elif self.type == 'nonpoint':
            if grid is None:
                # randomly generate points at source and target
                sa = [random() for i in range(n)]  # @UnusedVariable
                sb = [random() for i in range(n)]  # @UnusedVariable
                srcPnts = self.grid(sa, sb)
                targPnts = targetFunc(a, b)
            else:
                # generate target points
                targPnts = targetFunc(a, b)

                # map target points to source (assumes source is more
                # or less rectangular and facing the target region)
                print('warning: usability of grid ray generation untested for nonpoint source!')
                srcPnts = np.zeros(targPnts.shape, dt)
                rng0 = self.grid([0], [0])
                rng1 = self.grid([1], [1])
                srcX = (rng0[0, 0], rng1[0, 0])  # range of source x values
                srcY = (rng0[0, 1], rng1[0, 1])  # range of source y values
                srcZ = (rng0[0, 2], rng1[0, 2])  # range of source z values

                # range of target x values
                targX = (min(targPnts[:, 0]), max(targPnts[:, 0]))
                # range of target y values
                targY = (min(targPnts[:, 1]), max(targPnts[:, 1]))
                # range of target z values
                targZ = (min(targPnts[:, 2]), max(targPnts[:, 2]))
                srcXdiff = srcX[1] - srcX[0]
                srcYdiff = srcY[1] - srcY[0]
                srcZdiff = srcZ[1] - srcZ[0]
                targXdiff = targX[1] - targX[0]
                targYdiff = targY[1] - targY[0]

                for i in range(srcPnts.shape[0]):
                    srcPnts[i, 0] = srcX[0] + srcXdiff * (targPnts[i][0] - targX[0]) / targXdiff
                    srcPnts[i, 1] = srcY[0] + srcYdiff * (targPnts[i][1] - targY[0]) / targYdiff
                    srcPnts[i, 2] = srcZ[0] + srcZdiff * (targPnts[i][2] - targZ[0])

            # create rays
            for i, ray in enumerate(rays):
                ray.pos = srcPnts[i, :]
                ray.ori = targPnts[i, :] - ray.pos
                ray.ori = ray.ori / norm(ray.ori)
                ray.src = ray.pos
                ray.hist.append(ray.pos)

        else:
            raise ValueError('invalid source type')

        # tag the rays as coming from this source
        for i, ray in enumerate(rays):
            ray.tag = self
            ray.num = i

        # add energies to rays
        if self._spectrum is not None:
            energies = genCustomRands(self._spectrum, len(rays))
            for energy, ray in zip(energies, rays):
                ray.energy = energy

        return rays
