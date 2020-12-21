# SETUP
import os
import math
import random
import pygame
from pygame.locals import *
from pygame import *

# IMPORT SCRIPTS
from physics_engine import *
from rendering import *
from game_logic import *

pygame.init()

# STATIC INIT VARIABLES
monitor = pygame.display.Info()
version = "1.0.2"
title = "just don't die!"
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
icon = pygame.image.load("assets/icons/game_icon.png")

pygame.display.set_icon(icon)

Entity("player", [50,50], [10,10])
Entity("player_2", [100, 50], [10,10])
Entity("player_3", [0,50], [5,5])
Entity("player_4", [20, 200], [6,6])
Entity("player_5", [100, 10], [10,10])

mouse_down = True

def get_time_delta():
    return clock.get_fps()/fps

while running:
    frame_length = get_time_delta()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    Clear_Surface(display)
    Update_Camera([entities_dict.get("player").x,entities_dict.get("player").y])
    if pygame.mouse.get_pressed()[0]:
        if mouse_down == False:
            for i in range(100):
                s = random.randint(4,6)
                Particle(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],s,s,False)
                Impulse((pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]),30,entities_active)
        mouse_down = True
    else:
        mouse_down = False
    keys = pygame.key.get_pressed()
    if keys[K_w]:
        entities_dict.get("player").forces.update({"up":[0,1]})
    else:
        entities_dict.get("player").forces.update({"up":[0,0]})
    if keys[K_s]:
        entities_dict.get("player").forces.update({"down":[0,-1]})
    else:
        entities_dict.get("player").forces.update({"down":[0,0]})
    if keys[K_d]:
        entities_dict.get("player").forces.update({"right":[1,0]})
    else:
        entities_dict.get("player").forces.update({"right":[0,0]})
    if keys[K_a]:
        entities_dict.get("player").forces.update({"left":[-1,0]})
    else:
        entities_dict.get("player").forces.update({"left":[0,0]})

    Render_Particles(display,active_particles,frame_length)
    Render_Entities(display,entities_active,frame_length,True)
    # GAME LOGIC 
    Move_Entity(pygame.key.get_pressed(),entities_dict["player"])
    #d.update(entities_active)

    # RENDERING ENGINE

    #print(f"{len(active_particles)} + {clock.get_fps()} ")

    for entity in entities_active:
        entity.forces.update({"explosion":[0,0]})

    # Update screen
    pygame.display.flip()

    # Pause
    clock.tick(fps)
 
pygame.quit()