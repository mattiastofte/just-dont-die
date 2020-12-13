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

def Render_Entities(display,entities,time_delta,show_vectors=False):
    for entity in entities:
        entity.update(time_delta)
        pygame.draw.rect(display, (0, 255, 0), entity.rect())
    if show_vectors:
        for entity in entities:
            for force in entity.forces:
                x = entity.x + int(entity.width/2)
                y = entity.y + int(entity.height/2)
                vector = entity.forces[force]
                pygame.draw.line(display, (255,0,0), [x, y], [x+vector[0]*100,y-vector[1]*100])
