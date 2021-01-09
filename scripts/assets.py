import pygame
from pygame.locals import *
from pygame import *
import csv


[100,100,100,100,100,100,100]


class Animation():
    def __init__(self, name, path, speed):
        self.frames = []
        self.frame_length = speed
        while True:
            count = 0
            try:
                self.frames.append(pygame.image.load(f'{path}{count}.png'))
            except:
                break
        
        for frame in self.frames:
            pygame.transform.scale(frame, (frame.get_width()*2,frame.get_height()*2))

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
        