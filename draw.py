import numpy as np
import matplotlib.pyplot as plt
from reconstruction import all_rec_points

# separate 30 reconstructed points
points_12 = all_rec_points[:12]
points_18 = all_rec_points[12:]
cuboid_points = points_18[:7]
pyramid_points = points_18[7:11]
cube_points = points_18[11:]

# plot a scatter 3D coordinate
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(+280, -280)
ax.set_ylim(+220, -220)
ax.set_zlim(0, 250)

# preparation to plot the plate
x_plate, y_plate, z_plate = zip(*points_12)
xp1, zp1 = np.meshgrid(np.linspace(0, 220, 100), np.linspace(0, 250, 100))
yp2, zp2 = np.meshgrid(np.linspace(0, 220, 100), np.linspace(0, 250, 100))
Xs1_plate = xp1.T
Ys1_plate = np.zeros((100, 100))
Zs1_plate = zp1.T
Xs2_plate = np.zeros((100, 100))
Ys2_plate = yp2.T
Zs2_plate = zp2.T

# draw points and surfaces of plate
ax.scatter3D(x_plate, y_plate, z_plate, depthshade=False, color='black')
ax.plot_surface(Xs1_plate, Ys1_plate, Zs1_plate, color='yellow', alpha=0.7)
ax.plot_surface(Xs2_plate, Ys2_plate, Zs2_plate, color='yellow', alpha=0.7)


# preparation to plot the cuboid
x_cuboid, y_cuboid, z_cuboid = zip(*cuboid_points)
order_cuboid = [0, 4, 5, 6, 2, 1, 0, 3, 5, 3, 2]  # 1,5,6,7,3,2,1,4,6,4,3
Xs_cuboid = [x_cuboid[i] for i in order_cuboid]
Ys_cuboid = [y_cuboid[i] for i in order_cuboid]
Zs_cuboid = [z_cuboid[i] for i in order_cuboid]

# draw points and lines of cuboid
ax.scatter3D(x_cuboid, y_cuboid, z_cuboid, depthshade=False, color='blue')
ax.plot_wireframe(np.asarray(Xs_cuboid), np.asarray(Ys_cuboid),
                  np.vstack((np.asarray(Zs_cuboid), np.asarray(Zs_cuboid))), color='blue')

# preparation to plot the pyramid
x_pyramid, y_pyramid, z_pyramid = zip(*pyramid_points)
order_pyramid = [3, 1, 0, 3, 2, 1]  # 11,9,8,11,10,9 --> 4,2,1,4,3,2
Xs_pyramid = [x_pyramid[i] for i in order_pyramid]
Ys_pyramid = [y_pyramid[i] for i in order_pyramid]
Zs_pyramid = [z_pyramid[i] for i in order_pyramid]

# draw points and lines of pyramid
ax.scatter3D(x_pyramid, y_pyramid, z_pyramid, depthshade=False, color='orange')
ax.plot_wireframe(np.asarray(Xs_pyramid), np.asarray(Ys_pyramid),
                  np.vstack((np.asarray(Zs_pyramid), np.asarray(Zs_pyramid))), color='orange')

# preparation to plot the cube
x_cube, y_cube, z_cube = zip(*cube_points)
order_cube = [0, 4, 5, 6, 2, 1, 0, 3, 5, 3, 2]  # 12,16,17,18,14,13,12,15,17,15,14
Xs_cube = [x_cube[i] for i in order_cube]
Ys_cube = [y_cube[i] for i in order_cube]
Zs_cube = [z_cube[i] for i in order_cube]

# draw points and lines of cube
ax.scatter3D(x_cube, y_cube, z_cube, depthshade=False, color='green')
ax.plot_wireframe(np.asarray(Xs_cube), np.asarray(Ys_cube),
                  np.vstack((np.asarray(Zs_cube), np.asarray(Zs_cube))), color='green')

# show the plot
ax.view_init(35, 45)
ax.set_xlabel('X', fontsize='large')
ax.set_ylabel('Y', fontsize='large')
ax.set_zlabel('Z', fontsize='large')
plt.savefig('world_reconstruction.jpg')
plt.show()

