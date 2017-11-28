"""
special defines any additional special functions on top of scipy.special
"""

import numpy as np
import sympy
import scipy
from scipy import special, integrate, misc
import enum
from functools import lru_cache
from math import factorial

def spherical_hn(n, z, derivative=False):
    """spherical hankel function of the first kind or its derivative

            n: int,array-like        order of the bessel function
            z: array[complex/float]  argument
            derivative: bool         If True, compute the derivative instead    """

    return special.spherical_jn(n,z,derivative) + 1j*special.spherical_yn(n,z,derivative)

def associated_legendre(n,m, deriv=0):
    """associated legendre function of integer order and degree

            n: int         order
            m: int         degree
            deriv: int     derivative to take

        returns lpmv(x) function     """

    x = sympy.symbols('x')
    legfun_sym = sympy.functions.special.polynomials.assoc_legendre(n,m,x)
    legfunc_sym_deriv = sympy.diff(legfun_sym, x, deriv)

    legfun_num_deriv = sympy.lambdify(x,legfunc_sym_deriv, modules='numpy')
    return legfun_num_deriv

def pi_func(n, m):
    """pi special function that appears in the vector spherical harmonics (VSH)

            n: int         order
            m: int         degree

       returns pi(theta)                                                           """

    Pnm = associated_legendre(n,m)

    def f(theta):
        with np.errstate(divide='ignore',invalid='ignore'):
            return m*Pnm(np.cos(theta))/np.sin(theta)
    return f

def tau_func(n, m):
    """pi special function that appears in the vector spherical harmonics (VSH)

            n: int         order
            m: int         degree

       returns tau(theta)                                                           """

    Pnm_d = associated_legendre(n,m, deriv=1)

    def f(theta):
        with np.errstate(divide='ignore',invalid='ignore'):
            return -1*np.sin(theta)*Pnm_d(np.cos(theta))

    return f

@lru_cache(maxsize=None)
def a_func(m, n, u, v, p):
    """a function that appears in the VSH translation coefficients"""

    # if np.abs(m) > n or np.abs(u) > v or np.abs(m+u) > p:
    if np.abs(m) > n or np.abs(m+u) > p:
        print('here')
        return 0

    factor = (2*p+1)/2*factorial(p-m-u)/factorial(p+m+u)

    Pnm = associated_legendre(n,m)
    Pvu = associated_legendre(v,u)
    Ppmu = associated_legendre(p,m+u)
    integrand = lambda x: Pnm(x)*Pvu(x)*Ppmu(x)
    integral = integrate.quad(integrand, -1, 1)[0]

    return factor*integral

@lru_cache(maxsize=None)
def b_func(m, n, u, v, p):
    """b function that appears in the VSH translation coefficients"""

    b1 = (2*p+1)/(2*p-1)
    b2 = (v-u)*(v+u+1)*a_func(m,n,-u-1,v,p-1)
    b3 = -(p-m+u)*(p-m+u-1)*a_func(m,n,-u+1,v,p-1)
    b4 = 2*u*(p-m+u)*a_func(m,n,-u,v,p-1)

    return b1*(b2+b3+b4)

def Emn(m, n, E0):
    return E0*1j**n*(2*n+1)*factorial(n-m)/factorial(n+m)

def A_translation(m, n, u, v, r, theta, phi, k):
    factor = (-1)**u *1j**(v-n)*(2*v+1)/(2*v*(v+1))
    normalization = Emn(u,v,1)/Emn(m,n,1)

    sum_term = 0
    for p in range(np.abs(n-v), n+v+1):
        if np.abs(m-u) > p:
            continue
        else:
            Pnm = associated_legendre(p,m-u)
            sum_term += (-1j)**p *(n*(n+1) + v*(v+1) - p*(p+1))*a_func(m,n,-u,v,p)*spherical_hn(p, k*r)*Pnm(np.cos(theta))*np.exp(1j*(m-u)*phi)
    
    return normalization*factor*sum_term

def B_translation(m, n, u, v, r, theta, phi, k):
    factor = (-1)**u *1j**(v-n)*(2*v+1)/(2*v*(v+1))
    normalization = Emn(u,v,1)/Emn(m,n,1)

    sum_term = 0
    for p in range(np.abs(n-v), n+v+1):
        if np.abs(m-u) > p:
            continue
        else:
            Pnm = associated_legendre(p,m-u)
            sum_term += (-1j)**p *b_func(m,n,u,v,p)*spherical_hn(p, k*r)*Pnm(np.cos(theta))*np.exp(1j*(m-u)*phi)
    
    return normalization*factor*sum_term

class VSH_mode(enum.Enum):
    outgoing = enum.auto()
    incident = enum.auto()

def VSH(n, m, mode=VSH_mode.outgoing):
    """electric and magnetic vector spherical harmonic function

            n: int           order
            m: int           degree
            mode: VSH_mode   type of VSH (outgoing, incident)


       returns (N(r,θ,ϕ,k) -> [3,...], M(r,θ,ϕ,k) -> [3,...]), the 3 x,y,z components"""

    pi_f = pi_func(n,m)
    tau_f = tau_func(n,m)
    Pnm = associated_legendre(n,m)

    if mode is VSH_mode.outgoing:
        zn = spherical_hn
    elif mode is VSH_mode.incident:
        zn = special.spherical_jn
    else:
        raise TypeError('mode must be of enum type VSH_mode')
        
    def N(r, theta, phi, k):
        H = zn(n, k*r)
        Hp = zn(n, k*r, derivative=True)
        Pnm_val = Pnm(np.cos(theta))

        factor = (H + r*k*Hp)*np.exp(1j*m*phi)/(k*r)

        r_comp = n*(n+1)*Pnm_val*H/(k*r)*np.exp(1j*m*phi)
        theta_comp = tau_f(theta)*factor
        phi_comp = 1j*pi_f(theta)*factor

        return np.array([r_comp, theta_comp, phi_comp])

    def M(r, theta, phi, k):
        H = spherical_hn(n, k*r)
        factor = H*np.exp(1j*m*phi)

        theta_comp = 1j*pi_f(theta)*factor
        phi_comp = -1*tau_f(theta)*factor
        r_comp = 0*theta_comp      # no r-component, same shape

        return np.array([r_comp, theta_comp, phi_comp])

    return N,M


