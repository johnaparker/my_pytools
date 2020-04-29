import numpy as np
import matplotlib as mpl
from itertools import cycle
import quaternion

def trajectory_animation_3d(coordinates, orientations, shape, properties, colors=['C0'], trail=None, axes=False, axes_length=1, grid=False):
    """Create a 3D trajectory animation with VPython
        
        Arguments:
            coordinates[T,N,3]         particle x,y,z coordinates 
            orientations[T,N,4]        particle orientations (as quaternions)
            colors                     list of colors to cycle through
            shape[N]                   list of vpython shape classes for N particles (alternative size: CONST)
            properties[N]              list of dictionaries containing shape properties for N particles (alternative size: CONST)
            trail                      length of particle trail (default: no trail)
            axes                       include x,y,z axes for each particle (default: False)
            axes_length                length of axes, if set (default: 1)
    """

    import vpython
    vec = vpython.vector

    coordinates = np.asarray(coordinates)
    orientations = np.asarray(orientations)
    color_cycle = cycle(colors)

    make_trail = False if trail is None else True

    scene = vpython.canvas(background=vec(1,1,1))
    objs = []
    arrows = []
    trails = []

    for i in range(coordinates.shape[1]):
        color = vec(*mpl.colors.to_rgb(next(color_cycle)))
        pos = vec(*coordinates[0,i])
        # particle = shape[i](pos=pos, color=color,
                   # make_trail=make_trail, retain=trail, opacity=0.4, **properties[i])
        particle = shape[i](pos=pos, color=color,
                   opacity=0.4, **properties[i])
        objs.append(particle)

        if make_trail:
            def my_center(num):
                def center():
                    return objs[num].pos + objs[num].axis/2
                return center
            trails.append(vpython.attach_trail(my_center(i), color=color, retain=trail))


        if axes:
            arrow_x = vpython.arrow(pos=pos, axis=vec(1,0,0), scale=axes_length, color=vec(0,0,0),
                          shaftwidth=5)
            arrow_y = vpython.arrow(pos=pos, axis=vec(0,1,0), scale=axes_length, color=vec(0,0,0),
                          shaftwidth=5)
            arrow_z = vpython.arrow(pos=pos, axis=vec(0,0,1), scale=axes_length, color=vpython.color.red,
                          shaftwidth=5)

            arrows.append([arrow_x, arrow_y, arrow_z])


    for i,obj in enumerate(objs):
        rot = quaternion.as_rotation_matrix(orientations[0,i])
        a = obj.axis
        b = vec(*rot[:,2])
        a /= vpython.mag(a)
        b /= vpython.mag(b)
        axis = vpython.cross(a,b)
        angle = vpython.acos(vpython.dot(a,b))
        obj.rotate(angle=angle, axis=axis, origin=obj.pos + obj.axis/2)
        obj.pos -= obj.axis/2
        if axes:
            for j,arrow in enumerate(arrows[i]):
                arrow.pos = vec(*coordinates[0,i])
                arrow.axis = vec(*rot[:,j])*arrow.scale

    if grid:
        vpython.arrow(pos=vpython.vector(0,0,0), axis=vpython.vector(300,0,0), shaftwidth=2, color=vpython.color.black)
        vpython.arrow(pos=vpython.vector(0,0,0), axis=vpython.vector(0,300,0), shaftwidth=2, color=vpython.color.black)
        vpython.arrow(pos=vpython.vector(0,0,0), axis=vpython.vector(0,0,300), shaftwidth=2, color=vpython.color.black)

    for t in range(1,coordinates.shape[0]):
        if t == 2:
            scene.waitfor('click')
        for i,obj in enumerate(objs):
            rot = quaternion.as_rotation_matrix(orientations[t,i])

            a = obj.axis
            b = vec(*rot[:,2])
            a /= vpython.mag(a)
            b /= vpython.mag(b)
            axis = vpython.cross(a,b)
            angle = vpython.acos(vpython.dot(a,b))
            obj.rotate(angle=angle, axis=axis, origin=obj.pos + obj.axis/2)
            
            if shape[i] in (vpython.cylinder, vpython.arrow, vpython.cone, vpython.pyramid):
                obj.pos = vec(*coordinates[t,i]) - obj.axis/2
            else:
                obj.pos = vec(*coordinates[t,i])
            if axes:
                for j,arrow in enumerate(arrows[i]):
                    arrow.pos = vec(*coordinates[t,i])
                    arrow.axis = vec(*rot[:,j])*arrow.scale

        vpython.rate(30)
    for trail in trails:
        trail.clear()

if __name__ == '__main__':
    import vpython

    coordinates = np.zeros([100, 2, 3])
    orientations = np.ones([100,2], dtype=np.quaternion)
    shape = [vpython.sphere]*2
    properties = [{'radius': 5}]*2

    coordinates[:,0,0] = np.linspace(10, 100, 100)
    coordinates[:,1,0] = -np.linspace(10, 100, 100)

    trajectory_animation_3d(coordinates, orientations, shape, properties)
    
