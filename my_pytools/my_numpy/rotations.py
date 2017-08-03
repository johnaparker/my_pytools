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

def rotation_matrix_2d(angle):
    """Return a 2x2 rotation matrix by angle (radians)"""

    return np.array([ [np.cos(angle), -np.sin(angle)],
                      [np.sin(angle), np.cos(angle)] ])

def clip(data, domain):
    """clip data so that it falls in the range of a linear domain"""
    max_val = np.max(domain)
    min_val = np.min(domain)
    data[data>max_val] = max_val
    data[data<min_val] = min_val

def rotate_vector_field_2d(angle, data, r, phi, method = "linear", color = None):
    """Rotate a 2d vector field. Return the rotated data.
            
            angle           angle to rotate by
            data[2,N1,N2]   vector field
            r[N1]           linear array of radial domain
            phi[N1]         linear array of phi domain
            method          one of ['linear', 'nearest']; the interpolation method to be used. Defaults to linear
            color[N1,N2]    (optional) color data            """

    # rotate vectors
    data = np.asarray(data)
    r = np.asarray(r)
    phi = np.asarray(phi)

    U = data[0,...]
    V = data[1,...]
    Rot = rotation_matrix_2d(angle)
    U,V = np.einsum('ij,j...->i...', Rot, np.array([U,V]))

    # construct R, PHI in rotated (primed) coordinates
    R,PHI = np.meshgrid(r,phi, indexing='ij')
    X = R*np.cos(PHI)
    Y = R*np.sin(PHI)
    Xp,Yp = np.einsum('ij,j...->i...', Rot.T, np.array([X,Y]))

    Rp = np.sqrt(Xp**2 + Yp**2)
    PHIp = np.arctan2(Yp,Xp) 
    PHIp[PHIp<0] += 2*np.pi
    
    # clip data so that interpolation doesn't produce nan's for out of bounds domain
    clip(Rp, r)
    clip(PHIp, phi)

    if len(r) == 1:
        args = (phi,)
        args_p = (PHIp.squeeze(),)
        U,V = map(np.squeeze, [U,V])
    else:
        args = r,phi
        args_p = Rp,PHIp

    # rotate position of vectors using interpolation
    fU = ndinterp(U,*args, method=method)
    U = fU(*args_p)
    fV = ndinterp(V,*args, method=method)
    V = fV(*args_p)

    if color is not None:
        fC = ndinterp(color,r,phi, method=method)
        C = fC(Rp, PHIp)
        return np.array([U,V,C])

    return np.array([U,V])

