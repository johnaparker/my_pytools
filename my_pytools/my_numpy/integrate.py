import numpy as np
from scipy.integrate import simps
from .rotations import rotate_discrete_data

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


def sphere_integrate(func, N, theta_min, theta_max, phi_min = 0, phi_max = 2*np.pi, axis_init=None, axis_final=None):
    """Integrate over an angular portion of a sphere (discrete integration)

            func(theta,phi)     function to inegrate
            N                   Number of pts used in discretization
            theta_min           minimum theta
            theta_max           maximum theta
            phi_min             minimum phi
            phi_max             maximum phi
            axis_init           initial z-axis of data
            axis_final          final z-axis of data (if rotation of z-axis is desired)         """

    theta_int = np.linspace(theta_min, theta_max, N)
    phi_int = np.linspace(phi_min, phi_max, N)

    theta = np.linspace(0, np.pi, N)
    phi = np.linspace(0, 2*np.pi, N)

    if axis_init != None and axis_final != None:
        R = rotate_discrete_data(func, theta, phi, axis_init, axis_final)
    else:
        R = func

    # sigma_data = R(*np.meshgrid(theta, phi, indexing='ij'))
    sigma_data = R(*np.meshgrid(theta_int, phi_int))
    return simps_2d(theta_int, phi_int, sigma_data*np.sin(theta_int))
