# SETUP
import os
import math
import random
import pygame
from pygame.locals import *

# IMPORT SCRIPTS
from physics_engine import *
from rendering_engine import *

pygame.init()

# MODE
debug = False

# STATIC INIT VARIABLES
monitor = pygame.display.Info()
version = "0.0.1"
title = "nightfall"
stage = "alpha"
graphics_width = 320
graphics_height = 180
fps = 60

# Creates a display and a screen
flags = pygame.FULLSCREEN | pygame.SCALED | pygame.HWSURFACE | pygame.DOUBLEBUF
display = pygame.display.set_mode((graphics_width, graphics_height), flags, vsync=1)

# Set the title of the window
pygame.display.set_caption(f"{title} - {stage} {version}")

clock = pygame.time.Clock()
running = True

logo = pygame.image.load("assets/fonts/logo.png")

Entity([50,50], [10,10])

while running:
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    frame_length = clock.get_fps()/60
    Clear_Surface(display)
    for i in range(1):
        s = random.randint(4,6)
        Particle(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],s,s,False)

    Render_Particles(display,active_particles,frame_length)
    Render_Entities(display,active_entities,frame_length,{})

    print(f"{len(active_particles)} + {clock.get_fps()} ")


    # Update screen
    pygame.display.flip()

    # Pause
    clock.tick(fps)
 
pygame.quit()