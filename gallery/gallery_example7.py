'''
Goal: This figure shows several plots starting from on-axis and moving off-axis
      showing how the ghost ray pattern emerges and changes as the sources moves
      further off-axis. Source at 1 AU. No energy dependance included in this
      example. For FOXSI-SMEX Geometry.

User Inputs:
              0. FOXSI-SMEX PRESCRIPTION [lines 61-62]. Ask Albert Shih [albert.y.shih@nasa.gov]
                 or Steven Christe [steven.d.christe@nasa.gov] for the exact parameters.
              1. Number of rays.
              2. Off-axis angles
              3. Blocker Sizes
              4. Path where to save CSV files with rays and final plots.

Run:
              ipython SMEX-OffAxis.py

Output:
              1. CSV files with rays.
              2. "gallery_example7_00.png" - ghost-ray patterns colored by Par, Hyp, and Straight-through Ghost-Rays.
              3. "gallery_example7_01.png" - 2D-histogram of Ghost-ray patterns.

Last update: Sep, 2019
'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
from foxsisim.detector import Detector
from foxsisim.source import Source
from foxsisim.module import Module
from foxsisim.detector import Detector
from foxsisim.util import save_rays


n = 5000        ## Number of rays
SaveFolder = '/Users/Kamilobu/Desktop/test/' ## Path of the SaveFolder

fbr = 6.296          ## Front blocker radius [cm]. Need to confirm with Ron and Wayne.
rbr = 5.99           ## Rear blocker radius [cm]. Need to confirm with Ron and Wayne.
Sdist = -1.5e13      ## Distance to the Sun [cm].
offaxisAngles = np.array([0.0,2.0,4.0,7.0,10.0,16.,20.,24.,32])#np.arange(0.,33.,4.)     ## Off-axis angles [arcmin]

## Creating empty lists:
All_Drays, All_Hrays, All_Prays, All_Srays = [], [], [], []
All_Dx, All_Dy, All_Hx, All_Hy, All_Px, All_Py = [], [], [], [], [], []
All_Sx, All_Sy = [], []

fig, axs = plt.subplots(3, 3, sharex=True, sharey=True, figsize=(15,15))
fig.subplots_adjust(hspace=0.01,wspace=0.01)
st = fig.suptitle("FOXSI-SMEX Optics performance for off-axis sources", fontsize=28,y=0.92)

for i, angle in enumerate(offaxisAngles):
    #Create Source :
    #Xs = -Sdist * np.sin(np.deg2rad(np.sqrt(2.) * angle / 120.0))
    #Ys = -Sdist * np.sin(np.deg2rad(np.sqrt(2.) * angle / 120.0))
    Xs = -Sdist * np.sin(np.deg2rad(angle / 60.0))
    Ys = 0.0
    source = Source(type='point',center=[Xs, Ys, Sdist ])
    print('Off-axis Angle: %f' % angle)
    module = Module(radii = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
                    focal=0.0, core_radius=(fbr,rbr))
    rays = source.generateRays(module.targetFront,n)
    module.passRays(rays)
    Rrays = [ray for ray in rays if (ray.tag != 'Source')] #kills the passthrough rays
    save_rays(rays,filename=SaveFolder+'rays_Angle_=_'+str(angle)+'.csv')

    # Create detector :
    detector = Detector(width=30,
                    height=30,
                    normal = [0,0,1],
                    center = [0,0,1430],
                    reso = [4096,4096])
   # Detector Catch rays:
    detector.catchRays(rays)
    '''Defining D, H, and P rays'''
    Drays = [ray for ray in rays if (ray.des[2]==1430.0 and ray.bounces ==2 )]
    Srays = [ray for ray in rays if (ray.des[2]==1430.0 and ray.bounces ==0 and ray.tag[-8:] == 'Source-D' )]
    Hrays = [ray for ray in rays if (ray.des[2]==1430.0 and ray.bounces ==1 and ray.tag[-4:] == 'Hy-D' )]
    Prays = [ray for ray in rays if (ray.des[2]==1430.0 and ray.bounces ==1 and ray.tag[-4:] == 'Pa-D' )]

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

    plt.subplot(3,3,i+1)
    plt.scatter(All_Hx[i],All_Hy[i],color='red',s=0.005,alpha=0.9)
    plt.scatter(All_Px[i],All_Py[i],color='blue',s=0.005,alpha=0.9)
    plt.scatter(All_Dx[i],All_Dy[i],color='green',s=0.005,alpha=0.9)
    plt.scatter(All_Sx[i],All_Sy[i],color='black',s=0.005,alpha=0.9)
    plt.ylim(-14.0,14.)
    plt.xlim(-14.0,14.)
    if i not in [6,7,8]: plt.xticks([]);
    else: plt.xticks(fontsize=12); plt.xlabel('cm',fontsize=14)
    if i not in [0,3,6]: plt.yticks([])
    else: plt.yticks(fontsize=18); plt.ylabel('cm',fontsize=14)
    plt.tick_params(labelsize=14)
    ax = plt.gca()
    ax.add_patch(patches.Rectangle((-1.98,-1.98),3.96,3.96,fill=False,linewidth=0.5))
    ax.annotate('Optical axis',xy=[0.01,0.01],xytext=(-20, 25),color='black',alpha=0.8,
                textcoords='offset points',arrowprops=dict(
                arrowstyle='simple,tail_width=0.3,head_width=0.8,head_length=0.8',
                facecolor='grey',ec='grey'))
    ax.annotate(str(angle)+' arcmin',xy=[6,12],fontsize=12,color='black',alpha=0.7)
    r = 6.5
    ax.add_patch(patches.Circle((r - angle * 2.6/(r),0),r,fill=False,linewidth=0.5,alpha=0.5,color='black'))
plt.savefig(SaveFolder+'gallery_example7_00.png')


fig, axs = plt.subplots(3, 3, sharex=True, sharey=True, figsize=(15,15))
fig.subplots_adjust(hspace=0.01,wspace=0.01)
st = fig.suptitle("FOXSI-SMEX Optics performance for off-axis sources", fontsize=28,y=0.92)
for i, angle in enumerate(offaxisAngles):
    plt.subplot(3,3,i+1)
    All_X = np.concatenate((All_Hx[i],All_Px[i],All_Dx[i],All_Sx[i]))
    All_Y = np.concatenate((All_Hy[i],All_Py[i],All_Dy[i],All_Sy[i]))
    if i == 0:
        counts,ybins,xbins,image = plt.hist2d(All_X, All_Y, bins=100,
                                                    cmap=plt.cm.plasma_r,norm=mcolors.LogNorm(vmax=1.0),normed=True)
        imagebar = image;
        vmin0 = counts[np.where(counts>0)].min();
    else:
        counts,ybins,xbins,image = plt.hist2d(All_X, All_Y, bins=100,
                                                    cmap=plt.cm.plasma_r,norm=mcolors.LogNorm(vmax=1.0,vmin=vmin0),normed=True)
    plt.ylim(-14.0,14.)
    plt.xlim(-14.0,14.)
    if i not in [6,7,8]: plt.xticks([]);
    else: plt.xticks(fontsize=12); plt.xlabel('cm',fontsize=14)
    if i not in [0,3,6]: plt.yticks([])
    else: plt.yticks(fontsize=12); plt.ylabel('cm',fontsize=14)
    plt.tick_params(labelsize=8)
    ax = plt.gca()
    ax.add_patch(patches.Rectangle((-1.98,-1.98),3.96,3.96,fill=False,linewidth=0.5))
    ax.annotate('Optical axis',xy=[0.01,0.01],xytext=(-20, 25),color='black',alpha=0.8,
                textcoords='offset points',arrowprops=dict(
                arrowstyle='simple,tail_width=0.3,head_width=0.8,head_length=0.8',
                facecolor='grey',ec='grey'))
    r = 6.5
    ax.add_patch(patches.Circle((r - angle * 2.6/(r),0),r,fill=False,linewidth=0.5,alpha=0.5,color='black'))
    ax.annotate(str(angle)+' arcmin',xy=[6,12],fontsize=12,color='black',alpha=0.7)
cbar_ax = fig.add_axes([0.91, 0.115, 0.01, 0.25])
fig.colorbar(imagebar,cax=cbar_ax)
plt.savefig(SaveFolder+'gallery_example7_01.png')
