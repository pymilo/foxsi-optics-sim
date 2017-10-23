from foxsisim.module import Module
from foxsisim.detector import Detector
from foxsisim.source import Source
from foxsisim.plotting import scatterHist
from foxsisim.plotting import plot

import matplotlib.pyplot as plt

if __name__ == '__main__':

    # create module/detector/source objects using defaults
    module = Module()
    detector = Detector(tag='Det')
    source = Source(tag='Source')

    # generate 1000 rays at source
    rays = source.generateRays(module.targetFront, 1000)

    # pass rays through module
    module.passRays(rays, robust=True)

    # catch rays at detector
    detector.catchRays(rays)
    for ray in rays:
        print("{0} {1} {2}".format(ray.bounces, ray.dead, ray.tag))