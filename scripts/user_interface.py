import pygame
from pygame.locals import *
from pygame import *
import modified_sprite
import math

class Button(modified_sprite.Sprite):
    def __init__(self, pos, size, text, font, **kwargs):
        self.pos = pos
        self.size = size
        self.button_image = pygame.Surface(size)
        self.button_active_image = pygame.Surface(size)
        self.image = self.button_image
        self.font = font
        self.text = text

        # BUTTON ARGS
        self.color = (255,0,0)
        self.text_color = (255,255,255)
        self.stroke_color
        self.stroke_width = 1

        # ACTIVE BUTTON ARGS
        self.hover_color = self.color
        self.hover_text_color = self.text_color
        self.hover_stroke_color = self.stroke_color

        for key, value in properties.items():
            setattr(self, key, value)

        self.render_button()

    def render_button(self):
        self.button_image.fill(self.color)
        self.image.blit(self.font.render(f'{text}', True, self.text_color, self.color))

    def update(self, mouse):
        pass

class Tile_Menu(modified_sprite.Sprite):
    def __init__(self,font,tile_textures):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0,48,48,266)
        self.image = Surface((48,266))
        self.image.fill((60,60,60))
        self.offset = [0,0]
        self.font = font
        pygame.draw.rect(self.image,(20,20,20),(0,0,48,10))
        self.image.blit(font.render('tiles', True, (255,255,255), (20,20,20)),(0,1))
        self.render_tiles(tile_textures)

    def render_tiles(self, tile_textures):
        delta = [0,10]
        for tile, image in tile_textures.tile_images.items():
            self.image.blit(image,(delta))
            delta[0] += 16
            if delta[0] >= 48:
                delta[0] = 0
                delta[1] += 16

class Tile_Grid_Selector(modified_sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(200,200,16,16)
        self.offset = [0,0]
        self.image = Surface((16,16))
        self.image.fill((0,0,0))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        pygame.draw.line(self.image,(0,255,0),(0,0),(14,0),2)
        pygame.draw.line(self.image,(0,255,0),(14,0),(14,16),2)
        pygame.draw.line(self.image,(0,255,0),(14,14),(0,14),2)
        pygame.draw.line(self.image,(0,255,0),(0,14),(0,0),2)

    def update(self):
        self.rect.right = 16*pygame.mouse.get_pos()[0]//16
        self.rect.bottom = 16*pygame.mouse.get_pos()[1]//16

        
