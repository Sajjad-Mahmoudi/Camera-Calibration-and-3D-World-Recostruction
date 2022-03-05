import mouse_event
from calibration import calibration
import numpy as np

# store the M matrices in M_left, M_right for both left and right images
M_left, M_right = calibration.matrix_Ms[0], calibration.matrix_Ms[1]

# create M1T, M2T, and M3T by vertical stack
m3T_vector = np.vstack((M_left[2], M_left[2], M_right[2], M_right[2]))
m12T_vector = np.vstack((M_left[0], M_left[1], M_right[0], M_right[1]))

# reconstruct all 30 points simultaneously
def reconstruct_30():
    # create an object of mouse_event to store 30 points for "left.jpg" and "right.jpg"
    # and find the corresponding 3d coordinates
    rec_3D_30Points = []
    for index, image in enumerate(['left.jpg', 'right.jpg']):
        object_image = mouse_event.PointImage(image, 30)
        points_2d_corr = object_image.points_2d  # store 2D image points in the array "points_2d_corr"
        rec_3D_30Points.append(points_2d_corr)

    # store selected points from correspondence images separately
    imagePoint_left_corr, imagePoint_right_corr = rec_3D_30Points[0], rec_3D_30Points[1]

    # calculate 30 reconstructed 3D points
    rec_3D_Points_corr = []
    for i in range(30):
        both_points_vector_corr = np.vstack((imagePoint_left_corr[i, 0], imagePoint_left_corr[i, 1],
                                             imagePoint_right_corr[i, 0], imagePoint_right_corr[i, 1]))
        A = both_points_vector_corr * m3T_vector - m12T_vector
        U, S, V = np.linalg.svd(A)
        homo_3d_point_corr = V[-1, :]
        point_3d_corr = homo_3d_point_corr[:-1] / homo_3d_point_corr[-1]
        rec_3D_Points_corr.append(point_3d_corr)

    return rec_3D_Points_corr


# reconstruct 12 points on the plate
def reconstruct_12():
    # store 2D selected points in imagePoint_left and imagePoint_right
    # store real 3D points in real_3D_points
    imagePoint_left, imagePoint_right = calibration.matrix_imagePoints[0], calibration.matrix_imagePoints[1]
    real_3D_points = calibration.points_3d

    # create list to store reconstructed points
    rec_3D_points = []

    # calculate 12 reconstructed 3D points
    for i in range(12):
        both_points_vector = np.vstack((imagePoint_left[i, 0], imagePoint_left[i, 1],
                                        imagePoint_right[i, 0], imagePoint_right[i, 1]))

        A = both_points_vector * m3T_vector - m12T_vector
        U, S, V = np.linalg.svd(A)
        homo_3d_point = V[-1, :]
        point_3d = homo_3d_point[:-1] / homo_3d_point[-1]
        rec_3D_points.append(point_3d)

    # calculate mean square error between real and reconstructed 3D points
    mse = np.square(np.subtract(np.asarray(rec_3D_points), real_3D_points)).mean()

    return mse, rec_3D_points


# reconstruct 18 points of the shapes
def reconstruct_18():
    # create an object of mouse_event to store 18 points for "correspondence_left.jpg" and "correspondence_right.jpg"
    # and do the same to find the corresponding 3d coordinates
    rec_3D_18Points = []
    for index, image in enumerate(['correspondence_left.jpg', 'correspondence_right.jpg']):
        object_image = mouse_event.PointImage(image, 18)
        points_2d_corr = object_image.points_2d  # store 2D image points in the array "points_2d_corr"
        rec_3D_18Points.append(points_2d_corr)

    # store selected points from correspondence images separately
    imagePoint_left_corr, imagePoint_right_corr = rec_3D_18Points[0], rec_3D_18Points[1]

    # calculate 18 reconstructed 3D points
    rec_3D_Points_corr = []
    for i in range(18):
        both_points_vector_corr = np.vstack((imagePoint_left_corr[i, 0], imagePoint_left_corr[i, 1],
                                             imagePoint_right_corr[i, 0], imagePoint_right_corr[i, 1]))
        A = both_points_vector_corr * m3T_vector - m12T_vector
        U, S, V = np.linalg.svd(A)
        homo_3d_point_corr = V[-1, :]
        point_3d_corr = homo_3d_point_corr[:-1] / homo_3d_point_corr[-1]
        rec_3D_Points_corr.append(point_3d_corr)

    return rec_3D_Points_corr


if '__main__' == __name__:
    error, twelve = reconstruct_12()
    eighteen = reconstruct_18()
    all_rec_points = np.vstack((twelve, eighteen))
    print('\n\nMean Square Error =', error)
    print('All 30 reconstructed points:\n', all_rec_points)
else:
    all_rec_points = reconstruct_30()
