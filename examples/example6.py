import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

from foxsisim.module import Module
from foxsisim.detector import Detector
from foxsisim.source import Source
from foxsisim.plotting import plot

if __name__ == '__main__':

    tstart = datetime.now()

    source_distance = 1e4
    source = Source(type='point', center=[0, 0, -source_distance], color=[1, 0, 0])

    # spectrum = lambda x: np.exp(-x)
    max_energy = 30.0

    def spectrum(z):
        if (type(z) is not type([1])) and (type(z) is not type(np.array(1))):
            x = np.array([z])
        else:
            x = np.array(z)
        return np.piecewise(x, [x < 0, (x < max_energy) & (x > 0), (x >= max_energy)], [0, 1 / max_energy, 0])

    source.loadSpectrum(spectrum)
    plot(source)

    radii = [5.15100, 4.90000, 4.65900, 4.42900, 4.21000, 4.00000, 3.79900]  # 7 shell radii
    seglen = 30
    base = [0, 0, 0]
    focal_length = 200
    module = Module(radii=radii, seglen=seglen, base=base, angles=None, focal=focal_length)

    detector = Detector(center=[0, 0, 230])  # focal point is at 230 by default

    nrays = 500
#  generate nrays from the source
    rays = source.generateRays(module.targetFront, nrays)


    fig = plt.figure(figsize=(5, 5))
    plot(source)
    plt.hist([ray.energy for ray in rays], normed=True, label='generated rays')
    plt.legend()
    plt.show()

# pass rays through module
    module.passRays(rays, robust=True)

# catch rays at detector
    detector.catchRays(rays)

    rays_on_detector = len(detector.rays)

    plot(detector, energy_range=[0, 15])
    plt.show()

    print('Number of rays on Detector ' + str(rays_on_detector))
    print('Time total: ' + str((datetime.now() - tstart).seconds) + ' seconds')
    print('Time per ray (s): ' +
          str(rays_on_detector / float((datetime.now() - tstart).seconds)))
