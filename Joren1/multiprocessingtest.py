import multiprocessing
from facedetection import facerecognition
from coordinaatzoom6 import coordinaatzoomfunctie



def main():
    p2 = multiprocessing.Process(target=coordinaatzoomfunctie)
    p1 = multiprocessing.Process(target=facerecognition)

    p2.start()
    p1.start()

    p2.join()
    p1.join()
    print("einde")

if __name__ == '__main__':
    main()


