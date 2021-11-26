import multiprocessing
from main_program_test_final import pipeline
from coordinaatzoom import coordinaatzoomfunctie



def main():
    p2 = multiprocessing.Process(target=coordinaatzoomfunctie)
    p1 = multiprocessing.Process(target=pipeline)


    p2.start()
    p1.start()

    p2.join()
    p1.join()
    print("einde")

if __name__ == '__main__':
    main()


