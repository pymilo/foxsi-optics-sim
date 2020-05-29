#!/usr/bin/env python
'''
Here we create a module, a detector, and multiple ray sources. We 
pass the generated rays through the module, to the detector, and c
generate a detector pixel plot showing us where the rays hit. Pixels
are colored based on which source the rays come from.

Created on Aug 15, 2011

@author: rtaylor
'''
from foxsisim.module import Module
from foxsisim.detector import Detector
from foxsisim.source import Source
import matplotlib.pyplot as plt
from foxsisim.plotting import plot

if __name__ == '__main__':

    # create module using defaults
    module = Module(conic=True)
    
    # create a detector located slightly in front of focal point
    detector = Detector(center=[0,0,228]) # focal point is at 230 by default
    
    # create a few sources of different types
    source1 = Source() # a white source 'at infinity' whose rays point perpendicular to module aperture
    
    source2 = Source(type='point',          # a point source
                     center=[10,10,-35000], # located at [x=10,y=10,z=-35000]
                     color=[1,0,0])         # and colored red
    
    source3 = Source(width=0.0001,          # a 1 micron
                     height=0.0001,         # by 1 micron
                     type='nonpoint',       # non-point source (a square region)
                     center=[5,-8,-20000],  # centered at [x=5,y=-8,z=20000]
                     color=[0,1,1])         # and colored light blue
    
    #  generate 500 rays from each source
    rays = source1.generateRays(module.targetFront,500)
    rays.extend(source2.generateRays(module.targetFront,500))
    rays.extend(source3.generateRays(module.targetFront,500))
    
    # pass rays through module
    module.passRays(rays, robust=True)
    
    # catch rays at detector
    detector.catchRays(rays)
    
    # plot detector pixels
    plot(detector)
    
    # show
    plt.show(block=True)
