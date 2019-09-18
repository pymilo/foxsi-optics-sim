'''
Goal: This figure shows several plots starting from on-axis and moving off-axis
      showing how the ghost ray pattern emerges and changes as the sources moves
      further off-axis. Source at 1 AU. No energy dependance included in this
      example.

User Inputs:
              1. Number of rays.
              2. Path to the folder where to save the final figure.

Run:
        ipython gallery_example2.py

Output:
        An image saved as My_gallery_example2.png

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
offaxisAngles = np.arange(0.,33.,4.)     ## Off-axis angles [arcmin]

## Creating empty lists:
All_Drays, All_Hrays, All_Prays, All_Srays = [], [], [], []
All_Dx, All_Dy, All_Hx, All_Hy, All_Px, All_Py = [], [], [], [], [], []
All_Sx, All_Sy = [], []

for angle in offaxisAngles:
    #Create Source :
    Xs = -Sdist * np.sin(np.deg2rad(np.sqrt(2.) * angle / 120.0))
    Ys = -Sdist * np.sin(np.deg2rad(np.sqrt(2.) * angle / 120.0))
    source = Source(type='point',center=[Xs, Ys, Sdist ])
    print('Off-axis Angle: %f' % angle)
    module = Module(radii = [5.151,4.9,4.659,4.429,4.21,4.0,3.799,3.59,3.38,3.17], core_radius=(fbr,rbr))
    rays = source.generateRays(module.targetFront,n)
    module.passRays(rays)
    #Rrays = [ray for ray in rays if (ray.tag != 'Source')] #kills the passthrough rays
    #save_rays(rays,filename=SaveFolder+'rays_Angle_=_'+str(angle)+'.csv')

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
    Srays = [ray for ray in rays if (ray.des[2]==230.0 and ray.bounces ==0 and ray.tag[-8:] == 'Source-D' )]
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

fig = plt.figure(figsize=(15,15))
st = fig.suptitle("FOXSI rocket optics performance for off-axis sources", fontsize=30,y=0.92)
for i, angle in enumerate(offaxisAngles):
    plt.subplot(3,3,i+1)
    plt.title(str(angle)+'arcmin Off-Axis',fontsize=14)
    plt.ylabel('cm',fontsize=14)
    plt.yticks(fontsize=12)
    plt.xticks(fontsize=12)
    plt.scatter(All_Hx[i],All_Hy[i],color='black',s=0.5,alpha=0.9)
    plt.scatter(All_Px[i],All_Py[i],color='black',s=0.5,alpha=0.9)
    plt.scatter(All_Dx[i],All_Dy[i],color='black',s=0.5,alpha=0.9)
    plt.scatter(All_Sx[i],All_Sy[i],color='black',s=0.5,alpha=0.9)
    plt.ylim(-2.0,.7)
    plt.xlim(-2.0,.7)
    plt.tick_params(labelsize=8)
    ax = plt.gca()
    ax.add_patch(patches.Rectangle((-0.48,-0.48),0.96,0.96,fill=False,linewidth=0.5))
    ax.annotate('Optical axis',xy=[0.01,0.01],xytext=(-20, 25),color='black',alpha=0.8,
                textcoords='offset points',arrowprops=dict(
                arrowstyle='simple,tail_width=0.3,head_width=0.8,head_length=0.8',
                facecolor='grey',ec='grey'))
    #ax.add_patch(patches.Circle((0,0),np.sqrt(0.48),fill=False,linewidth=0.5,alpha=0.5))
    plt.savefig(SaveFolder+'My_gallery_example2.png')
