from threading import Thread
import subprocess

t1 = Thread(target=subprocess.run, args=(["python", "main_program_test.py"],))
t2 = Thread(target=subprocess.run, args=(["python", "zoom_test.py"],))

t1.start()
t2.start()
