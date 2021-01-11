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
camera_pos = [0,400]

# FUNCTIONS
def Update_Camera_Pos(pos):
    camera_pos[0] = pos[0]
    camera_pos[1] = pos[1]
    Floor_Camera()

def Scroll_Camera_Pos(delta):
    camera_pos[0] += delta[0]
    camera_pos[1] += delta[1]
    Floor_Camera()

def Floor_Camera():
    camera[0] = int(camera_pos[0])
    camera[1] = int(camera_pos[1])
