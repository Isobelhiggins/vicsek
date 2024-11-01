import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

# parameters
L = 10.0 # size of box
rho = 1.0 # density
N = int(rho * L**2) # number of particles
print("N", N)

r0 = 1.0 # interaction radius
deltat = 1.0 # time step
factor = 0.5
v0 = r0 / deltat * factor # velocity
iterations = 200 # animation frames
eta = 0.15 # noise/randomness

# initialise positions and angles
positions = np.random.uniform(0, L, size = (N, 2))
angles = np.random.uniform(-np.pi, np.pi, size = N) # from 0 to 2pi rad

# define barrier position and size
barrier_x_start, barrier_x_end = 3, 7
barrier_y_start, barrier_y_end = 3, 7

# ensure particles are not generated inside the barrier
positions = np.zeros((N, 2))
for i in range(N):
    position = np.random.uniform(0, L, size = 2)
    while barrier_x_start <= position[0] <= barrier_x_end and barrier_y_start <= position[1] <= barrier_y_end:
        position = np.random.uniform(0, L, size = 2)
    positions[i] = position

def barrier_collision(position, angle):
    # calculate next position based on current position and angle
    next_position = position + v0 * np.array([np.cos(angle), np.sin(angle)]) * deltat
    
    # check if next position is at the barrier
    if barrier_x_start <= next_position[0] <= barrier_x_end and barrier_y_start <= next_position[1] <= barrier_y_end:
        return position # return current position when it hit the barrier
    else:
        return next_position # continue updating position if not at barrier

def animate(frames):
    print(frames)
    
    global positions, angles
    # empty arrays to hold updated positions and angles
    new_positions = np.empty_like(positions)
    new_angles = np.empty_like(angles)
    
    # loop over all particles
    for i in range(N):
        # list of angles of neighbouring particles
        neighbour_angles = []
        # distance to other particles
        for j in range(N):
            distance = np.linalg.norm(positions[i] - positions[j])
            # if within interaction radius add angle to list
            if distance < r0:
                neighbour_angles.append(angles[j])
         
        # if there are neighbours, calculate average angle and noise/randomness       
        if neighbour_angles:
            average_angle = np.mean(neighbour_angles)
            noise = eta * np.random.uniform(-np.pi, np.pi)
            new_angles[i] = average_angle + noise # updated angle with noise
        else:
            # if no neighbours, keep current angle
            new_angles[i] = angles[i]
        
        # update position with barrier collision check
        new_positions[i] = barrier_collision(positions[i], new_angles[i])
        # boundary conditions of box
        new_positions[i] %= L
        
    # update global variables
    positions = new_positions
    angles = new_angles
    
    # plotting
    qv.set_offsets(positions)
    qv.set_UVC(np.cos(angles), np.sin(angles), angles)
    return qv,
 
fig, ax = plt.subplots(figsize = (6, 6))  
 
qv = ax.quiver(positions[:,0], positions[:,1], np.cos(angles), np.sin(angles), angles, clim = [-np.pi, np.pi], cmap = "hsv")
ax.add_patch(plt.Rectangle((barrier_x_start, barrier_y_start), barrier_x_end - barrier_x_start, barrier_y_end - barrier_y_start, color = "grey", alpha = 0.5))
ax.set_title(f"Vicsek model for {N} particles with an attractive barrier, using for loops")
anim = FuncAnimation(fig, animate, frames = range(1, iterations), interval = 5, blit = True)
writer = FFMpegWriter(fps = 10, metadata = dict(artist = "Isobel"), bitrate = 1800)
anim.save("Vicsek_loops_barrier.mp4", writer = writer, dpi = 100)
plt.show()