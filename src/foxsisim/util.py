'''
Created on Jul 2017

@authors: Milo & Steven
'''

import numpy as np
from foxsisim.ray import Ray


def save_rays(list_of_rays, filename='list_of_rays.csv'):
    with open(filename, 'w') as f:
        f.write('index, position[0], position[1], position[2], orientation[0], orientation[1], \
        orientation[2], source[0], source[1], source[2], dest[0], dest[1], dest[2], dead, tag, bounces, energy \n')
        for i, ray in enumerate(list_of_rays):
            f.write('{index},{pos0},{pos1},{pos2},{ori0},{ori1},{ori2},{src0},{src1},{src2},\
            {des0},{des1},{des2},{dead},{tag},{bounces},{energy},\n'.format(
                index=i, pos0=ray.pos[0], pos1=ray.pos[1], pos2=ray.pos[2], ori0=ray.ori[0], ori1=ray.ori[1],
                ori2=ray.ori[2],
                src0=ray.src[0], src1=ray.src[1], src2=ray.src[2], des0=ray.des[0], des1=ray.des[1],
                des2=ray.des[2],
                dead=ray.dead, tag=ray.tag, bounces=ray.bounces, energy=ray.energy))
    f.close()
    print('Rays saved in file : '+filename)

def load_rays(filename='list_of_rays.csv'):
    with open(filename, 'r') as f:
        header = f.readline()
        list_of_rays = []
        for line in f.readlines():
            nray = Ray()
            index, pos0, pos1, pos2, ori0, ori1, ori2, src0, src1, src2, des0, des1, \
                des2, dead, tag, bounces, energy, none = line.strip().split(',')
            # loading values to nray.
            nray.pos = np.array((pos0, pos1, pos2), dtype='float')
            nray.ori = np.array((ori0, ori1, ori2), dtype='float')
            nray.src = np.array((src0, src1, src2), dtype='float')
            nray.des = np.array((des0, des1, des2), dtype='float')
            nray.dead = dead
            nray.tag = tag
            nray.bounces = bounces
            nray.energy = energy
            list_of_rays.append(nray)
    f.close()
    print('Rays from '+filename+' loaded.')
    return list_of_rays
