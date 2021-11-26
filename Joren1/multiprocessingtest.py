import multiprocessing

import time

def printr():
    print("1")
    time.sleep(0.5)
    print("done")


def printr2():
    print("2")
    time.sleep(1.5)
    print("DONE")

p1 = multiprocessing.Process(target=printr)
p2 = multiprocessing.Process(target=printr2)


p1.start()
p2.start()

p1.join()
p2.join()





