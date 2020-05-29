'''
Created on Jul 19, 2011

@author: rtaylor
'''
from foxsisim.annulus import Annulus
from foxsisim.shell import Shell
from foxsisim.circle import Circle
from foxsisim.mymath import reflect, calcShellAngle
from math import tan
from numpy.linalg import norm
from numpy import zeros

class Module:
    '''
    A complete foxsi module. By default, it consists of seven nested shells.
    '''

    def __init__(self,
                 base=[0, 0, 0],
                 seglen=30.0,
                 focal=200.0,
                 radii=[5.151, 4.9, 4.659, 4.429, 4.21, 4.0, 3.799],
                 angles=None,
                 conic=False,
                 shield=True,
                 core_radius=None,
                 thickness=None
                 ):
        '''
        Constructor

        Parameters:
            base:       the center point of the wide end of the segment
            seglen:     the axial length of each segment
            focal:      the focal length, measured from the center of the module
            radii:      a list of radii, one for each shell from biggest to
                        smallest
            angles:     optional parameter to overwrite the shell angles computed
                        by constructor
            conic:      if True, use a conic approximation to the Wolter-I parabola-hyperbola.
            shield:       if True, create a shield at the core of the optic to block straight-thru
                        flux.
            shield_radius If shield is True then use this value for the shield radius
        '''
        if angles is None:
            angles = calcShellAngle(radii, focal)
        elif len(radii) != len(angles):
            raise ValueError('Number of radii and angles do not match')

        self.shells = []
        for i, r in enumerate(radii):
            self.shells.append(Shell(base=base, focal=focal, seglen=seglen, ang=angles[i],
                                     r=r, conic=conic))

        # inner core (blocks rays going through center of module)
        # not sure if the core must have an angle to it so made it very small
        # and made coreFaces match in radius
        if shield is True:
            self.shield = True
            if core_radius is None:
                r0 = self.shells[-1].front.r0
                r1 = r0 - seglen * tan(4 * angles[-1])
                # ang = atan((r0 - r1) / (2 * seglen))
            else:
                if isinstance(core_radius,(int,float)):
                    r0 = core_radius
                    r1 = core_radius
                elif isinstance(core_radius,(tuple,list)) and len(core_radius)==2 :
                    r0 = core_radius[0]
                    r1 = core_radius[1]
                else: print('Error: Keyword core_radius must be a number or a 2D tuple')
            # self.core = Segment(base=base, seglen=2 * seglen, ang=0, r0=r0)
            self.coreFaces = [Circle(center=base, normal=[0, 0, 1], radius=r0),
                              Circle(center=[base[0], base[1],
                                             base[2] + 2 * seglen],
                                     normal=[0, 0, -1], radius=r1)]
        else:
            self.shield = None

        # sieve effect :
        if thickness is None:
            self.thickness = zeros(len(radii)).tolist()
        elif isinstance(thickness, (tuple, list)) and len(thickness)==len(radii) :
            self.thickness = thickness
        else:
            print('Error: Keyword thickness must have same length as radii')
        self.sieveFront = []
        self.sieveBack  = []
        for thick, shell in zip(self.thickness, self.shells):
            self.sieveFront.append(Annulus(center=base, normal=[0, 0, 1],
                                           radius=shell.front.r0,thickness=thick))
            self.sieveBack.append(Annulus(center=[base[0], base[1], base[2] + 2 * seglen],
                                          normal=[0, 0, -1],
                                          radius=shell.back.r1,thickness=thick))

    def getDims(self):
        '''
        Returns the module's dimensions:
        [radius at wide end, radius at small end, length]
        '''
        front = self.shells[0].front
        back = self.shells[0].back
        return [front.r0, back.r1, front.seglen + back.seglen]

    def getSurfaces(self):
        '''
        Returns a list of surfaces
        '''
        surfaces = []
        for shell in self.shells:
            surfaces.extend(shell.getSurfaces())
        # surfaces.append(self.core)
        surfaces.extend(self.coreFaces)
        return (surfaces)

    def passRays(self, rays, robust=False):
        '''
        Takes an array of rays and passes them through the front end of
        the module.
        '''
        # print('Module: passing ',len(rays),' rays')

        # get all module surfaces
        allSurfaces = self.getSurfaces()
        allSurfaces.remove(self.coreFaces[0])  # we'll test these seperately
        allSurfaces.remove(self.coreFaces[1])

        # create regions consisting of adjacent shells
        regions = [None for shell in self.shells]
        for i, shell in enumerate(self.shells):
            # innermost shell
            if i == len(self.shells) - 1:
                regions[i] = shell.getSurfaces()
                # regions[i].append(self.core)
            else:
                # outer shell (reflective side facing region)
                regions[i] = shell.getSurfaces()
                # nested shell (non reflective)
                regions[i].extend(self.shells[i + 1].getSurfaces())

        for ray in rays:
            # Does the ray hit the front sieve?
            for annulus in self.sieveFront:
                sol = annulus.rayIntersect(ray)
                if sol is not None:
                    ray.pos = ray.getPoint(sol[2])
                    ray.dead = True
                    ray.des = ray.pos
                    ray.hist.append(ray.pos)
                    ray.update_tag(annulus.tag)
                    continue
                else:
                    # move ray to the front of the optics
                    ray.moveToZ(self.coreFaces[0].center[2])

            # reset surfaces
            surfaces = [s for s in allSurfaces]
            firstBounce = True  # used for optimization

            # while ray is inside module
            while True:
                # find nearest ray intersection
                bestDist = None
                bestSol = None
                bestSurf = None
                for surface in surfaces:

                    sol = surface.rayIntersect(ray)
                    if sol is not None:
                        dist = norm(ray.getPoint(sol[2]) - ray.pos)
                        if bestDist is None or dist < bestDist:
                            bestDist = dist
                            bestSol = sol
                            bestSurf = surface

                # if a closest intersection was found
                if bestSol is not None:

                    # update ray
                    ray.pos = ray.getPoint(bestSol[2])
                    ray.hist.append(ray.pos)
                    ray.bounces += 1
                    ray.update_tag(bestSurf.tag)
                    #print("%i ray bounce number %i" % (ray.num, ray.bounces))

                    x = reflect(ray.ori,
                                bestSurf.getNormal(bestSol[0], bestSol[1]),
                                ray.energy)
                    # print('x = ',x)
                    # if reflected
                    if x is not None:
                        # update ori to unit vector reflection
                        ray.ori = x / norm(x)
                    # otherwise, no reflection means ray is dead
                    else:
                        ray.dead = True
                        # print("%i ray killed by reflect" % ray.num)
                        break

                    # knowing the surface it has just hit, we can
                    # narrow down the number of surface to test

                    # remove shells the ray cannot even 'see'
                    if firstBounce:
                        firstBounce = False
                        for region in regions:
                            if bestSurf is region[0] or bestSurf is region[1]:
                                surfaces = [s for s in region]
                                break

                    # assuming each segment can be hit no more than once
                    # eliminate the surface from our list
                    if not robust:
                        surfaces.remove(bestSurf)

                # if no intersection, ray can exit module
                else:
                    break
                    # print(ray.hist)
                    # print(ray.des)

            sol = self.coreFaces[1].rayIntersect(ray)
            if sol is not None:
                # print("ray hit rear blocker")
                ray.pos = ray.getPoint(sol[2])
                #ray.bounces += 1
                ray.dead = True
                ray.des = ray.pos
                ray.hist.append(ray.pos)
                ray.update_tag(self.coreFaces[1].tag)
                continue
            # Does the ray hit the back sieve?
            for annulus in self.sieveBack:
                sol = annulus.rayIntersect(ray)
                if sol is not None:
                    #print("ray hit back sieve")
                    ray.pos = ray.getPoint(sol[2])
                    ray.dead = True
                    ray.des = ray.pos
                    ray.hist.append(ray.pos)
                    ray.update_tag(annulus.tag)
                    continue
            else:
                ray.moveToZ(self.coreFaces[1].center[2])
                #ray.hist.append(ray.pos)

    def plot2D(self, axes, color='b'):
        '''
        Plots a 2d cross section of the module
        '''
        for shell in self.shells:
            shell.plot2D(axes, color)
        # print(self.coreFaces[0].center)
        # print(self.coreFaces[1].center)
        if self.shield is not None:
            # plot core
            # self.core.plot2D(axes, color)
            # base = self.core.base
            r0 = self.coreFaces[0].radius
            r1 = self.coreFaces[1].radius
            z0 = self.coreFaces[0].center[2]
            z1 = self.coreFaces[1].center[2]
            # seglen = self.core.seglen
            axes.plot((z0, z0), (r0, -r0), '-' + color)
            axes.plot((z1, z1), (r1, -r1), '-' + color)

    def plot3D(self, axes, color='b'):
        '''
        Generates a 3d plot of the module in the given figure
        '''
        for shell in self.shells:
            shell.plot3D(axes, color)

    def targetFront(self, a, b):
        '''
        Takes two list arguments of equal size, the elements of which range
        from 0 to 1. Returns an array of points that exist on the circle
        defined by the wide end of the module.
        '''
        # must modify 'a' so that we dont return points from the core
        r0 = self.shells[0].front.r0
        r1 = self.coreFaces[0].radius
        a0 = (r1 / r0) ** 2  # the 'a' value that gives r1=sqrt(a)*r0
        adiff = 1 - a0
        for i in range(len(a)):
            a[i] = a[i] * adiff + a0
        return self.shells[0].targetFront(a, b)

    def targetBack(self, a, b):
        '''
        Takes two list arguments of equal size, the elements of which range
        from 0 to 1. Returns an array of points that exist on the circle
        defined by the small end of the module.
        '''
        # must modify 'a' so that we dont return points from the core
        r0 = self.shells[0].back.r1
        r1 = self.coreFaces[0].radius
        a0 = (r1 / r0) ** 2  # the 'a' value that gives r1=sqrt(a)*r0
        adiff = 1 - a0
        for i in range(len(a)):
            a[i] = a[i] * adiff + a0
        return self.shells[0].targetBack(a, b)
