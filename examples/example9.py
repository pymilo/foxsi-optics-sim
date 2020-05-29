#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import numpy.random
from foxsisim.module import Module
from foxsisim.detector import Detector
from foxsisim.source import Source
from foxsisim.plotting import plot

if __name__ == '__main__':

    tstart = datetime.now()
    # spectrum = lambda x: np.exp(-x)
    max_energy = 30.0
    min_energy = 1.0
    nrays = 500

    energies = numpy.random.rand(nrays) * (max_energy - min_energy) + min_energy
    source_distance = 1e4
    source = Source(type='point', center=[0, 0, -source_distance], color=[1, 0, 0], spectrum=energies)

    radii = [5.15100, 4.90000, 4.65900, 4.42900, 4.21000, 4.00000, 3.79900]  # 7 shell radii
    seglen = 30
    base = [0, 0, 0]
    focal_length = 200
    module = Module(radii=radii, seglen=seglen, base=base, angles=None, focal=focal_length, conic=True)

    detector = Detector(center=[0, 0, 230])  # focal point is at 230 by default

    #  generate nrays from the source
    rays = source.generateRays(module.targetFront, nrays)

    plt.figure()
    plt.hist([ray.energy for ray in rays], normed=True, label='generated rays')
    plt.legend()
    plt.show(block=True)

    # pass rays through module
    module.passRays(rays, robust=True)

    # catch rays at detector
    detector.catchRays(rays)

    rays_on_detector = len(detector.rays)

    plot(detector, energy_range=[0, 15])
    plt.show(block=True)

    print('Number of rays on Detector ' + str(rays_on_detector))
    print('Time total: ' + str((datetime.now() - tstart).seconds) + ' seconds')
    print('Time per ray (s): ' +
          str(rays_on_detector / float((datetime.now() - tstart).seconds)))
