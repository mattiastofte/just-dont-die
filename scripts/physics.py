import pygame
from pygame import *
from pygame.locals import *
import random
import numpy as np
from rendering import camera
from assets import *

# FEATURES
# Entities: simple rectangular hitboxes, elasisity from 0-1, solid or movable.
# Physics: position, velocity, acceleration, forces, displacement.
# Collisions: normal collisions or bouncy collisions.

# STORAGE
dict_entities = {}
active_entities = []
active_particles = []

#def Vector(x,y):
#    return np.array([x,y])

class Entity(pygame.sprite.Sprite):
    def __init__(self, name, pos, forces={}, vel=[0,0]):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.pos = pos
        self.vel = vel
        self.forces = forces
        self.image = pygame.image.load('assets/green.png')
        self.rect = self.image.get_rect()

    def update(self, time_delta):
        for force in self.forces:
            self.vel[0] += self.forces[force][0]*time_delta
            self.vel[1] += self.forces[force][1]*time_delta
        self.pos[0] += self.vel[0]
        self.pos[1] -= self.vel[1]
        self.rect.center = [self.pos[0]+camera[0],self.pos[1]+camera[1]]
        pygame.sprite.collide_mask(self,test_map)

class Map(pygame.sprite.Sprite):
    def __init__(self,map):
        pygame.sprite.Sprite.__init__(self)
        self.image = Generate_Map(map)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = [camera[0],camera[1]]

#class Entity:
#    def __init__(self, name, pos, size, forces={}, vel=[0,0]):
#        self.name = name
#        self.pos = pos
#        self.vel = vel
#        self.size = size
#        self.forces = forces
#        dict_entities.update({self.name:self})
#        active_entities.append(self)

#    def rect(self):
#        return pygame.Rect(int(self.pos[0]+camera[0]),int(self.pos[1]+camera[1]),int(self.size[0]),int(self.size[1]))

#    def update(self, time_delta):
#        for force in self.forces:
#            self.vel[0] += self.forces[force][0]*time_delta
#            self.vel[1] += self.forces[force][1]*time_delta
#        self.pos[0] += self.vel[0]
#        self.pos[1] -= self.vel[1]

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

def Impulse(pos,strength,entities):
    for entity in entities:
        force_vector = np.array([-1*(pos[0]-entity.x),(pos[1]-entity.y)])
        scalar = strength/(np.linalg.norm(force_vector))**1.5
        entity.forces.update({"explosion":list(force_vector*scalar)})
    

class Point_Gravity:
    def __init__(self,pos,strength):
        self.x = pos[0]
        self.y = pos[1]
        self.strength = strength
    
    def update(self, entities):
        for entity in entities:
            force_vector = np.array([(self.x-entity.x),-1*(self.y-entity.y)])
            scalar = self.strength/(np.linalg.norm(force_vector))**2 # finner lengden av vektoren
            entity.forces.update({"point":list(force_vector*scalar)})

def Physics_Engine():
    pass

def Update_Entities(time_delta):
    for entity in active_entities:
        entity.update(time_delta)

