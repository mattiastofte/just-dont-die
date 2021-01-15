import pygame
from pygame.locals import *
from pygame import *
import modified_sprite

class Button(modified_sprite.Sprite):
    def __init__(self, pos, size, **kwargs):
        self.pos = pos
        self.size = size
        self.image = pygame.Surface(size)
        self.color = (255,0,0)
        
