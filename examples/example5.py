#!/usr/bin/env python
'''
Here, instead of passing rays through a complete module, we only 
pass them through a single shell, catching them on the other side 
with a normal detector.

Created on Aug 15, 2011

@author: rtaylor
'''
from foxsisim.shell import Shell
from foxsisim.detector import Detector
from foxsisim.source import Source
from foxsisim.plotting import scatterHist
from foxsisim.mymath import reflect
import matplotlib.pyplot as plt
from numpy.linalg import norm

if __name__ == '__main__':

    # create default shell/detector/source
    shell = Shell()
    detector = Detector()
    source = Source()
    
    # generate 500 rays pointing at shell
    rays = source.generateRays(shell.targetFront, 500)
    
    # pass rays through shell
    surfaces = shell.getSurfaces() # each shell has two segments
    for ray in rays:
        while True:
            
            sol = None
            for surface in surfaces:
                
                # solve for intersection of ray with surface
                sol = surface.rayIntersect(ray)
                if sol is not None: break
            
            # if ray hits reflective surface
            if sol is not None:
                
                # update ray
                ray.pos = ray.getPoint(sol[2])
                ray.bounces += 1
                x = reflect(ray.ori,surface.getNormal(sol[0],sol[1]))
                # if reflected
                if x is not None:
                    ray.ori = x / norm(x) # update ori to unit vector reflection
                # otherwise, no reflection means ray is dead
                else:
                    ray.dead = True 
                    break
                
            else: break
    
    # catch rays as detector
    detector.catchRays(rays)

    # scatter plot
    detectorRays = detector.rays 
    fig = plt.figure(figsize=(5,5))
    scatterHist(detectorRays,fig)
        
    # show
    plt.show()
