import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"  # Reduces camera load time SIGNIFICANTLY
import tkinter as tk
import cv2


root=tk.Tk()

# Small default values for testing
reps = 5
rest = 10
sets = 3

reps_var = tk.IntVar(value=reps)  # how many are performed before the rest interval
rest_var = tk.IntVar(value=rest)  # how long the person rests before the next repetition starts. The rest interval is specified in seconds
sets_var = tk.IntVar(value=sets)  # how many groups of repetitions will be performed

def start():
    global reps, rest, sets
    reps = reps_var.get()
    rest = rest_var.get()
    sets = sets_var.get()
    root.quit()  # stop blocking on input


# Labels
reps_label = tk.Label(root, text='Reps')
rest_label = tk.Label(root, text='Rest')
sets_label = tk.Label(root, text='Sets')

# Entries
reps_entry = tk.Entry(root, textvariable=reps_var, )
rest_entry = tk.Entry(root, textvariable=rest_var)
sets_entry = tk.Entry(root, textvariable=sets_var)

start_btn = tk.Button(root,text='Start', command=start)

# Layout boxes
reps_label.grid(row=0,column=0)
reps_entry.grid(row=0,column=1)
rest_label.grid(row=1,column=0)
rest_entry.grid(row=1,column=1)
sets_label.grid(row=2,column=0)
sets_entry.grid(row=2,column=1)
start_btn.grid(row=3,column=1)

root.mainloop()  # Start Tkinter GUI, blocking until start is entered

# Done waiting for input, start workout tracking
print(f'Starting workout: Reps: {reps}, Rest: {rest}, Sets: {sets}')

video_capture = cv2.VideoCapture(0)  # 0 is default camera

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36h11)
detectorParams = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, detectorParams)

video_capture = cv2.VideoCapture(0)
if not video_capture.isOpened():
    print('Error: Cannot open camera.'); 

while True:
    result, video_frame = video_capture.read()
    if not result: break
        
    #video_frame = cv2.flip(video_frame, 1)
    (corners, ids, rejected) = detector.detectMarkers(video_frame)
    cv2.aruco.drawDetectedMarkers(video_frame, corners, ids)

    cv2.imshow("Workout Tracker", video_frame)

    k = cv2.waitKey(1)
    if k == ord('q'):  # q to stop
        break


video_capture.release()
cv2.destroyAllWindows()

