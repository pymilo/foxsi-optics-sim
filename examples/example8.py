from foxsisim.module import Module
from foxsisim.detector import Detector
from foxsisim.source import Source
from foxsisim.plotting import scatterHist
from foxsisim.plotting import plot
import numpy as np

if __name__ == '__main__':
    # create module of 7 shells
    module = Module(radii=[5.151, 3.799],
                    seglen=30.0,
                    base=[0,0,0],
                    focal=200,
                    angles=None,
                    conic=False)

    detector = Detector(width=0.96,
                        height=0.96,
                        normal=[0,0,1],
                        center=[0,0,200.0+30.0],
                        reso =[128,128])

    source_distance = -2187.5
    offaxis_angle_arcmin = 1.0
    source = Source(type='point',
                center=[ source_distance * np.sin(np.deg2rad(offaxis_angle_arcmin/60.0)) , 0.0 , source_distance ],
                color=[0,1,1])

    rays = source.generateRays(module.targetFront, 2000)
    module.passRays(rays, robust=True)
    detector.catchRays(rays)

    plot(detector)
    scatterHist(rays)