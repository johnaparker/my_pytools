import numpy as np
from .interpolate import ndinterp

def axis_angle(u, theta):
    """Create rotation matrix using angle-axis method
            u[3]        axis vector
            theta       angle           """
    u = np.asarray(u)
    u = u/np.linalg.norm(u)
    ct = np.cos(theta)
    st = np.sin(theta)
    ux,uy,uz = u

    rot_matrix = np.array([ [ct + ux**2*(1-ct),    ux*uy*(1-ct) - uz*st, ux*uz*(1-ct) + uy*st  ],
                            [ux*uy*(1-ct) + uz*st, ct + uy**2*(1-ct)   , uy*uz*(1-ct) - ux*st],
                            [uz*ux*(1-ct) - uy*st, uz*uy*(1-ct) + ux*st, ct + uz**2*(1-ct)    ]   ])
    return rot_matrix

def rotate_to(vec_from, vec_to):
    """Create rotation matrix using angle-axis method
            vec_from[3]     initial orientation
            vec_to[3]       final orientation       """
    vec_to = np.asarray(vec_to)
    vec_to = vec_to/np.linalg.norm(vec_to)
    vec_from = np.asarray(vec_from)
    vec_from = vec_from/np.linalg.norm(vec_from)
    
    theta = np.arccos( np.dot(vec_to, vec_from) )
    u = np.cross(vec_from, vec_to)
    return axis_angle(u,theta)

def rotate_discrete_data(sig, theta, phi, vec_from, vec_to):
    """Rotate an interpolated function to a primed system
            sig_1(theta,phi)        function to rotate
            theta[N]                values of theta (from 0 to pi, uniform or non-uniform)
            phi[N]                  values of phi (from 0 to 2*pi, uniform or non-uniform)
            vec_from[3]             initial orientation
            vec_to[3]               final orientation       

       Returns interpolated function in the primed coordiate system, sig'(theta,phi)"""

    theta_mesh, phi_mesh = np.meshgrid(theta, phi, indexing='ij')
    R = sig(theta_mesh, phi_mesh)

    X = R*np.sin(theta_mesh)*np.cos(phi_mesh)
    Y = R*np.sin(theta_mesh)*np.sin(phi_mesh)
    Z = R*np.cos(theta_mesh)

    rot = rotate_to(vec_from = vec_from, vec_to = vec_to)
    trans = np.tensordot(rot,np.array([X,Y,Z]), axes=(1,0))
    X_p,Y_p,Z_p = trans

    phi_p = np.arctan2(Y_p,X_p)
    phi_p[phi_p < 0] += 2*np.pi
    R_p = (X_p**2 + Y_p**2 + Z_p**2)**.5
    eps = 1e-30
    theta_p = np.arccos(Z_p/(R_p + eps))

    R = sig(theta_p, phi_p)
    return ndinterp(R, theta, phi)
