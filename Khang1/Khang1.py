import csv
import copy
import argparse
import itertools
from collections import Counter
from collections import deque
from threading import Thread
import cv2 as cv
import numpy as np
import mediapipe as mp

from utils import CvFpsCalc
from model import KeyPointClassifier
from model import PointHistoryClassifier
import hand_gestures as hg
import face

def hands():
    hg.main()

def faces():
    face.main()

Thread(target = hands).start()
Thread(target = faces).start()