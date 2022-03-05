Considerations to be taken into account for execution:
    1. Please read explanation part below before executing the module(s)
    2. You don't need to run "mouse_event.py", "calibration.py", or "reconstruction.py" module, unless you want to try
       or print related each part information separately. You can have all exercise done only by executing "draw.py"
       module (you need to select points using left mouse click and finish the running/current window by clicking some
       button).
    3. In "calibration.py" module, please uncomment the lines 24 if you don't have  "world_points.txt" in "exercise_1"
       folder
    4. You can execute the "draw.py" or other modules in terminal using the commands below:
       python draw.py

Explanation for each module:
    a) "mouse_event.py": performs selecting point on image. If you run it directly, it prints each selected point
        coordinate on console and stores them in the "points_2d" array
    b) "calibration.py": modifies the "calibration_points3.txt" file by removing the blank lines and stores the modified
        text file in "world_points.txt", and performs the camera calibration task and draw the coordinates on left and
        right images and save them as "coordinates_left.jpg" and "coordinates_right.jpg". If you run it directly,
        you can print M, K, R, and T matrices for both left and right images
    c) "reconstruction.py": performs world point reconstructions. If you run it directly, you can see MSE and 30
        reconstructed point coordinate on console. Note that you need to select 12 points and then select 18
        points of shapes
    d) "draw.py": performs drawing the reconstructed points and the corresponding shapes, storing the image in
        "world_reconstruction.jpg". Note that when running it,you need to select the 12 points and then all 30 points
        (Attention: for selecting 30 points, you select them from "left.jpg" and "right.jpg" images because they are
         higher quality photos, so pay attention to the order)

Please note if you have problems in terms of path/directory, please overwrite the addresses such as "left.jpg"
or "right.jpg" with absolute path or path from content root


