# June 2014, @milo & @Steven 
''' Example 2 using the geometry of the Hyp and Par. This should show
perfect focusing with all rays falling in a point.'''

from foxsisim.module import Module
from foxsisim.detector import Detector
from foxsisim.source import Source
from foxsisim.plotting import scatterHist
from foxsisim.plotting import plot

import matplotlib.pyplot as plt

if __name__ == '__main__':

    # create module/detector/source objects using defaults
    module = Module()
    detector = Detector()
    source = Source()

    # generate 1000 rays at source
    rays = source.generateRays(module.targetFront, 1000)

    # pass rays through module
    module.passRays(rays, robust=True)

    # catch rays at detector
    detector.catchRays(rays)

    # plot detector pixels
    plot(detector)
    
    # create scatter plot
    detectorRays = detector.rays
    fig2 = plt.figure(figsize=(5,5))
    scatterHist(detectorRays,fig2)

    # show
    plt.show()

