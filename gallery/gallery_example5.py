'''
Goal:

User Inputs:
              1. Number of rays.
              2. Path to the folder where to save the final figure.

Run:
        ipython gallery_example5.py

Output:
        An image saved as My_gallery_example5.png

Last update: Sep, 2019
'''

import numpy as np
from foxsisim.source import Source
from foxsisim.module import Module
from foxsisim.util import load_rays, save_rays
from foxsisim.detector import Detector

n = 100                ## number of rays
SaveFolder = './'      ## Path of the SaveFolder
Sdist = -1.5e13        ## cm
offaxisAngle = 0.0     ## arcmin

fbrs = np.arange(2.623,3.29,0.05) # Front blocker radius ranging from 2.623 cm to 3.273

#Create Source :
source = Source(type='point',center=[0, -Sdist * np.sin(np.deg2rad(offaxisAngle / 60.0)), Sdist ])

fbr = 2.8575
rbr = 0.00
offaxisAngles = np.arange(0.0,30.,2.) # Off-Axis Angles


F286_NR_All_Drays, F286_NR_All_Hrays, F286_NR_All_Prays = [], [], []
F286_NR_All_Dx, F286_NR_All_Dy, F286_NR_All_Hx, F286_NR_All_Hy, F286_NR_All_Px, F286_NR_All_Py = [], [], [], [], [], []


for fbr in fbrs:
    print('Front radius: %f' % fbr)
    module = Module(radii = [3.17], core_radius=(fbr,0.))
    rays = source.generateRays(module.targetFront,n)
    module.passRays(rays)
    rays = [ray for ray in rays if (ray.tag != 'Source')] #kills the passthrough rays


    # Create detector :
    detector = Detector(width=10,
                    height=10,
                    normal = [0,0,1],
                    center = [0,0,230],
                    reso = [1024,1024])
    # Detector Catch rays:
    detector.catchRays(Brays)

    '''Defining D, H, and P rays for each blocker size: '''
    Drays = [ray for ray in rays if (ray.des[2]==230.0 and abs(ray.des[1])<= 0.48 and abs(ray.des[0])<= 0.48 and ray.bounces ==2 )]
    Srays = [ray for ray in rays if (ray.des[2]==230.0 and abs(ray.des[1])<= 0.48 and abs(ray.des[0])<= 0.48 and ray.bounces ==1 )]
    Hrays = [ray for ray in rays if (ray.des[2]==230.0 and abs(ray.des[1])<= 0.48 and abs(ray.des[0])<= 0.48 and ray.bounces ==1 and ray.tag[-4:] == 'Hy-D' )]
    Prays = [ray for ray in rays if (ray.des[2]==230.0 and abs(ray.des[1])<= 0.48 and abs(ray.des[0])<= 0.48 and ray.bounces ==1 and ray.tag[-4:] == 'Pa-D' )]

    F286_NR_All_Drays.append(Drays)
    F286_NR_All_Hrays.append(Hrays)
    F286_NR_All_Prays.append(Prays)

    sim_scale = 1.0    # 1cm = 17.4 arcmin
    #sim_scale = 17.4    # 1cm = 17.4 arcmin

    #Hyperboloid
    Hx, Hy = [], []
    for ray in Hrays:
        Hx.append(ray.pos[0]*sim_scale)
        Hy.append(ray.pos[1]*sim_scale)
    F286_NR_All_Hx.append(Hx)
    F286_NR_All_Hy.append(Hy)

    # Paraboloid
    Px, Py = [], []
    for ray in Prays:
        Px.append(ray.pos[0]*sim_scale)
        Py.append(ray.pos[1]*sim_scale)
    F286_NR_All_Px.append(Px)
    F286_NR_All_Py.append(Py)

    # Double
    Dx, Dy = [], []
    for ray in Drays:
        Dx.append(ray.pos[0]*sim_scale)
        Dy.append(ray.pos[1]*sim_scale)
    F286_NR_All_Dx.append(Dx)
    F286_NR_All_Dy.append(Dy)


## Figure definition:
f, ax1 = plt.subplots(1, 1, sharex='col', sharey='row',figsize=(6,6))

## Front Blocker Doubles
ax1.set_title('Front blocker size dependance',fontsize=24)
ax1.plot(offaxisAngles, F286_NR_Doubles/max(np.array(F286_NR_Doubles)),'o-',label='Dobles FB=2.8575cm - RB=0.00cm')
ax1.plot(offaxisAngles, F309_NR_Doubles/max(np.array(F309_NR_Doubles)),'o-',label='Dobles FB=3.0967cm - RB=0.00cm')
ax1.plot(offaxisAngles, F313_NR_Doubles/max(np.array(F313_NR_Doubles)),'o-',label='Dobles FB=3.1334cm - RB=0.00cm')
ax1.plot(offaxisAngles, F317_NR_Doubles/max(np.array(F317_NR_Doubles)),'o-',label='Dobles FB=3.1700cm - RB=0.00cm')
ax1.set_ylabel('Doubles normalized intensity',fontsize=16)
ax1.axvline(8.25,color='Grey',linestyle='--',lw=0.8)
ax1.text(7.7,0.4,'Si Detector Edge = 8.25"',rotation=90,fontsize=10,color='Grey')
ax1.axvline(11.91,color='Grey',linestyle='--',lw=0.8)
ax1.text(11.4,0.7,'Si Detector Diagonal = 11.91"',rotation=90,fontsize=10,color='Grey')
plt.savefig(SaveFolder+'My_gallery_example5.png')
