'''
Created on Jul 19, 2011

@author: rtaylor
'''
from plane import Plane
from source import Source
import numpy as np
from numpy.linalg import norm

dtf = np.dtype('f8')


class Detector(Plane):
    '''
    Detector object that catches rays that hit it's rectangular plane, and
    stores their colors in a pixel array.
    '''

    def __init__(self,
                 center=[0, 0, 230],
                 width=2,
                 height=2,
                 normal=[0, 0, 1],
                 reso=[256, 256],
                 pixels=None,
                 freqs=None,
                 ):
        '''
        Constructor

        Parameters:
            center:    the center location of the source
            width:     the width of the projection rectangle
            height:    the height of the projection rectangle
            normal:    direction the projection rectangle is facing
            reso:      resolution of pixels (W,H)
            pixels:    optional numpy array to hold pixel colors (W x H x 3)
            freqs:     optional array to count the number of times a pixel is
                       hit (W x H)
        '''
        # normal should be length 1
        normal = normal / norm(normal)

        # create rectangular dimensions
        if normal[0] == 0 and normal[2] == 0:  # normal is in y direction
            sign = normal[1]  # 1 or -1
            ax1 = sign * np.array((0, 0, width), dtf)
            ax2 = sign * np.array((0, height, 0), dtf)
        else:
            ax1 = np.cross([0, 1, 0], normal)  # parallel to xz-plane
            ax2 = height * np.cross(normal, ax1)
            ax1 *= width

        # calc origin
        origin = np.array(center) - (0.5 * ax1 + 0.5 * ax2)

        # instantiate
        Plane.__init__(self, origin, ax1, ax2)
        self.center = np.array(center, dtf)
        self.reso = reso
        self.pixels = pixels
        self.freqs = freqs
        self.rays = []

        # bring in pixels
        if pixels is None:
            self._initDetectorImage()
        elif freqs is None:
            raise ValueError('must pass freqs when passing pixels')
        elif pixels.shape[0:2] != freqs.shape:
            raise ValueError('pixels and freqs arrays do not correspond')

    def plotSpectrum(self, axes, dE=1, range=[0, 20]):
        '''
        Plot the spectrum of the rays in a region of interest (if available,
        not yet implemented) or across the entire detector
        '''
        energies = [ray.energy for ray in self.rays]
        axes.hist(energies, bins=(range[1] - range[0]) / dE, range=range)
        axes.set_xlabel("Energy [keV]")
        axes.set_title("Detector Spectrum N = " + str(len(energies)))

    def _initDetectorImage(self):

        # rgb colors in float form
        pixels = np.zeros((self.reso[0], self.reso[1], 3), np.dtype('f4'))
        # number of times a pixel is hit by a ray
        freqs = np.zeros(self.reso, np.dtype('u4'))
        self.pixels = pixels
        self.freqs = freqs

    def catchRays(self, rays):
        '''
        Takes an array of rays and tests each for collision with the detector
        plane. If the ray collides, the corresponding pixel in the detector is
        colored. The attribute 'freqs' counts the number of times a pixel is
        hit.
        '''

        # for each ray
        for ray in rays:
            # if ray hasn't hit anything yet
            if not ray.dead:
                # test intersection with detector
                sol = self.rayIntersect(ray)
                if sol is not None:
                    # update ray attributes
                    ray.pos = ray.getPoint(sol[2])
                    ray.des = ray.pos
                    ray.dead = True
                    ray.bounces += 0
                    ray.hist.append(ray.pos)
                    self.rays.append(ray)

    def _makeImage(self, energy_range=None):
        '''
        Bin the rays that were caught by the detector to make an image
        '''
        # vars
        dims = self.pixels.shape
        colorSum = np.zeros(dims, np.dtype('f4'))
        counts = np.zeros(dims[0:2], np.dtype('u4'))
        len1 = norm(self.ax1)  # length of rectangle side 1
        len2 = norm(self.ax2)  # length of rectangle side 2
        unit1 = self.ax1 / len1  # ax1 unit vector
        unit2 = self.ax2 / len2  # ax2 unit vector

        self._initDetectorImage()

        for ray in self.rays:
            # find pixel
            disp = ray.pos - self.origin
            # length ratio of projection to ax1
            scale1 = np.dot(disp, unit1) / len1
            # length ratio of projection to ax2
            scale2 = np.dot(disp, unit2) / len2
            xpix = dims[1] * scale1
            ypix = dims[0] * (1 - scale2)

            # get color
            if isinstance(ray.tag, Source):
                colorSum[ypix, xpix, :] += ray.tag.colorAtPoint([ray.src])
            else:
                colorSum[ypix, xpix, :] += np.array((1, 1, 1))  # assume white

            if energy_range is not None:
                if ((ray.energy < energy_range[1]) &
                    (ray.energy > energy_range[0])):
                    counts[ypix, xpix] += 1
            else:
                counts[ypix, xpix] += 1

        # average the colors
        for x in range(dims[0]):
            for y in range(dims[1]):
                if counts[x, y] > 0:
                    # total = self.freqs[x,y] + counts[x,y]
                    # self.pixels[x,y] = (self.freqs[x,y]*self.pixels[x,y]
                    # + colorSum[x,y]) / total
                    total = counts[x, y]
                    self.pixels[x, y] = colorSum[x, y] / total
                    self.freqs[x, y] = total
