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
version = "1.0.5"
title = "just don't die!"
stage = "alpha"
graphics_width = 640
graphics_height = 360
fps = 60

# INITIALIZE DISPLAY
flags = pygame.FULLSCREEN | pygame.SCALED | pygame.HWSURFACE | pygame.DOUBLEBUF
display = pygame.display.set_mode((graphics_width, graphics_height), flags, vsync=1)
pygame.display.set_caption(f"{title} - {version} ({stage})")
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
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*2,self.image.get_height()*2))
        self.rect = self.image.get_rect()
        self.collisions = []
        self.mask = pygame.mask.Mask((self.rect.width,self.rect.height),fill=True)
        self.mask.fill()
        self.touching_ground = False
        self.show_vectors = True
        self.jump = 0
        self.name_tag_text = font.render(f'madiasu', True, (255,255,255), (38,38,38))
        self.name_tag = pygame.Surface((int(self.name_tag_text.get_width()+8),int(self.name_tag_text.get_height()+8)))
        self.name_tag.blit(self.name_tag_text,(4,4))

    def update(self, tile_hitboxes, time_delta):

        # FRICTION
        if player.touching_ground:
            self.forces.update({'friction':[-1*(self.vel[0]/10),0]})
        else:
            self.forces.update({'friction':[-1*(self.vel[0]/20),0]})

        # ITTARATE TROUGH FORCES
        for force in self.forces:
            self.vel[0] += self.forces[force][0] * time_delta
            self.vel[1] += self.forces[force][1] * time_delta
            #force_vector = np.array([(self.x-entity.x),-1*(self.y-entity.y)])
        if 'jump' in player.forces:
            player.forces.pop('jump')

        # UPDATE POS WITH CAMERA
        self.rect.right = self.pos[0] - camera[0]
        self.rect.bottom = self.pos[1] - camera[1]
        
        # X-VECTOR MOVEMENT
        self.pos[0] += self.vel[0]
        self.rect.right = int(self.pos[0]) - camera[0]
        for hitbox in tile_hitboxes:
            if self.rect.colliderect(hitbox): 
                if self.vel[0] > 0:
                    self.pos[0] = hitbox.left + camera[0]
                else:
                    self.pos[0] = hitbox.right + self.rect.width + camera[0]
                self.rect.right = int(self.pos[0]) - camera[0]

        # Y-VECTOR MOVEMENT
        self.pos[1] -= self.vel[1]
        self.rect.bottom = int(self.pos[1]) - camera[1]
        for hitbox in tile_hitboxes:
            if self.rect.colliderect(hitbox): 
                if self.vel[1] < 0: 
                    self.pos[1] = int(hitbox.bottom) + camera[1] - 16
                else:
                    
                    self.pos[1] = hitbox.top + self.rect.height + camera[1] + 16
                self.rect.bottom = int(self.pos[1]) - camera[1]
        
        # GROUND TOUCH CHECK
        self.touching_ground = False
        if player.vel[1] == 0 or player.vel[1] < 0:
            self.rect.bottom = int(self.pos[1]) - camera[1] + 1
            for hitbox in tile_hitboxes:
                if self.rect.colliderect(hitbox): 
                    player.jump = 0
                    self.touching_ground = True
            self.rect.bottom = int(self.pos[1]) - camera[1] 

        # RENDER NAMETAG
        display.blit(self.name_tag,(player.pos[0]-camera[0]+4,player.pos[1]-camera[1]+4))

        # DRAW VECTORS
        if self.show_vectors:
            for force in self.forces:
                pygame.draw.line(display, (255,0,0), [self.pos[0]-camera[0],self.pos[1]-camera[1]], [self.pos[0]+(self.forces[force][0]*100)-camera[0],self.pos[1]-(self.forces[force][1]*100)-camera[1]],2)
        

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, asset):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.image = asset
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = [self.pos[0]-camera[0],self.pos[1]-camera[1]]
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
            delta[0] += 16
        delta[0] = 0
        delta[1] += 16

def Render_Tiles(tiles):
    global tile_hitboxes
    tile_hitboxes = []
    for tile in tiles:
        #if tile.pos[0]-camera[0]>10 and tile.pos[0]-camera[0]<300:
        #    if tile.pos[1]+camera[1]>10 and tile.pos[1]+camera[1]<170:
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
    print(f'cam-x: {camera[0]} cam-y: {camera[1]}')
    print(f'player-x: {player.pos[0]} player-y: {player.pos[1]}')

def Follow_Camera(entity):
    Scroll_Camera_Pos(((entity.pos[0]-camera_pos[0]-310)/10,(entity.pos[1]-camera_pos[1]-200)/10))


def Move_Player(keys):
    if keys[K_d]:
        if player.touching_ground:
            player.forces.update({'move_right':[0.8,0]})
        else:
            player.forces.update({'move_right':[0.4,0]})
    else:
        if 'move_right' in player.forces:
            player.forces.pop('move_right')
    if keys[K_a]:
        if player.touching_ground:
            player.forces.update({'move_left':[-0.8,0]})
        else:
            player.forces.update({'move_left':[-0.4,0]})
    else:
        if 'move_left' in player.forces:
            player.forces.pop('move_left')
    if player.touching_ground == False:
        if 'normal' in player.forces:
            player.forces.pop('normal')
    else:
        player.vel[1] = 0
        player.forces.update({'normal':[0,0.4]})


# GAME LOOP

# VARIABLES
tiles = []
tile_hitboxes = []

# OBJECTS
font = pygame.font.Font('assets/fonts/dogica.ttf', 8)
clock = pygame.time.Clock()
level = pygame.sprite.Group()
player = Entity('player', [100,400])
entities = pygame.sprite.Group()
entities.add(player)
Generate_Tiles()
player.forces.update({"gravity":[0,-0.4]})
text = font.render(f'{title} - {version} ({stage})', True, (38,38,38), (255,255,255))

running = True

while running:
    time_delta = get_time_delta()
    keys = pygame.key.get_pressed()
    events = pygame.event.get()

    for event in events:    
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.jump < 2:
                player.jump += 1
                player.vel[1] = 0
                player.forces.update({'jump':[0,8]})

    # INPUT
    Move_Player(keys)
    Follow_Camera(player)
    Floor_Camera()

    #Move_Camera(keys)

    # RENDERING
    display.fill((255,255,255))
    display.blit(text,(2,2))
    Render_Tiles(tiles)
    entities.update(tile_hitboxes,time_delta)
    entities.draw(display) 

    # SCREEN UPDATE
    pygame.display.flip()

    # FPS CAP
    print(clock.get_fps())
    clock.tick(60)
    
pygame.quit()