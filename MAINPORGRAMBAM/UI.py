from tkinter import *
from tkinter import ttk

MOUTH_AR_THRESH = 0.67
fps = 0
straal_cm = 150
frame_counter = 0

def adjust(x, n, a):
    x += n
    a.set(x)
    print(x, a)
def adjust1():
    adjust(MOUTH_AR_THRESH, 0.01, sensitivity_window)
def adjust2():
    adjust(MOUTH_AR_THRESH, -0.01, sensitivity_window)
def adjust3():
    adjust(straal_cm, 5, distance_window)
def adjust4():
    adjust(straal_cm, -5, distance_window)

    # Startup info window



root = Tk()
root.title("Meeting OWL")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
fps_window = StringVar()
fps_window.set(fps)
sensitivity_window = StringVar()
sensitivity_window.set(MOUTH_AR_THRESH)
distance_window = StringVar()
distance_window.set(straal_cm)

ttk.Button(mainframe, text="+0.01", command=adjust1).grid(column=5, row=8, sticky=(W, E))
ttk.Button(mainframe, text="-0.01", command=adjust2).grid(column=4, row=8, sticky=(W, E))
ttk.Button(mainframe, text="+5", command=adjust3).grid(column=5, row=9, sticky=(W, E))
ttk.Button(mainframe, text="-5", command=adjust4).grid(column=4, row=9, sticky=(W, E))

ttk.Label(mainframe, text="Status").grid(column=2, row=0, sticky=(S))
ttk.Label(mainframe, text="Position").grid(column=3, row=0, sticky=(S))
ttk.Label(mainframe, text="Participant 1").grid(column=1, row=2, sticky=(W))
ttk.Label(mainframe, text="Participant 2").grid(column=1, row=3, sticky=(W))
ttk.Label(mainframe, text="Participant 3").grid(column=1, row=4, sticky=(W))
ttk.Label(mainframe, text="Participant 4").grid(column=1, row=5, sticky=(W))
ttk.Label(mainframe, text="FPS").grid(column=1, row=7, sticky=(S))
ttk.Label(mainframe, text="Sensitivity").grid(column=1, row=8, sticky=(S))
ttk.Label(mainframe, text="Distance").grid(column=1, row=9, sticky=(S))

ttk.Label(mainframe, textvariable=fps_window).grid(column=2, row=7, sticky=(W, E))
ttk.Label(mainframe, textvariable=distance_window).grid(column=2, row=9, sticky=(W, E))
ttk.Label(mainframe, textvariable=sensitivity_window).grid(column=2, row=8, sticky=(W, E))

root.mainloop()