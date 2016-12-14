import numpy as np
from my_pytools.my_numpy.integrate import simps_2d
from my_pytools.my_numpy.interpolate import ndinterp
from my_pytools.my_numpy.rotations import rotate_discrete_data

# function
def f(theta_val, phi_val):
    return np.sin(theta_val) + 1

# get discrete f at N^2 angular points
N = 500
tau = np.linspace(1,-1,N)
th = np.arccos(tau)
ph = np.linspace(0,2*np.pi,N)
theta,phi = np.meshgrid(th,ph, indexing='ij')
R = f(theta,phi)

# interpolate f
sig_1 = ndinterp(R, th, ph, fill_value=None)

# rotated f
sig_2 = rotate_discrete_data(sig_1, th, ph, [0,0,1], [1,0,0])


print("First test...")
th_int = np.linspace(0,1.0*np.pi,N)
ph_int = np.linspace(0,2*np.pi,N)
theta_int,phi_int = np.meshgrid(th_int, ph_int)

print("Initial data: ", simps_2d(th_int,ph_int,np.sin(th_int)*sig_1(theta_int, phi_int)))
print("Rotated data: ", simps_2d(th_int,ph_int,np.sin(th_int)*sig_2(theta_int, phi_int)))
print("Expected value: ", (4+np.pi)*np.pi)

print("\nSecond test...")
th_int = np.linspace(0,0.5*np.pi,N)
ph_int = np.linspace(0,2*np.pi,N)
theta_int,phi_int = np.meshgrid(th_int, ph_int)

print("Initial data: ", simps_2d(th_int,ph_int,np.sin(th_int)*sig_1(theta_int, phi_int)))
print("Rotated data: ", simps_2d(th_int,ph_int,np.sin(th_int)*sig_2(theta_int, phi_int)))
print("Expected value: ", (4+np.pi)*np.pi/2)

print("\nThird test...")
th_int = np.linspace(0,0.001*np.pi,N)
ph_int = np.linspace(0,2*np.pi,N)
theta_int,phi_int = np.meshgrid(th_int, ph_int)

y1 = simps_2d(th_int,ph_int,np.sin(th_int)*sig_1(theta_int, phi_int))
y2 = simps_2d(th_int,ph_int,np.sin(th_int)*sig_2(theta_int, phi_int))
print("Initial data: ", y1)
print("Rotated data: ", y2)
print("Ratio: ", y2/y1)
print("Expected ratio: ", 2)

