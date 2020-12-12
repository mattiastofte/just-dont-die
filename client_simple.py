# SETUP
import os
import math
import pygame
from pygame.locals import *
from physics_engine import *
import random

pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Mode
debug = False

# Static init variables
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

logo = pygame.image.load("assets/text/logo.png")
i = 1
count = 0
while running:
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Clear screen
    display.fill(BLACK)

    frame_length = clock.get_fps()/60
    count += 0.05
    if 1 == 1:
        s = random.randint(5,10)
        cos = math.cos(count)
        sin = math.sin(count)
        for count in range(200):
            Particle(50,50,s,s,False)
    for entities in active_entities:
        entities.update(frame_length)
        pygame.draw.rect(display, WHITE, entities.rect())
    
    print(f"{len(active_entities)} + {clock.get_fps()} ")


    # Update screen
    pygame.display.flip()
    # Pause
    clock.tick(fps)
 
pygame.quit()