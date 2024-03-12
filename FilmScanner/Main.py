from picamera2 import Picamera2, Preview
from socket import timeout
import queue
from threading import Thread
from fractions import Fraction
import numpy as np
import cv2 as cv
import glob
import os
import serial
import math
from datetime import datetime, timedelta
import time
import subprocess

#Local
from Marlin import *
from Threshold import *
from Util import *
from Camera import *


# Globals
NUM_THREADS = 3
lower_threshold = 150



def main():
    print("Started")

    confirgureLowResCamera()



if __name__ == "__main__":
    main()