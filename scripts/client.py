# SETUP
import os
import math
import random
import pygame
from pygame.locals import *
from pygame import *

# IMPORT SCRIPTS
from physics_engine import *
from rendering_engine import *
from game_logic import *

pygame.init()

# MODE
debug = False

# STATIC INIT VARIABLES
monitor = pygame.display.Info()
version = "1.0.2"
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
icon = pygame.image.load("assets/icons/game_icon.png")

pygame.display.set_icon(icon)

Entity("player", [50,50], [10,10])
d = Point_Gravity([100, 100], 2)
entities_dict.get("player").forces.update({"gravity":[0,-0.12]})

while running:
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    frame_length = clock.get_fps()/60  
    Clear_Surface(display)
    d.x = pygame.mouse.get_pos()[0]
    d.y = pygame.mouse.get_pos()[1]
    for i in range(1):
        s = random.randint(4,6)
        Particle(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],s,s,False)
    # GAME LOGIC 
    Move_Entity(pygame.key.get_pressed(),entities_dict["player"])
    d.update(entities_active)

    # RENDERING ENGINE
    Render_Particles(display,active_particles,frame_length)
    Render_Entities(display,entities_active,frame_length,True)
    


    print(f"{len(active_particles)} + {clock.get_fps()} ")


    # Update screen
    pygame.display.flip()

    # Pause
    clock.tick(fps)
 
pygame.quit()