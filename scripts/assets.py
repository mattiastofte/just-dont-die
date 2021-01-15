import pygame
from pygame.locals import *
from pygame import *
import modified_sprite
import csv

class Animation():
    def __init__(self, name, path, frame_length, offset):
        self.frames = []
        self.frames_flipped = []
        self.frame_length = frame_length
        self.offset = offset
        self.number_of_frames = 0
        while True:
            try:
                self.frames.append(pygame.image.load(f'{path}{self.number_of_frames+1}.png'))
                self.number_of_frames += 1
            except:
                break
        
        for frame in range(self.number_of_frames):
            self.frames[frame] = pygame.transform.scale(self.frames[frame], (self.frames[frame].get_width()*2,self.frames[frame].get_height()*2))
            self.frames_flipped.append(pygame.transform.flip(self.frames[frame], True, False))
        
        self.number_of_frames = len(self.frames)
        print(f'[GAME] Loaded {self.number_of_frames} frames for animation: {name}')

class Background(modified_sprite.Sprite):
    def __init__(self, path, offset):
        self.image = pygame.image.load(path)
    
def Change_Animation(entity, animation, flipped=False):
    entity.frame_count = 0
    entity.animation = animation
    entity.flipped = flipped

def Swap_Frame(entity):
    entity.offset = entity.animation.offset
    if entity.flipped:
        try:
            entity.image = entity.animation.frames_flipped[entity.frame_count]
        except:
            entity.frame_count = 0
            entity.image = entity.animation.frames_flipped[entity.frame_count]
    else:
        try:
            entity.image = entity.animation.frames[entity.frame_count]
        except:
            entity.frame_count = 0
            entity.image = entity.animation.frames[entity.frame_count]
    
def Generate_Empty_Map(name):
    with open(f'data/{name}.csv', 'w', newline='') as csv_file:
        empty_row = []
        map_data = csv.writer(csv_file)
        for i in range(128):
            empty_row.append(0)
        for i in range(128):
            map_data.writerow(empty_row)

def Load_Tile_Assets():
    tile_images = {}
    tile_images.update({'dirt':pygame.image.load('assets/tiles/basic.png')})
    for tile in tile_images:
        tile_images.update({tile:pygame.transform.scale(tile_images[tile], [16,16])})
    return tile_images

#def Generate_Map(name):
#    map_surface = pygame.Surface((1028,1028), pygame.SRCALPHA, 32)
#    map_surface.convert_alpha()
#    tile = pygame.image.load('assets/tiles/basic.png')
#    delta = [0,0]
#    with open(f'data/{name}.csv', newline='') as f:
#        reader = csv.reader(f)
#        data = list(reader)
#    for row in data:
#        for column in row:
#            if column == '1':
#                map_surface.blit(tile,(delta[0],delta[1]))
#            else:
#                pass
#            delta[0] += 8
#        delta[0] = 0
#        delta[1] += 8
#    return map_surface
        