import pygame
import random

# FEATURES
# Entities: simple rectangular hitboxes, elasisity from 0-1, solid or movable.
# Physics: position, velocity, acceleration, forces, displacement.
# Collisions: normal collisions or bouncy collisions.

active_entities = []
active_particles = []

class Entity:
    def __init__(self, name, x, y, width, height, explode):
        self.id = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x_a = (random.random()*8)-4
        self.y_a = 0.2
        self.x_v = 0
        self.y_v = -1*(random.random()*4)
        self.explode = explode
        active_entities.append(self)

    def rect(self):
        return pygame.Rect(int(self.x),int(self.y),int(self.width),int(self.height))

    def update(self, time_delta):
        if self.y > 200:
            pass
            # active_entities.remove(self)
        self.x_a = self.x_a/2
        self.y_v += self.y_a
        self.x_v += self.x_a
        self.y += self.y_v
        self.x += self.x_v
        if self.width > 0:
            self.width -= 0.2
            self.height -= 0.2
        else:
            if self.explode == True:
                for i in range(10):
                    s = random.randint(2,8)
                    Entity(random.randint(10000,100000),self.x,self.y,s,s,False)
            active_entities.remove(self)
        
class Emitter:
    pass

class Particle:
    def __init__(self, x, y, width, height, explode):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x_v = (-8+random.random()*16)
        self.y_v = -1*(random.random()*6)
        self.explode = explode
        active_particles.append(self)

    def rect(self):
        return pygame.Rect(int(self.x),int(self.y),int(self.width),int(self.height))

    def update(self, time_delta):
        self.y_v += 0.25
        self.x_v = self.x_v/1.05
        self.y += self.y_v
        self.x += self.x_v
        if self.width > 0:
            self.width -= 0.1
            self.height -= 0.1
        else:
            if self.explode == True:
                for i in range(10):
                    Particle(self.x,self.y,3,3,False)
            active_particles.remove(self)