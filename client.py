# Setup
import os
import math

def install(libary):
    if libary == "pygame":
        print("[info] installing pygame 2.0.0 ...")
        try:
            os.system("pip3 install pygame==2.0.0")
            print("[info] correct version of pygame was successfully installed")
        except:
            print("[error] failed to install correct version of pygame")
    else:
        pass

try:
    pygame_package_info = os.popen("pip3 show pygame").read()
    index = pygame_package_info.find("Version:")
    pygame_version = str(pygame_package_info[index+9:index+14])
except:
    pygame_version = "null"

if pygame_version == "2.0.0":
    print("[info] correct version of pygame detected.")
elif pygame_version == "null":
    print("[warning] pygame libary is missing")
    install("pygame")
else:
    print("[warning] pygame is outdated and an update is required.")
    install("pygame")

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
fps = 60

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
    x += 0.25
    # Clear screen
    display.fill(BLACK)
    display.blit(logo,(math.sin(x)*10,math.cos(x)*30))
    # Update screen
    pygame.display.flip()
    # Pause
    clock.tick(fps)
 
pygame.quit()