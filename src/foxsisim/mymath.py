'''
Created on Jul 19, 2011

@author: rtaylor
'''
from math import pi,acos,atan,tan
import numpy as np
from numpy import dot
from numpy.linalg import norm

halfpi = pi/2
dtf = np.dtype('f8')

def angleBetweenVectors(a,b):
    '''
    Returns the angle between two vectors
    '''
    return acos(dot(a,b)/(norm(a)*norm(b)))

def reflect(x,normal):
    '''
    Takes a vector and reflects it in relation to a normal
    '''
    # if the angle of incidence is greater than 90 deg, return None
    if acos(dot(-x,normal)/(norm(x)*norm(normal))) > halfpi:
        return None
    return x-2*dot(x,normal)*normal

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
    
    
    