def rotate_vector_field_3d(rot_matrix, data, r, theta, phi, method = 'linear', color = None):
    """Rotate a 3d vector field. Return the rotated data.
            
            rot_matrix[3,3]    3d rotation matrix
            data[3,N1,N2,N3]   vector field
            r[N1]              linear array of radial domain
            theta[N2]          linear array of theta domain
            phi[N3]            linear array of phi domain
            method             one of ['linear', 'nearest']; the interpolation method to be used. Defaults to linear
            color[N1,N2,N3]    (optional) color data            """

    # rotate position of vectors
    data = np.asarray(data)
    r = np.asarray(r)
    theta = np.asarray(theta)
    phi = np.asarray(phi)

    U = data[0,...]
    V = data[1,...]
    W = data[2,...]

    # U,V,W = np.einsum('ij,j...->i...', Rot, np.array([U,V,W]))

    # construct R, THETA, PHI in rotated (primed) coordinates
    R,THETA,PHI = np.meshgrid(r,theta,phi, indexing='ij')
    X = R*np.sin(THETA)*np.cos(PHI)
    Y = R*np.sin(THETA)*np.sin(PHI)
    Z = R*np.cos(THETA)
    Xp,Yp,Zp = np.einsum('ij,j...->i...', rot_matrix, np.array([X,Y,Z]))

    Rp = np.sqrt(Xp**2 + Yp**2 + Zp**2)
    THETAp = np.arccos(Zp/Rp)
    PHIp = np.arctan2(Yp,Xp) 
    PHIp[PHIp<0] += 2*np.pi
    
    # clip data so that interpolation doesn't produce nan's for out of bounds domain
    clip(Rp, r)
    clip(THETAp, theta)
    clip(PHIp, phi)


    # rotate vectors using interpolation
    if len(r) == 1:
        args = theta,phi
        args_p = THETAp.squeeze(),PHIp.squeeze()
        U,V,W = map(np.squeeze, [U,V,W])
    else:
        args = r,theta,phi
        args_p = Rp,THETAp,PHIp

    fU = ndinterp(U,*args, method=method)
    U = fU(*args_p)
    fV = ndinterp(V,*args, method=method)
    V = fV(*args_p)
    fW = ndinterp(W,*args, method=method)
    W = fW(*args_p)

    xhat = np.array([np.sin(THETA)*np.cos(PHI), np.cos(THETA)*np.cos(PHI), -np.sin(PHI)])
    yhat = np.array([np.sin(THETA)*np.sin(PHI), np.cos(THETA)*np.sin(PHI), np.cos(PHI)])
    zhat = np.array([np.cos(THETA), -np.sin(THETA), np.zeros_like(THETA)])

    rhat_p = np.array([np.sin(THETAp)*np.cos(PHIp), np.sin(THETAp)*np.sin(PHIp), np.cos(THETAp)])
    that_p = np.array([np.cos(THETAp)*np.cos(PHIp), np.cos(THETAp)*np.sin(PHIp), -np.sin(THETAp)])
    phat_p = np.array([-np.sin(PHIp), np.cos(PHIp), np.zeros_like(THETAp)])

    U,V,W = U*rhat_p + V*that_p + W*phat_p
    U,V,W = np.einsum('ij,j...->i...', rot_matrix.T, np.array([U,V,W]))
    U,V,W = U*xhat + V*yhat + W*zhat

    if len(r) == 1:
        U,V,W = map(np.squeeze, [U,V,W])

    if color is not None:
        fC = ndinterp(color,*args, method=method)
        C = fC(*args_p)
        return np.array([U,V,W,C])

    return np.array([U,V,W])

if __name__ == "__main__":
    # test rotate_vector_field_2d
    phi = np.linspace(0,2*np.pi,20)
    r = np.linspace(1,5,5)

    R,PHI = np.meshgrid(r,phi, indexing='ij')
    X = R*np.cos(PHI)
    Y = R*np.sin(PHI)

    U = np.zeros_like(X)
    V = np.ones_like(X)

    V[X<0] *= -1
    C = np.zeros(shape = U.shape)
    C[X<0] = .2

    fig, axes = plt.subplots(ncols=2, figsize=plt.figaspect(1/2))
    axes[0].quiver(X,Y,U,V,C, pivot='mid', cmap = 'bwr')
    axes[0].set_aspect('equal')

    angle = np.pi/8
    U,V,C = rotate_vector_field_2d(angle, [U,V], r, phi, color=C, method="nearest")
    axes[1].quiver(X,Y,U,V,C, pivot='mid', cmap = 'bwr')
    axes[1].set_aspect('equal')

    # test rotate_vector_field_3d
    r = np.array([1])
    theta = np.linspace(0,np.pi,20)
    phi = np.linspace(0,2*np.pi,20)

    R,THETA,PHI = np.meshgrid(r,theta,phi, indexing='ij')
    U = np.zeros_like(THETA)
    V = np.sin(THETA)
    W = np.zeros_like(THETA)

    fig, axes = plt.subplots(ncols=2, figsize=plt.figaspect(1/2.5))
    axes[0].pcolormesh(THETA.squeeze(), PHI.squeeze(), np.abs(V.squeeze())**2, shading='gouraud')
    axes[0].quiver(THETA.squeeze(), PHI.squeeze(), V.squeeze(),W.squeeze(), color='black')

    Rot = rotate_to([0,0,1],[1,0,0])
    U,V,W = rotate_vector_field_3d(Rot, [U,V,W], r, theta, phi)
    axes[1].pcolormesh(THETA.squeeze(), PHI.squeeze(), np.abs(V.squeeze())**2 + np.abs(W.squeeze())**2 + np.abs(U.squeeze())**2, shading='gouraud')

    axes[1].quiver(THETA.squeeze(), PHI.squeeze(), V.squeeze(),W.squeeze(), color='black')

    plt.show()
