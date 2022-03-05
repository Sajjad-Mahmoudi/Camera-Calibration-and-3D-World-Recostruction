import mouse_event
import numpy as np
import cv2


class Calculations:

    def __init__(self):
        # axis coordinates of homogenous scene
        axis_length = 200  # the number of pixels to draw the axes on image
        self.homo_origin_scene = [0, 0, 0, 1]
        self.homo_x_scene = [axis_length, 0, 0, 1]
        self.homo_y_scene = [0, axis_length, 0, 1]
        self.homo_z_scene = [0, 0, axis_length, 1]

        # create 4 lists to be filled with M, K, R, T, and image points for each image
        self.matrix_Ms = []
        self.matrix_Ks = []
        self.matrix_Rs = []
        self.matrix_Ts = []
        self.matrix_imagePoints = []

        # uncomment the line 24
        # self.modify_txt_file()
        self.points_3d = np.loadtxt('world_points.txt')  # store the coordinates of 3d points into "points_3d" array
        self.points_3d_withOne = np.insert(self.points_3d, 3, 1, axis=1)  # add a column of ones to "points_3d"
        self.calc()

    def modify_txt_file(self):
        with open("calibration_points3.txt", "r") as f, open("world_points.txt", "w") as outFile:
            for line in f.readlines():
                if not line.strip():
                    continue
                if line:
                    outFile.write(line)

    def calc(self):
        for index, image in enumerate(['left.jpg', 'right.jpg']):

            # create an instance of class "PointImage" from "mouse_event" module
            object_image = mouse_event.PointImage(image)
            points_2d = object_image.points_2d  # store 2D image points in the array "points_2d"
            self.matrix_imagePoints.append(points_2d)

            # create "all_points" list containing coefficients for each point, shape= (24, 12)
            all_points = []
            for i in range(len(self.points_3d_withOne)):
                add_ui = np.array(self.points_3d[i] * points_2d[i][0])
                add_vi = np.array(self.points_3d[i] * points_2d[i][1])
                row_ui = np.concatenate((self.points_3d_withOne[i], np.zeros(4), -add_ui, -points_2d[i][0]), axis=None)
                row_vi = np.concatenate((np.zeros(4), self.points_3d_withOne[i], -add_vi, -points_2d[i][1]), axis=None)
                all_points.append(row_ui)
                all_points.append(row_vi)

            # calculate U, S, and V matrices
            U, S, V = np.linalg.svd(np.asarray(all_points))

            # calculate M matrix
            M = V[-1, :].reshape((3, 4))
            self.matrix_Ms.append(M)

            # axis coordinates of homogenous image and corresponding converted points from homogenous coordinates
            homo_origin_image = np.matmul(M, np.asarray(self.homo_origin_scene))
            conv_origin_image = homo_origin_image[:2] / homo_origin_image[2]
            homo_x_image = np.matmul(M, np.asarray(self.homo_x_scene))
            conv_x_image = homo_x_image[:2] / homo_x_image[2]
            homo_y_image = np.matmul(M, np.asarray(self.homo_y_scene))
            conv_y_image = homo_y_image[:2] / homo_y_image[2]
            homo_z_image = np.matmul(M, np.asarray(self.homo_z_scene))
            conv_z_image = homo_z_image[:2] / homo_z_image[2]

            # draw the axes coordinates on image
            im = cv2.imread(image)
            cv2.line(im, (int(conv_origin_image[0]), int(conv_origin_image[1])),
                     (int(conv_x_image[0]), int(conv_x_image[1])),
                     (0, 255, 0), thickness=2)
            cv2.line(im, (int(conv_origin_image[0]), int(conv_origin_image[1])),
                     (int(conv_y_image[0]), int(conv_y_image[1])),
                     (0, 255, 0), thickness=2)
            cv2.line(im, (int(conv_origin_image[0]), int(conv_origin_image[1])),
                     (int(conv_z_image[0]), int(conv_z_image[1])),
                     (0, 255, 0), thickness=2)
            cv2.imwrite('coordinates_' + image, im)
            cv2.imshow('Image with coordinates', im)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            # estimate the intrinsic and extrinsic parameters
            r3 = M[2, 0:2]
            cx = np.dot(M[0, 0:2], M[2, 0:2])
            cy = np.dot(M[1, 0:2], M[2, 0:2])
            fx = np.linalg.norm(np.cross(M[0, 0:2], M[2, 0:2]))
            fy = np.linalg.norm(np.cross(M[1, 0:2], M[2, 0:2]))
            r1 = (M[0, 0:2] - cx * M[2, 0:2]) / fx
            r2 = (M[1, 0:2] - cy * M[2, 0:2]) / fy
            tx = (M[0, 3] - cx * M[2, 3]) / fx
            ty = (M[1, 3] - cy * M[2, 3]) / fy
            tz = M[2, 3]

            # obtain K, R, and T matrices
            K = np.array([fx, 0, cx, 0, fy, cy, 0, 0, 1]).reshape((3, 3))
            R = np.vstack((r1, r2, r3))
            T = np.array([tx, ty, tz])
            self.matrix_Ks.append(K)
            self.matrix_Rs.append(R)
            self.matrix_Ts.append(T)

    def __str__(self):
        return 'M_left:\n' + str(np.asarray(self.matrix_Ms[0])) + '\nK_left:\n' + str(np.asarray(self.matrix_Ks[0])) +\
            '\nR_left:\n' + str(np.asarray(self.matrix_Rs[0])) + '\nT_left:\n' + str(np.asarray(self.matrix_Ts[0])) +\
            '\n\nM_right:\n' + str(np.asarray(self.matrix_Ms[1])) + '\nK_right:\n' + str(np.asarray(self.matrix_Ks[1])) +\
            '\nR_right:\n' + str(np.asarray(self.matrix_Rs[1])) + '\nT_right:\n' + str(np.asarray(self.matrix_Ts[1]))


if '__main__' == __name__:
    calibration = Calculations()
    print('\n\n')
    print(calibration.__str__())
else:
    calibration = Calculations()
