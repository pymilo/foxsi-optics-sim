'''
Created on Jul 19, 2011

@author: rtaylor
'''
from math import pi,acos,atan,tan
import numpy as np
from numpy import dot
from numpy.linalg import norm
from numpy.random import random
from reflectivity import Reflectivity
from scipy import interpolate

halfpi = pi/2
dtf = np.dtype('f8')
mirror_reflectivity = Reflectivity()

def angleBetweenVectors(a,b):
    '''
    Returns the angle between two vectors
    '''
    return acos(dot(a,b)/(norm(a)*norm(b)))

def reflect(x,normal,energy):
    '''
    Takes a vector and reflects it in relation to a normal
    '''
    # if the angle of incidence is greater than 90 deg, return None
    incident_angle = angle_of_incidence(x, normal)
    graze_angle = halfpi - incident_angle    
    if incident_angle > halfpi:
        return None
    if random(1)[0] > mirror_reflectivity.value(energy, np.rad2deg(graze_angle)):
        return None
    return x-2*dot(x,normal)*normal

def angle_of_incidence(x, normal):
    '''
    Calculate the angle of incidence between a vector and the normal
    '''
    return acos(dot(-x,normal)/(norm(x)*norm(normal)))

def grazing_angle(x, normal):
    '''
    Calculate the grazing angle between a vector and the surface. The complement to the
    angle of incidence.
    '''
    return halfpi - acos(dot(-x,normal)/(norm(x)*norm(normal)))

def calcShellAngle(radius, focalLength):
    '''
    Calculates shell angle(s) given one or more shell radius
    and a focal length. Takes one radius, a list, or a numpy array
    of radii. Returns an angle or a numpy array of angles.
    '''
    if type(radius) is np.ndarray or type(radius) is list:
        return np.array([atan(r/(focalLength*4)) for r in radius],dtf) # took this eqn from the excel file...
    else: 
        return atan(radius/(focalLength*4))
    
def calcShellRadius(angle, focalLength):
    '''
    Calculates shell radii given one or more shell angles
    and a focal length. Takes one angle, a list, or a numpy array
    of angles. Returns a radius or a numpy array of radii.
    '''
    if type(angle) is np.ndarray or type(angle) is list:
        return np.array([tan(a)*focalLength*4 for a in angle],dtf)
    else:
        return tan(angle)*focalLength*4
    
def genCustomRands(x, y, n):
    '''
    Generate n random numbers given a distribution (x, y)
    '''
    last_index = 0
    not_done = True
    result = np.zeros(n)
    f = interpolate.interp1d(x, y, kind = 2)
    while not_done: 
        xtry = random(20*n) * (x.max() - x.min()) + x.min()
        ytry = random(20*n) * (y.max() - y.min()) + y.min()
        #now fill the array
        good_index = ytry < f(xtry)
        good_count = np.count_nonzero(good_index)
        if good_count + last_index >= n:
            not_done = False
            good_count = n - last_index
        result[last_index:good_count+last_index] = xtry[good_index][0:good_count]
        last_index += good_count
    return result