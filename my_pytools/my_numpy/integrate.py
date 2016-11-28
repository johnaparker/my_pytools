import numpy as np
from scipy.integrate import simps

def simps_2d(xd,yd,fd):
    """1d simpsons rule extended to 2d"""
    xData = np.zeros(len(xd))
    for i,x in enumerate(xd):
        xData[i] = simps(fd[i,:], yd)

    return simps(xData, xd)

def simps_3d(xd,yd,zd,fd):
    """1d simpsons rule extended to 3d"""
    xyData = np.zeros((len(xd), len(yd)))
    for i,x in enumerate(xd):
        for j,y in enumerate(yd):
            xyData[i,j] = simps(fd[i,j,:], zd)

    return simps_2d(xd,yd, xyData)

def simps_4d(xd,yd,zd,wd,fd):
    """1d simpsons rule extended to 4d"""
    xyzData = np.zeros((len(xd), len(yd), len(zd)))
    for i,x in enumerate(xd):
        for j,y in enumerate(yd):
            for j,k in enumerate(zd):
                xyzData[i,j,k] = simps(fd[i,j,k,:], wd)

    return simps_3d(xd,yd,zd, xyzData)
