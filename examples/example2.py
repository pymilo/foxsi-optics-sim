#!/usr/bin/env python
'''
Here we create a module, a detector, and an 'atinf' ray source. Then
we generate rays at the source, pass them through the module and catch
them with the detector. After catching them we create a scatter plot,
showing us the source's point spread function. Points in the scatter
plot are colored based on how many times the corresponding ray bounced
in the module (green => once, blue => twice).

Created on Aug 15, 2011

@author: rtaylor
'''
from foxsisim.module import Module
from foxsisim.detector import Detector
from foxsisim.source import Source
from foxsisim.plotting import scatterHist
import matplotlib.pyplot as plt

if __name__ == '__main__':

    # create module/detector/source objects using defaults
    module = Module()
    detector = Detector()
    source = Source()
    
    #  generate 1000 rays at source
    rays = source.generateRays(module.targetFront, 1000)
    
    # pass rays through module
    module.passRays(rays, robust=True)
    
    # catch rays at detector
    detector.catchRays(rays)
    
    # plot detector pixels
    fig1 = plt.figure(figsize=(5,5))
    axes1 = fig1.gca()
    detector.plotImage(axes1)

    # create scatter plot
    detectorRays = detector.rays # detector does not necessarily catch all rays, so it stores its own list 
    fig2 = plt.figure(figsize=(5,5))
    scatterHist(detectorRays,fig2)
        
    # show
    plt.show()
