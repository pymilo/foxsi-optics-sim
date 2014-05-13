#!/usr/bin/env python
'''
Here we create a 7 shell module, plot its cross section, and plot a 3D 
representation. Note: the 3D representation uses polygons to construct 
the module shells (but within the software, the shells are constructed 
mathematically to have perfect curvature).

Created on Aug 15, 2011

@author: rtaylor
'''
from foxsisim.module import Module
from foxsisim.plotting import get3dAxes
import matplotlib.pyplot as plt

if __name__ == '__main__':

    # module parameters
    focalLength = 200.0
    segmentLength = 30.0
    radii = [5.15100, 4.90000, 4.65900, 4.42900, 4.21000, 4.00000, 3.79900]  # 7 shell radii

    # create module
    module = Module(seglen=segmentLength, focal=focalLength, radii=radii)

    # generate cross section
    fig1 = plt.figure(figsize=(9, 3))
    axes1 = fig1.gca()
    module.plot2D(axes1, 'b')

    # generate 3d representation
    fig2 = plt.figure(figsize=(5, 5))
    axes2 = get3dAxes(fig2)
    module.plot3D(axes2, 'b')

    # show figures
    plt.show()
