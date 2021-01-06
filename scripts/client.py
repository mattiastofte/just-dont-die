# SETUP
import pygame
from pygame.locals import *
from pygame import *
import os
import math
import random

# IMPORT SCRIPTS
from rendering import *
from assets import *

pygame.init()

# STATIC INIT VARIABLES
monitor = pygame.display.Info()
version = "1.0.4"
title = "just don't die!"
stage = "alpha"
graphics_width = 320
graphics_height = 180 
fps = 60

# INITIALIZE DISPLAY
flags = pygame.FULLSCREEN | pygame.SCALED | pygame.HWSURFACE | pygame.DOUBLEBUF
display = pygame.display.set_mode((graphics_width, graphics_height), flags, vsync=1)
pygame.display.set_caption(f"{title} - {stage} {version}")
icon = pygame.image.load("assets/icons/game_icon.png")
pygame.display.set_icon(icon)

# LOAD ASSETS
tile_images = Load_Tile_Assets()

# FUNCTIONS
sign = lambda x: math.copysign(1, x) 

class Entity(pygame.sprite.Sprite):
    def __init__(self, name, pos, forces={}, vel=[0,0]):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.pos = pos
        self.vel = vel
        self.forces = forces
        self.image = pygame.image.load('assets/characters/player/green.png')
        self.rect = self.image.get_rect()
        self.collisions = []
        self.mask = pygame.mask.Mask((self.rect.width,self.rect.height),fill=True)
        self.mask.fill()

    def update(self, tile_hitboxes, time_delta):
        # ITTARATE TROUGH FORCES
        for force in self.forces:
            self.vel[0] += self.forces[force][0]*time_delta
            self.vel[1] += self.forces[force][1]*time_delta
            
        # X-VECTOR MOVEMENT
        self.pos[0] += self.vel[0]
        self.rect.right = self.pos[0]+camera[0]
        for hitbox in tile_hitboxes:
            if self.rect.colliderect(hitbox): 
                if self.vel[0] > 0:
                    self.pos[0] = hitbox.left - camera[0]
                else:
                    self.pos[0] = hitbox.right + self.rect.width - camera[0]
                self.rect.right = self.pos[0]+camera[0]

        # Y-VECTOR MOVEMENT
        self.pos[1] -= self.vel[1]
        self.rect.bottom = self.pos[1]+camera[1]
        for hitbox in tile_hitboxes:
            if self.rect.colliderect(hitbox): 
                if self.vel[1] < 0: 
                    self.pos[1] = hitbox.bottom - camera[1] - 8
                else:
                    self.pos[1] = hitbox.top + self.rect.height - camera[1] + 8
                self.rect.bottom = self.pos[1]+camera[1]

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, asset):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.image = asset
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = [self.pos[0]+camera[0],self.pos[1]+camera[1]]
        display.blit(self.image,(self.rect.x,self.rect.y))

#class Map(pygame.sprite.Sprite):
#    def __init__(self,map):
#        pygame.sprite.Sprite.__init__(self)
#        self.image = Generate_Map(map)
#        self.rect = self.image.get_rect()
#        self.mask = pygame.mask.from_surface(self.image)
#
#    def update(self):
#        self.rect.center = [camera[0],camera[1]]

def Generate_Tiles():
    delta = [0,0]
    with open(f'data/test.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    for row in data:
        for column in row:
            if column == '1':
                tiles.append(Tile([delta[0],delta[1]],tile_images.get('dirt')))
            else:
                pass
            delta[0] += 8
        delta[0] = 0
        delta[1] += 8

def Render_Tiles(tiles):
    global tile_hitboxes
    tile_hitboxes = []
    for tile in tiles:
        if tile.pos[0]+camera[0]>10 and tile.pos[0]+camera[0]<300:
            if tile.pos[1]+camera[1]>10 and tile.pos[1]+camera[1]<170:
                tile.update()
                tile_hitboxes.append(tile.rect)
        

def get_time_delta():
    return clock.get_fps()/fps

def Move_Camera(keys):
    if keys[K_RIGHT]:
        Scroll_Camera([5,0])
    if keys[K_LEFT]:
        Scroll_Camera([-5,0])
    if keys[K_UP]:
        Scroll_Camera([0,5])
    if keys[K_DOWN]:
        Scroll_Camera([0,-5])

def Move_Player(keys):
    if keys[K_d]:
        player.vel[0] += 0.1
    if keys[K_a]:
        player.vel[0] -= 0.1
    if keys[K_w]:
        player.vel[1] += 0.1
    if keys[K_s]:
        player.vel[1] -= 0.1
    if keys[K_SPACE]:
        player.vel[0] = 0
        player.vel[1] = 0

# GAME LOOP

# VARIABLES
tiles = []
tile_hitboxes = []

# OBJECTS
clock = pygame.time.Clock()
level = pygame.sprite.Group()
player = Entity('player', [0,0])
entities = pygame.sprite.Group()
entities.add(player)
Generate_Tiles()

running = True

while running:
    time_delta = get_time_delta()
    keys = pygame.key.get_pressed()
    events = pygame.event.get()

    for event in events:    
        if event.type == pygame.QUIT:
            running = False

    # RENDERING
    display.fill((255,255,255))
    Render_Tiles(tiles)
    entities.update(tile_hitboxes,time_delta)
    entities.draw(display) 
    Move_Player(keys)
    Move_Camera(keys)
    # SCREEN UPDATE
    pygame.display.flip()

    # FPS CAP
    clock.tick(fps)
    #print(clock.get_fps())
    print(len(tile_hitboxes))
    
pygame.quit()