##### riccati needs to be verified with miepy #####

def riccati_1(n,z, derivative = False):
    jn = special.spherical_jn(n, z)

    if derivative:
        jn_p = special.spherical_jn(n, z, derivative=True)
        return z*jn_p + jn
    return z*jn

def riccati_2(n,z, derivative = False):
    yn = special.spherical_yn(n, z, derivative = derivative) 

    if derivative:
        yn_p = special.spherical_yn(n, z, derivative=True)
        return -z*yn_p - yn
    return -z*yn

def riccati_3(n,z, derivative = False):
    return riccati_2(n,z, derivative) - riccati_1(n,z, derivative)

###### below are pi,tau,VSH used in Mie theory, which may differ from those defined above ######

def pi_tau_func(n):
    # if np.sin(theta) == 0: return 0
    lpn = special.legendre(n)
    lpn_p = lpn.deriv()
    lpn_p2 = lpn_p.deriv()

    def pi_func(theta):
        return -1*lpn_p(np.cos(theta))
        # with np.errstate(divide='ignore', invalid='ignore'):
            # val = lpn(np.cos(theta))/np.sin(theta)
            # val[val == np.inf] = 0
            # val = np.nan_to_num(val)
            # return val

    def tau_func(theta):
        # val = -1*np.sin(theta)*lpn_p(np.cos(theta))
        val = -1*np.cos(theta)*lpn_p(np.cos(theta)) + np.sin(theta)**2*lpn_p2(np.cos(theta))
        return val

    return pi_func, tau_func 

class vector_spherical_harmonics:
    def __init__(self, n, superscript=3):
        self.pi_func, self.tau_func = pi_tau_func(n)
        self.n = n

        if superscript == 1:
            self.z_func = lambda x: special.spherical_jn(n,x)
            self.zp_func = lambda x: special.spherical_jn(n,x, derivative=True)
        elif superscript == 3:
            self.z_func = lambda x: spherical_hn(n,x)
            self.zp_func = lambda x: spherical_hn(n,x, derivative=True)

    def M_o1n(self, k):
        def f(r, theta, phi):
            theta_comp = np.cos(phi)*self.pi_func(theta)*self.z_func(k*r)
            phi_comp = -1*np.sin(phi)*self.tau_func(theta)*self.z_func(k*r)
            r_comp = np.zeros(shape = theta.shape, dtype=np.complex)
            return np.array([r_comp, theta_comp, phi_comp])
        return f

    def M_e1n(self, k):
        def f(r, theta, phi):
            theta_comp = -1*np.sin(phi)*self.pi_func(theta)*self.z_func(k*r)
            phi_comp = -1*np.cos(phi)*self.tau_func(theta)*self.z_func(k*r)
            r_comp = np.zeros(shape = theta.shape, dtype=np.complex)
            return np.array([r_comp, theta_comp, phi_comp])
        return f

    def N_o1n(self, k):
        def f(r, theta, phi):
            p = k*r
            theta_comp = np.sin(phi)*self.tau_func(theta)*(self.z_func(p) + p*self.zp_func(p))/p
            phi_comp = np.cos(phi)*self.pi_func(theta)*(self.z_func(p) + p*self.zp_func(p))/p
            r_comp = np.sin(phi)*self.n*(self.n+1)*np.sin(theta)*self.pi_func(theta)*self.z_func(p)/p
            return np.array([r_comp, theta_comp, phi_comp])
        return f

    def N_e1n(self, k):
        def f(r, theta, phi):
            p = k*r
            theta_comp = np.cos(phi)*self.tau_func(theta)*(self.z_func(p) + p*self.zp_func(p))/p
            phi_comp = -1*np.sin(phi)*self.pi_func(theta)*(self.z_func(p) + p*self.zp_func(p))/p
            r_comp = np.cos(phi)*self.n*(self.n+1)*np.sin(theta)*self.pi_func(theta)*self.z_func(p)/p
            return np.array([r_comp, theta_comp, phi_comp])
        return f

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    plt.figure(1)

    x = np.linspace(-1,1,1000)
    
    f = associated_legendre(2, 0)
    plt.plot(x, f(x), label = r'$P_2^0$')

    f = associated_legendre(2, 1)
    plt.plot(x, f(x), label = r'$P_2^1$')

    f = associated_legendre(2, 2)
    plt.plot(x, f(x), label = r'$P_2^2$')

    plt.legend()

    plt.figure(2)
    theta = np.linspace(0, np.pi, 1000)
    f = pi_func(2,1)
    plt.plot(theta, f(theta), label = r'$\pi_{2,1}$')
    f = tau_func(2,1)
    plt.plot(theta, f(theta), label = r'$\tau_{2,1}$')

    plt.legend()

    f1,f2 = VSH(2,1, VSH_mode.incident)

    r = np.array([10])
    theta = np.linspace(1e-6, np.pi-1e-6, 30)
    phi = np.linspace(0, 2*np.pi, 30)
    k = np.linspace(1,10,10)

    y = f1(*np.meshgrid(r,theta,phi,k, indexing='ij'))
    print(y.shape)
    y = f2(*np.meshgrid(r,theta,phi,k, indexing='ij'))
    print(y.shape)

    plt.show()
