# SETUP
import pygame
from pygame.locals import *
from pygame import *
import modified_sprite
import os
import math 
import random
import pickle

# IMPORT SCRIPTS
from rendering import *
from assets import *
from user_interface import *

pygame.init()

# STATIC INIT VARIABLES
monitor = pygame.display.Info()
version = "1.0.6"
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

# MUSIC
#Runaway = pygame.mixer.Sound('assets/sounds/music/Runway.mp3')
#Runaway.set_volume(0.1)
#Runaway.play()

# LOAD ASSETS
tile_images = Load_Tile_Assets()

# FUNCTIONS
#sign = lambda x: math.copysign(1, x) 

# MODIFIED GROUP CLASS
class Entity(modified_sprite.Sprite):
    def __init__(self, pos, size, **properties):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.offset = [0,0]
        self.vel = [0,0]
        self.forces = {}
        self.show_vectors = False
        self.show_hitbox = False
        self.rect = pygame.Rect(0,0,size[0],size[1])
        self.physics = True
        
        # ANIMATION VARIABLES
        self.frame_count = 0
        self.frame_time_lapsed = pygame.time.get_ticks()
        self.flipped = False
        # CREATE A ALPHA SURFACE AS IMAGE FOR BLITTING
        self.image = Surface((self.rect.width,self.rect.height))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        # CREATE A HITBOX SURFACE
        if self.show_hitbox:
            self.hitbox = Surface((self.rect.width,self.rect.height))
            self.hitbox.fill((252,186,3))
            pygame.draw.rect(self.hitbox,(0,0,0),(2,2,self.rect.width-4,self.rect.height-4))
            self.hitbox.set_colorkey((0,0,0))
            self.hitbox.convert_alpha()
        # CREATE MASK OFF ENTITY
        #self.mask = pygame.mask.Mask((self.rect.width,self.rect.height),fill=True)
        #self.mask.fill()
        if self.physics:
            self.touching_ground = False
        
        for key, value in properties.items():
            setattr(self, key, value)


    def update(self, tile_hitboxes, time_delta):
        # MOVE BACK TO SPAWN
        if self.pos[1] > 2000:
            self.pos[0] = 100
            self.pos[1] = 400
            self.vel[0] = 0
            self.vel[1] = 1

        # UPDATE POS WITH CAMERA
        self.rect.right = self.pos[0] - camera[0]
        self.rect.bottom = self.pos[1] - camera[1]

        # FRICTION
        if self.physics:
            if player.touching_ground:
                self.forces.update({'friction':[-1*(self.vel[0]/10),0,False]})
            else:
                self.forces.update({'friction':[-1*(self.vel[0]/10),0,False]})

            # ITTARATE TROUGH FORCES
            pop_list = []
            for key, value in self.forces.items():
                self.vel[0] += value[0] * time_delta
                self.vel[1] += value[1] * time_delta
                if value[2]:
                    pop_list.append(key)

            # POP IMPULSES
            for key in pop_list:
                self.forces.pop(key)
        
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
                        player.jump_count = 0
                        self.touching_ground = True
                self.rect.bottom = int(self.pos[1]) - camera[1] 

            # FORCE NORMAL
            if self.touching_ground == False:
                if 'normal' in self.forces:
                    self.forces.pop('normal')
            else:
                self.vel[1] = 0
                self.forces.update({'normal':[0,0.4,False]})

            # DRAW VECTORS
            if self.show_vectors:
                for force in self.forces:
                    pygame.draw.line(display, (255,0,0), [self.pos[0]-camera[0],self.pos[1]-camera[1]], [self.pos[0]+(self.forces[force][0]*100)-camera[0],self.pos[1]-(self.forces[force][1]*100)-camera[1]],2)
        else:
            self.rect.bottom = int(self.pos[1]) - camera[1]
            self.rect.right = int(self.pos[0]) - camera[0]

        # RENDER HITBOX
        if self.show_hitbox:
            display.blit(self.hitbox,(self.pos[0]-camera[0]-self.rect.width,self.pos[1]-camera[1]-self.rect.height))

