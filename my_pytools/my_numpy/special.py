"""
special defines any additional special functions on top of scipy.special
"""

import numpy as np
import sympy
from scipy import special


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

def VSH_magnetic_scat(n, m):
    """magnetic vector spherical harmonic function

            n: int         order
            m: int         degree

       returns M(r,θ,ϕ,k) -> [3,...] array, the 3 x,y,z components   """
 
    pi_f = pi_func(n,m)
    tau_f = tau_func(n,m)

    def M(r, theta, phi, k):
        H = spherical_hn(n, k*r)
        factor = H*np.exp(1j*m*phi)

        theta_comp = 1j*pi_f(theta)*factor
        phi_comp = -1*tau_f(theta)*factor
        r_comp = 0*theta_comp      # no r-component, same shape

        return np.array([r_comp, theta_comp, phi_comp])

    return M

def VSH_electric_scat(n, m):
    """electric vector spherical harmonic function

            n: int         order
            m: int         degree

       returns N(r,θ,ϕ,k) -> [3,...] array, the 3 x,y,z components   """

    pi_f = pi_func(n,m)
    tau_f = tau_func(n,m)
    Pnm = associated_legendre(n,m)

    def N(r, theta, phi, k):
        H = spherical_hn(n, k*r)
        Hp = spherical_hn(n, k*r, derivative=True)
        Pnm_val = Pnm(np.cos(theta))

        factor = (H + r*k*Hp)*np.exp(1j*m*phi)/(k*r)

        r_comp = n*(n+1)*Pnm_val*H/(k*r)*np.exp(1j*m*phi)
        theta_comp = tau_f(theta)*factor
        phi_comp = 1j*pi_f(theta)*factor

        return np.array([r_comp, theta_comp, phi_comp])

    return N

def riccati_1(nmax,x):
    """Riccati bessel function of the 1st kind

       returns (r1, r1'), n=0,1,...,nmax"""

    jn,jnp = special.sph_jn(nmax,x)

    r0 = x*jn
    r1 = jn + x*jnp
    return np.array([r0,r1])

def riccati_2(nmax,x):
    """Riccati bessel function of the 2nd kind

       returns (r2, r2'), n=0,1,...,nmax"""

    jn,jnp,yn,ynp = special.sph_jnyn(nmax,x)
    hn = jn + 1j*yn
    hnp = jnp + 1j*ynp

    r0 = x*hn
    r1 = hn + x*hnp
    return np.array([r0,r1])

def riccati_3(nmax,x):
    """Riccati bessel function of the 3rd kind

       returns (r3, r3'), n=0,1,...,nmax"""

    yn,ynp = special.sph_yn(nmax,x)

    r0 = x*yn
    r1 = yn + x*ynp
    return np.array([r0,r1])

def riccati_1_single(n,x):
    """Riccati_1, but only a single n value"""
    pre = (np.pi*x/2)**.5
    jn = pre*special.jv(n+0.5,x)
    jnp = jn/(2*x) + pre*special.jvp(n+0.5,x)

    return np.array([jn,jnp])

def riccati_2_single(n,x):
    """Riccati_2, but only a single n value"""
    pre = (np.pi*x/2)**.5
    hn = pre*special.hankel1(n+0.5,x)
    hnp = hn/(2*x) + pre*special.h1vp(n+0.5,x)

    return np.array([hn,hnp])

def riccati_3_single(n,x):
    """Riccati_3, but only a single n value"""
    # pre = (np.pi*x/2)**.5
    # yn = pre*special.yv(n+0.5,x)
    # ynp = yn/(2*x) + pre*special.yvp(n+0.5,x)

    # return np.array([yn,ynp])
    return riccati_2_single(n,x) - riccati_1_single(n,x)



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

    f1 = VSH_magnetic_scat(2,1)
    f2 = VSH_electric_scat(2,1)

    r = np.array([10])
    theta = np.linspace(0, np.pi, 30)
    phi = np.linspace(0, 2*np.pi, 30)
    k = np.linspace(1,10,10)

    y = f1(*np.meshgrid(r,theta,phi,k, indexing='ij'))
    print(y.shape)
    y = f2(*np.meshgrid(r,theta,phi,k, indexing='ij'))
    print(y.shape)

    plt.show()
