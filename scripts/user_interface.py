import pygame
from pygame.locals import *
from pygame import *
import modified_sprite

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
        