class Player(Entity):
    def __init__(self, name, pos, size, **properties):
        self.name = name
        self.state = 'idle'
        self.jump_count = 0
        self.animation = idle_animation
        super().__init__(pos, size, **properties)
        self.image = pygame.Surface((0,0))
        self.name_tag_text = font.render(f'{self.name}', True, (255,255,255), (38,38,38))
        self.name_tag = pygame.Surface((int(self.name_tag_text.get_width()+8),16))
        self.name_tag.fill((38, 38, 38))
        self.name_tag.blit(self.name_tag_text,(4,4))
        self.offset = [0,0]

    def update(self, tile_hitboxes, time_delta):
        super().update(tile_hitboxes,time_delta)
        self.current_tick = pygame.time.get_ticks()
        if self.current_tick-self.frame_time_lapsed > self.animation.frame_length:
            if self.frame_count > self.animation.number_of_frames:
                self.frame_count = 0
            else:
                self.frame_count += 1
            self.frame_time_lapsed = self.current_tick
            Swap_Frame(self)
        
        # NAMETAG RENDERING
        display.blit(self.name_tag,(self.pos[0]-camera[0]+2,self.pos[1]-camera[1]+2))

class Tile(modified_sprite.Sprite):
    def __init__(self, pos, asset):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.image = asset
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = [self.pos[0]-camera[0],self.pos[1]-camera[1]]
        display.blit(self.image,(self.rect.x,self.rect.y))

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
        if tile.pos[0]-camera[0]>-50 and tile.pos[0]-camera[0]<750:
            if tile.pos[1]-camera[1]>-50 and tile.pos[1]-camera[1]<400:
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
            player.forces.update({'move_right':[0.8,0,False]})
        else:
            player.forces.update({'move_right':[0.4,0,False]})
    else:
        if 'move_right' in player.forces:
            player.forces.pop('move_right')
    if keys[K_a]:
        if player.touching_ground:
            player.forces.update({'move_left':[-0.8,0,False]})
        else:
            player.forces.update({'move_left':[-0.4,0,False]})
    else:
        if 'move_left' in player.forces:
            player.forces.pop('move_left')

# GAME LOOP

# VARIABLES
tiles = []
tile_hitboxes = []

# ANIMATIONS
idle_animation = Animation('idle','assets/characters/player/idle/idle',100,[0,0])
running_animation = Animation('run','assets/characters/player/run/run',100,[-20,-4])

# OBJECTS
font = pygame.font.Font('assets/fonts/dogica.ttf', 8)
clock = pygame.time.Clock()
level = modified_sprite.Group()
#player = Entity([100,400], [20,20])
player = Player('madiasu', [100,400], [28,56], show_vectors=True)
player2 = Player('SaiYue', [200,850], [28,56], physics=False)
player3 = Player('Largosof', [300,850], [28,56], physics=False)
#player_2 = Entity('player_2', [100,400])
entities = modified_sprite.Group()
entities.add(player)
entities.add(player2)
entities.add(player3)
Generate_Tiles()
player.forces.update({"gravity":[0, -0.4, False]})
player2.forces.update({"gravity":[0, -0.4, False]})
player3.forces.update({"gravity":[0, -0.4, False]})
text = font.render(f'{title} - {version} ({stage})', True, (38,38,38), (255,255,255))

# GAME LOOP
running = True
while running:
    time_delta = get_time_delta()
    keys = pygame.key.get_pressed()
    events = pygame.event.get()

    for event in events:    
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.jump_count < 2:
                player.jump_count += 1
                player.vel[1] = 0
                player.forces.update({'jump':[0 , 8, True]})
            if event.key == pygame.K_d:
                Change_Animation(player, running_animation, False)
            if event.key == pygame.K_a:
                Change_Animation(player, running_animation, True)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                if not (keys[K_d] and keys[K_a]):
                    Change_Animation(player, idle_animation, True)
                    
    # INPUT
    Move_Player(keys)
    Follow_Camera(player)

    # RENDERING
    display.fill((255,255,255))
    display.blit(text,(2,2))
    Render_Tiles(tiles)
    entities.update(tile_hitboxes,time_delta)
    entities.draw(display) 
    fps_text = font.render((f'fps: {round(clock.get_fps(),2)}'), True, (38,38,38), (255,255,255))
    display.blit(fps_text,(550,2))

    # SCREEN UPDATE
    pygame.display.flip()

    # FPS CAP
    clock.tick(60)
    
pygame.quit()
