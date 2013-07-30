#!/usr/bin/env python
'''
Here we place a 'nonpoint' source where the detector normally would
be, placing the detector instead facing towards the wide end of the
module. The nonpoint source then randomly sends rays through the
'wrong' end of the module. The detector catches some of these, and
the generated image is displayed.

Created on Aug 15, 2011

@author: rtaylor
'''
from foxsisim.module import Module
from foxsisim.detector import Detector
from foxsisim.source import Source
import matplotlib.pyplot as plt

if __name__ == '__main__':

    # create module using defaults
    module = Module()
    
    # create large detector facing aperture
    detector = Detector(center=[0,0,-100], normal=[0,0,1], width=50, height=50)
    
    # create a nonpoint source replacing the detector
    source = Source(center=[0,0,230], normal=[0,0,-1], width=2, height=2, type='nonpoint')
    
    #  generate 1000 rays at source and target them towards the **backend** of module
    rays = source.generateRays(module.targetBack, 1000)
    
    # simulate
    module.passRays(rays)
    detector.catchRays(rays)
    
    # plot detector pixels
    fig1 = plt.figure(figsize=(5,5))
    axes1 = fig1.gca()
    detector.plotImage(axes1)

    # show
    plt.show()
