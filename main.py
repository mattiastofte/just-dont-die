"""
 Simple snake example.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
"""

# Setup
import os

try:
    pygame_package_info = os.popen("pip3 show pygame").read()
    index = pygame_package_info.find("Version:")
    pygame_version = str(pygame_package_info[index+9:index+14])
except:
    pygame_version = "null"

if pygame_version == "2.0.0":
    print("correct version of pygame detected.")
else:
    print("error: correct version of pygame is not installed")
    print("installing pygame 2.0.0 ...")
    try:
        os.system("pip3 install pygame==2.0.0")
        print("correct version of pygame was successfully installed")
    except:
        print("couldn't install correct version of pygame")

import pygame
from pygame.locals import *

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
width = 320
height = 180

# Creates a display and a screen
flags = pygame.FULLSCREEN | pygame.SCALED | pygame.HWSURFACE | pygame.DOUBLEBUF
display = pygame.display.set_mode((width, height), flags, vsync=1)

# Set the title of the window
pygame.display.set_caption(f"{title} - {stage} {version}")

clock = pygame.time.Clock()
running = True

logo = pygame.image.load("assets/text/logo.png")
x = 0
while running:
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if x > 60:
        x = 0
    x += 1
    # Clear screen
    display.fill(BLACK)
    display.blit(logo,(0,x))
    # Update screen
    pygame.display.flip()
 
    # Pause
    clock.tick(60)
 
pygame.quit()