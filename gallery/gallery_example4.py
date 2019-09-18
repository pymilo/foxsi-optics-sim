'''
Goal: The simulated energy response of a point source on the Sun 28 arcminute
      off-axis as observed by the FOXSI rocket mirror modules. The spectrum of
      the source is assumed to be flat from 0 to 30 keV.

User Inputs:
              1. Number of rays.
              2. Path to the folder where to save the final figure.

Run:
        ipython gallery_example4.py

Output:
        An image saved as My_gallery_example4.png

Last update: Sep, 2019
'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime
from foxsisim.module import Module
from foxsisim.source import Source
from foxsisim.detector import Detector
import seaborn as sns
sns.set_context('paper')
sns.set_style('dark')

n = 1000        ## Number of rays
SaveFolder = '/Users/Kamilobu/Desktop/test/' ## Path of the SaveFolder

fbr = 3.09671       ## Front blocker radius [cm].
rbr = 2.62          ## Rear blocker radius [cm].
Sdist = -1.5e13     ## Distance to the Sun [cm].
angle = 28.0        ## Off-axis angles [arcmin].
max_energy = 30.0   ## Maximum energy

''' Defining Input Spectrum '''
def spectrum(z):
        if (type(z) is not type([1])) and (type(z) is not type(np.array(1))):
            x = np.array([z])
        else:
            x = np.array(z)
        return np.piecewise(x, [x < 0, ((x < max_energy) & (x > 0)), (x >= max_energy)], [0, 1./max_energy, 0])

''' Creating the FOXSI telescope '''
module = Module(radii = [5.151,4.9,4.659,4.429,4.21,4.0,3.799,3.59,3.38,3.17], core_radius=(fbr,rbr))

Xs = -Sdist * np.sin(np.deg2rad(np.sqrt(2.) * angle / 120.0))
Ys = -Sdist * np.sin(np.deg2rad(np.sqrt(2.) * angle / 120.0))
source = Source(type='point', center=[Xs, Ys, Sdist ])
source.loadSpectrum(spectrum)

''' Generating rays '''
tstart = datetime.now()
rays = source.generateRays(module.targetFront, n)
tgen = datetime.now()
print('rays generated, time = ' + str((tgen - tstart).seconds) + 'seconds' )

print('Pasing rays')
module.passRays(rays)

rays = [ray for ray in rays if (ray.dead==False)] ## save only those alive rays

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

fig = plt.figure(figsize=(12,12))
st = fig.suptitle("Energy response for a "+str(angle)+" arcmin off-axis point source", fontsize=18,y=.95)
## Straight-Through
plt.subplot(2,2,1)
plt.hist([ray.energy for ray in Srays], density=True, label='rays on detector',color='grey',bins=20,alpha=.5)
plt.xlabel('Energy [keV]',fontsize=14)
plt.title('Straight-Through rays - Spectrum',fontsize=14)
plt.xlim(0,30)
plt.yticks(fontsize=10);plt.xticks(fontsize=10)
## Doubles
plt.subplot(2,2,2)
plt.hist([ray.energy for ray in Drays], density=True, label='rays on detector',color='g',bins=20,alpha=.5)
plt.xlabel('Energy [keV]',fontsize=14)
plt.title('Doubly reflected rays - Spectrum',fontsize=14)
plt.xlim(0,20)
plt.yticks(fontsize=10);plt.xticks(fontsize=10)
## Paraboloids
plt.subplot(2,2,3)
plt.hist([ray.energy for ray in Prays], density=True, label='rays on detector',color='b',bins=20,alpha=.5)
plt.xlabel('Energy [keV]',fontsize=14)
plt.title('Singly reflected rays [Paraboloid] - Spectrum',fontsize=14)
plt.xlim(0,20)
plt.yticks(fontsize=10);plt.xticks(fontsize=10)
## Hyperboloids
plt.subplot(2,2,4)
plt.hist([ray.energy for ray in Hrays], density=True, label='rays on detector',color='r',bins=20,alpha=.5)
plt.xlabel('Energy [keV]',fontsize=14)
plt.title('Singly reflected rays [Hyperboloid] - Spectrum',fontsize=14)
plt.xlim(0,20)
plt.yticks(fontsize=10);plt.xticks(fontsize=10)
plt.savefig(SaveFolder+"My_gallery_example4.png")
