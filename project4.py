import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"  # Reduces camera load time SIGNIFICANTLY
import tkinter as tk
import cv2
from threading import Timer


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

# Workout State Variables
current_set = 1
current_rep = 0
# State can be "Exercise", "Rest", or "Done"
workout_state = "Exercise" 
rest_timer = rest


def tick_rest():  # called every second to update rest timer
    global workout_state, rest_timer, rest

    if rest_timer==0:
        rest_timer = rest  # reset to max rest
        workout_state="Exercise"
    else:
        rest_timer-=1
        workout_state=f"Rest: {rest_timer} sec"
        t = Timer(1, tick_rest)
        t.start()
    
    

# function to handle counting reps and switching sets
def count_rep():
    global reps, rest, sets
    global current_set, current_rep, workout_state
    
    if workout_state=="Exercise":
        current_rep+=1

        if (current_rep == reps):
            current_rep=0
            current_set+=1
            workout_state=f"Rest: {rest} sec"

            if (current_set == sets+1):
                current_rep=reps
                current_set=sets
                workout_state="Done"
            else:
                t = Timer(1, tick_rest)
                t.start()



# UI Display settings
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.8
font_color = (255, 255, 255) # White
thickness = 2

video_capture = cv2.VideoCapture(0)
if not video_capture.isOpened():
    print('Error: Cannot open camera.'); 

while True:
    result, video_frame = video_capture.read()
    if not result: break
        
    #video_frame = cv2.flip(video_frame, 1)
    (corners, ids, rejected) = detector.detectMarkers(video_frame)
    cv2.aruco.drawDetectedMarkers(video_frame, corners, ids)

    # We get the frame width (w) to align to the right side
    h, w, _ = video_frame.shape 
    box_top_left = (w - 260, 30)  # 300px from right edge, 30px from top
    box_bottom_right = (w - 30, 150) # 30px from right edge, 180px from top
    
    # Draws the black box with 50% transparency (alpha)
    overlay = video_frame.copy()
    cv2.rectangle(overlay, box_top_left, box_bottom_right, (0, 0, 0), -1) # Black
    alpha = 0.6 # Transparency factor
    cv2.addWeighted(overlay, alpha, video_frame, 1 - alpha, 0, video_frame)
    
    # Define text positions (inside the new box)
    text_x = w - 245 # X position for all text
    set_y = 55
    rep_y = 95
    state_y = 135

    # 1. Display SETS
    set_text = f"Set: {current_set} / {sets}"
    cv2.putText(video_frame, set_text, 
                (text_x, set_y), font, font_scale, font_color, thickness)
    
    # 2. Display REPS
    rep_text = f"Rep: {current_rep} / {reps}"
    cv2.putText(video_frame, rep_text, 
                (text_x, rep_y), font, font_scale, font_color, thickness)

    # 3. Display Workout State
    cv2.putText(video_frame, workout_state, 
                (text_x, state_y), font, font_scale, (0, 255, 0), thickness) # Green
    weight_text = "Weight: --"
    
    # Check if any tags were detected
    if ids is not None:
        flat_ids = ids.flatten()
        if 5 in flat_ids:
            weight_text = "Weight: 5 lbs"
        elif 10 in flat_ids:
            weight_text = "Weight: 10 lbs"
    
    # Display at bottom-right
    # (h - 30) puts it near the bottom of the screen
    cv2.putText(video_frame, weight_text, (w - 250, h - 30), 
                font, font_scale, (0, 255, 255), thickness) # Yellow text
    
    cv2.imshow("Workout Tracker", video_frame)

    

    k = cv2.waitKey(1)
    if k == ord('q'):  # q to stop
        break
    elif k == ord('r'):  # r to advance rep (for debugging)
        count_rep()
    

video_capture.release()
cv2.destroyAllWindows()

