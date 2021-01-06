import os
import math
import pygame
from pygame.locals import *
import random
from pathlib import Path

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# VARAIBLES
camera = [0,0]

# FUNCTIONS
def Update_Camera(pos):
    camera[0] = -1*pos[0]+150
    camera[1] = 1*pos[1]+80

def Scroll_Camera(delta):
    camera[0] -= delta[0]
    camera[1] += delta[1]
