import os
from dotmap import DotMap

EMULATOR_TITLE = "LDPlayer"
SCREEN_SCALING = 1.25

IMAGES = {
    "START": os.path.abspath(os.path.dirname(__file__)) + "/img/start6.png", 
    "OP_SELECT": os.path.abspath(os.path.dirname(__file__)) + "/img/big_op_sel.png",
    "OP_SELECT2": os.path.abspath(os.path.dirname(__file__)) + "/img/selbig.png",
    "WIN3": os.path.abspath(os.path.dirname(__file__)) + "/img/big_win_3.png",
    "WIN3_LD": os.path.abspath(os.path.dirname(__file__)) + "/img/win3_ld.png",
    "OOS": os.path.abspath(os.path.dirname(__file__)) + "/img/big_oos.png",
}

LT = 50  # Lower Threshold for edge detection
UT = 150  # Upper threshold for edge detection

CC = 0.7 # Confidence coefficient, how similar the image needs to be

ACTION_DELAY = 2 #in seconds