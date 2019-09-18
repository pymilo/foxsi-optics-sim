'''
Goal: Simulated ghost ray pattern for a solar source at 28 arcminute off axis
      for a 10-shell FOXSI rocket optics module. The image is color-coded to
      show what reflections lead to what features or parts of the ghost ray
      pattern. In green rays, the rays that reflect twice and are properly focused.
      In blue and red rays are rays that reflect once on the paraboloid and the
      hyperboloid segment respectively.

      Genreate also a cross-section of the optics module showing the spatial distribution of
      the singly reflected rays differentiated by color.

User Inputs:
              1. Number of rays.
              2. Path to the folder where to save the final figure.

Run:
        ipython gallery_example3.py

Output:
        An image saved as My_gallery_example3.png

Last update: Sep, 2019
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from foxsisim.detector import Detector
from foxsisim.source import Source
from foxsisim.module import Module
from foxsisim.detector import Detector

n = 1000        ## Number of rays
SaveFolder = '/Users/Kamilobu/Desktop/test/' ## Path of the SaveFolder

fbr = 3.09671       ## Front blocker radius [cm].
rbr = 2.62          ## Rear blocker radius [cm].
Sdist = -1.5e13     ## Distance to the Sun [cm].
angle = 28.0        ## Off-axis angles [arcmin].

Xs = -Sdist * np.sin(np.deg2rad(np.sqrt(2.) * angle / 120.0))
Ys = -Sdist * np.sin(np.deg2rad(np.sqrt(2.) * angle / 120.0))
source = Source(type='point',center=[Xs, Ys, Sdist ])
print('Off-axis Angle: %f' % angle)
module = Module(radii = [5.151,4.9,4.659,4.429,4.21,4.0,3.799,3.59,3.38,3.17], core_radius=(fbr,rbr))
rays = source.generateRays(module.targetFront,n)
module.passRays(rays)
rays = [ray for ray in rays if (ray.tag != 'Source')] #kills the passthrough rays

## Creating empty lists:
All_Drays, All_Hrays, All_Prays, All_Srays = [], [], [], []
All_Dx, All_Dy, All_Hx, All_Hy, All_Px, All_Py = [], [], [], [], [], []
All_Sx, All_Sy = [], []

# Create detector :
detector = Detector(width=10,
                    height=10,
                    normal = [0,0,1],
                    center = [0,0,230],
                    reso = [1024,1024])
# Detector Catch rays:
detector.catchRays(rays)
'''Defining D, H, and P rays'''
Drays = [ray for ray in rays if (ray.des[2]==230.0 and ray.bounces ==2 )]
Srays = [ray for ray in rays if (ray.des[2]==230.0 and ray.bounces ==0 and ray.tag[-8:] == 'Source-D')]
Hrays = [ray for ray in rays if (ray.des[2]==230.0 and ray.bounces ==1 and ray.tag[-4:] == 'Hy-D' )]
Prays = [ray for ray in rays if (ray.des[2]==230.0 and ray.bounces ==1 and ray.tag[-4:] == 'Pa-D' )]

All_Drays.append(Drays)
All_Hrays.append(Hrays)
All_Prays.append(Prays)
All_Srays.append(Srays)

sim_scale = 1.0    # 1cm = 17.4 arcmin
#sim_scale = 17.4    # 1cm = 17.4 arcmin

#Hyperboloid
Hx, Hy = [], []
for ray in Hrays:
    Hx.append(ray.pos[0]*sim_scale)
    Hy.append(ray.pos[1]*sim_scale)
All_Hx.append(Hx)
All_Hy.append(Hy)

# Paraboloid
Px, Py = [], []
for ray in Prays:
    Px.append(ray.pos[0]*sim_scale)
    Py.append(ray.pos[1]*sim_scale)
All_Px.append(Px)
All_Py.append(Py)

# Double
Dx, Dy = [], []
for ray in Drays:
    Dx.append(ray.pos[0]*sim_scale)
    Dy.append(ray.pos[1]*sim_scale)
All_Dx.append(Dx)
All_Dy.append(Dy)

# StraightThrough
Sx, Sy = [], []
for ray in Srays:
    Sx.append(ray.pos[0]*sim_scale)
    Sy.append(ray.pos[1]*sim_scale)
All_Sx.append(Sx)
All_Sy.append(Sy)

FrontRadii = [5.345, 5.085, 4.835, 4.595, 4.365, 4.15, 3.94, 3.725, 3.51, 3.29]
InterRadii = [5.151,4.9,4.659,4.429,4.21,4.0,3.799,3.59,3.38,3.17]
InnerRadii = [4.56, 4.335, 4.125, 3.92, 3.725, 3.54, 3.36, 3.18, 2.995, 2.805]

prays = [ray.pos for ray in rays]
orays = [ray.ori for ray in rays]
srays = [ray.src for ray in rays]
drays = [ray.des for ray in rays]
trays = [ray.tag for ray in rays]
hrays = [ray.hist for ray in rays]
brays = [ray.bounces for ray in rays]
deadrays = [ray.dead for ray in rays]

CSHrays = [ray for ray in rays if (ray.bounces ==1 and ray.hist[-2][2] >= 30 and ray.tag[-4:] == 'Hy-D')]
CSPrays = [ray for ray in rays if (ray.bounces ==1 and ray.hist[-2][2] <= 30 and ray.tag[-4:] == 'Pa-D')]
CSHx, CSHy = np.array([ray.hist[-2][0] for ray in CSHrays]), np.array([ray.hist[-2][1] for ray in CSHrays])
CSPx, CSPy = np.array([ray.hist[-2][0] for ray in CSPrays]), np.array([ray.hist[-2][1] for ray in CSPrays])

fig = plt.figure(figsize=(11,5))
st = fig.suptitle("Singly and doubly reflected rays for a "+str(angle)+" arcmin off-axis point source", fontsize=18)
plt.subplot(1,2,1)
plt.title('Focal plane',fontsize=14)
plt.xlabel('cm',fontsize=14);plt.ylabel('cm',fontsize=14)
plt.yticks(fontsize=12);plt.xticks(fontsize=12)
plt.scatter(Hx,Hy,color='red',s=0.3,alpha=0.7)
plt.scatter(Px,Py,color='blue',s=0.3,alpha=0.7)
plt.scatter(Dx,Dy,color='green',s=0.3,alpha=0.7)
plt.scatter(Sx,Sy,color='black',s=0.3,alpha=0.7)
plt.ylim(-2.0,.7)
plt.xlim(-2.0,.7)
ax = plt.gca()
ax.add_patch(patches.Rectangle((-0.48,-0.48),0.96,0.96,fill=False,linewidth=0.5))
ax.add_patch(plt.Circle((0, 0), 0.03, color='k',fill=True,linewidth=.3))
ax.annotate('Optical axis',xy=[0.01,0.03],xytext=(-20, 30),
            textcoords='offset points',arrowprops=dict(
                arrowstyle='simple,tail_width=0.3,head_width=0.8,head_length=0.8',
                facecolor='k'))
## Cross-Section
plt.subplot(1,2,2)
ax = fig.gca()
# Plot Shells
for r in InterRadii:
    c = plt.Circle((0, 0), r, color='k',fill=False,linewidth=.3)
    ax.add_artist(c)

# Plot random points
plt.scatter(CSPx,CSPy,s=0.3,color='b')
plt.scatter(CSHx,CSHy,s=0.3,color='r')
plt.title('Optics cross-section',fontsize=14)
plt.xlabel('cm',fontsize=14);plt.ylabel('cm',fontsize=14)
plt.yticks(fontsize=12);plt.xticks(fontsize=12)
plt.xlim(-6,6);plt.ylim(-6,6)
plt.savefig(SaveFolder+'My_gallery_example3.png')
