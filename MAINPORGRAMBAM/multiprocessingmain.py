import multiprocessing
from main_testv2 import pipeline
from coordinaatzoom import coordinaatzoomfunctie
zoomcamera = 2
widecamera = 1


def main():
    p2 = multiprocessing.Process(target=coordinaatzoomfunctie, args=(zoomcamera,))
    p1 = multiprocessing.Process(target=pipeline, args=(widecamera,))

    p2.start()
    p1.start()

    p2.join()
    p1.join()
    print("einde")

if __name__ == '__main__':
    main()


