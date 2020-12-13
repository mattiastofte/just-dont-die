import pygame
import random

# FEATURES
# Entities: simple rectangular hitboxes, elasisity from 0-1, solid or movable.
# Physics: position, velocity, acceleration, forces, displacement.
# Collisions: normal collisions or bouncy collisions.

active_entities = []
active_particles = []

class Entity:
    def __init__(self, pos, size, movement=[0,0,0,0]):
        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.x_a = movement[0]
        self.y_a = movement[1]
        self.x_v = movement[2]
        self.y_v = movement[3]
        active_entities.append(self)

    def rect(self):
        return pygame.Rect(int(self.x),int(self.y),int(self.width),int(self.height))

    def update(self, time_delta, forces):
        self.x_a = 0
        self.y_a = 0
        for force in forces:
            vector = forces[force]
            self.x_a += vector[0] 
            self.y_a += vector[1]
        self.x_v += self.x_a
        self.y_v += self.y_a
        self.x += self.x_v
        self.y -= self.y_v
            
        
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