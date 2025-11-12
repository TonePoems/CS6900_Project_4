import tkinter as tk
 

root=tk.Tk()

# Small default values for testing
reps_var = tk.IntVar(value=5)  # how many are performed before the rest interval
rest_var = tk.IntVar(value=10)  # how long the person rests before the next repetition starts. The rest interval is specified in seconds
sets_var = tk.IntVar(value=3)  # how many groups of repetitions will be performed

def start():

    reps = reps_var.get()
    rest = rest_var.get()
    sets = sets_var.get()

    print(f'Starting workout: Reps: {reps}, Rest: {rest}, Sets: {sets}')
    # TODO: Enter curl tracking logic


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

root.mainloop()  # Start Tkinter gui



