import numpy as np
import matplotlib.pyplot as plt

def f(x,y,z):
    return np.array([x,y,z])


r = np.linspace(0,1,10)
theta = np.linspace(0,np.pi,10)
phi = np.linspace(0,2*np.pi,10)

def sph_basis_vectors(theta, phi):
    rhat = np.array([np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)])
    theta_hat = np.array([np.cos(theta)*np.cos(phi), np.cos(theta)*np.sin(phi), -1*np.sin(theta)])
    phi_hat = np.array([-1*np.sin(phi), np.cos(phi), 0*phi])

    return rhat, theta_hat, phi_hat

def cart_basis_vectors(theta, phi):
    pass

def sph_to_cart(r, theta, phi):
    x = r*np.sin(theta)*np.cos(phi)
    y = r*np.sin(theta)*np.sin(phi)
    z = r*np.cos(theta)

    return np.array([x,y,z])

def cart_to_sph(x,y,z):
    r = (x**2 + y**2 + z**2)**.5
    theta = np.arccos(z/r)
    phi = np.arctan2(y,x)
    phi[phi<0] += 2*np.pi

    return np.array([r,theta,phi])

def cart_to_sph_domain(func):

    def g(r, theta, phi, *args, **kwargs):
        x,y,z = sph_to_cart(r,theta,phi)
        return func(x,y,z, *args, **kwargs)

    return g

def sph_to_cart_domain(func):

    def g(x,y,z, *args, **kwargs):
        r,theta,phi = cart_to_sph(x,y,z)
        return func(r,theta,phi, *args, **kwargs)

    return g

def cart_to_sph_range(func):
    pass

def sph_to_cart_range(func):
    def g(*args, **kwargs):
        func_ret = func(*args, **kwargs)
        rhat, theta_hat, phi_hat = sph_basis_vectors(args[1], args[2])  # <--- PROBLEM: we don't know if domain is cart or sph, and therfore can't get the right basis vectors
        return rhat*func_ret[0] + theta_hat*func_ret[1] + phi_hat*func_ret[2]
    return g

if __name__ == "__main__":
    g = cart_to_sph_domain(f)
    g = sph_to_cart_range(f)


    R, THETA, PHI = np.meshgrid(np.array([1]), theta,phi, indexing='ij')
    print(g(R,THETA,PHI).shape)
    # THETA, PHI = np.meshgrid(theta,phi, indexing='ij')
    # print(g(1,THETA,PHI).shape)

