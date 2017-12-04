'''Visualize 3D orientation quaternions.
Not optimized for speed!

author: Thomas Haslwanter
date:   Nov-2016
ver:    0.1
'''

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d    
import matplotlib.animation as animation
import skinematics as skin

def show_orientation(quats, out_file=None, title_text=None, deltaT=100):
    '''Calculates the orienation of an arrow-patch used to visualize a quaternion.
    
    Parameters
    ----------
    quats : array [(N,3) or (N,4)]
            Quaterions describing the orientation.
    out_file : string
            Path- and file-name of the animated out-file ("*.mp4"). [Default=None]
    title_text : string
            Name of title of animation [Default=None]
    deltaT : int
            interval between frames [msec]. Smaller numbers make faster
            animations.
    
    '''
    
    # Initialize the 3D-figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Define the arrow-shape and the top/bottom colors
    delta = 0.01    # "Thickness" of arrow
    corners = [[0, 0, 0.6],
             [0.2, -0.2, 0],
             [0, 0, 0]]
    colors = ['r', 'b']
    
    # Calculate the arrow corners
    corner_array = np.column_stack(([*corners]))
    
    corner_arrays = []
    corner_arrays.append( corner_array + np.r_[0., 0., delta] )
    corner_arrays.append( corner_array - np.r_[0., 0., delta] )
    
    # Calculate the new orientations, given the quaternion orientation
    all_corners = []
    for quat in quats:
        all_corners.append([skin.vector.rotate_vector(corner_arrays[0], quat), 
                            skin.vector.rotate_vector(corner_arrays[1], quat)])
        
    # Animate the whole thing, using 'update_func'
    num_frames = len(q)
    ani = animation.FuncAnimation(fig, _update_func, num_frames,
                                  fargs=[all_corners, colors, ax, title_text],
                                  interval=deltaT)
    
    # If requested, save the animation to a file
    if out_file is not None:
        ani.save(out_file)
        print('Animation saved to {0}'.format(out_file))
    
    plt.show()    
    
    return

def _update_func(num, all_corners, colors, ax, title=None):
    '''For 3D plots it seems to be impossible to only re-set the data values,
    so the plot has to be cleared and re-generated for each frame
    '''
    
    # Clear previous plot
    ax.clear()

    # Plot coordinate axes
    ax.plot([-1, 1], [0, 0], [0, 0])
    ax.plot([0, 0], [-1, 1], [0, 0])
    ax.plot([0, 0], [0, 0], [-1, 1])
    
    # Format the plot
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.xlabel('x')
    plt.ylabel('y')
    
    try:
        # Plot and color the top- and bottom-arrow
        for up_down in range(2):
            corners = all_corners[num][up_down]
            ph = ax.plot_trisurf(corners[:,0], corners[:,1], corners[:,2])
            ph.set_color(colors[up_down])
        
        if title is not None:
            plt.title(title)
        
    except RuntimeError:
        # When the triangle is exactly edge-on "plot_trisurf" seems to have a numerical problem
        print('Cannot show triangle edge-on!')
    return


if __name__ == '__main__':
    
    # Set the parameters
    omega = np.r_[0, 10, 10]     # [deg/s]
    duration = 2
    rate = 100
    q0 = [1, 0, 0, 0]
    out_file = 'demo_patch.mp4'
    title_text = 'Rotation Demo'
    
    ## Calculate the orientation
    dt = 1./rate
    num_rep = duration*rate
    omegas = np.tile(omega, [num_rep, 1])
    q = skin.quat.vel2quat(omegas, q0, rate, 'sf')
        
    show_orientation(q)
    show_orientation(q, out_file, 'Well done!')
