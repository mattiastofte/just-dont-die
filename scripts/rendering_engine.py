import os
import math
import pygame
from pygame.locals import *
from physics_engine import *
import random
from pathlib import Path

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# FUNCTIONS

def Clear_Surface(display):
    display.fill(BLACK)

#def Render_Entities(entities):
#    for entities in entities:
#        entities.update(frame_length)
#        pygame.draw.rect(display, WHITE, entities.rect())

def Render_Particles(display,particles,time_delta):
    for particle in particles:
        particle.update(time_delta)
        pygame.draw.rect(display, WHITE, particle.rect())
