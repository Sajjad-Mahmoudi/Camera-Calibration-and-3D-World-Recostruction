# importing the modules
import cv2
import numpy as np


# function to display the coordinates of the points clicked on the image
class PointImage:
	def __init__(self, image_name, num_points=12):
		self.num_points = num_points
		self.points_2d = np.zeros((num_points, 2))  # store coordinates of mouse click on image
		self.counter = 0
		self.img = cv2.imread(image_name, 1)  # reading the image
		cv2.imshow('image', self.img)  # displaying the image

		# setting mouse handler for the image and calling the click_event() function
		cv2.setMouseCallback('image', self.click_event)

		cv2.waitKey(0)  # wait for a key to be pressed to exit
		cv2.destroyAllWindows()  # close the window

	def click_event(self, event, x, y, flags, params):
		# checking for left mouse clicks
		if event == cv2.EVENT_LBUTTONDOWN:
			if self.counter < self.num_points:
				self.points_2d[self.counter] = x, y  # store coordinates of image into the matrix
				self.counter += 1
			if '__main__' == __name__:
				print(x, ' ', y)  # displaying the coordinates on the Shell

			# displaying the coordinates on the image window
			font = cv2.FONT_HERSHEY_SIMPLEX
			cv2.putText(self.img, str(x) + ',' + str(y), (x, y), font, 0.25, (0, 75, 0), 1)
			cv2.imshow('image', self.img)


# test = PointImage('correspondence_left.jpg', 18)
