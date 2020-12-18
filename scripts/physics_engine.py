import pygame
import random
import numpy as np
from rendering_engine import camera

# FEATURES
# Entities: simple rectangular hitboxes, elasisity from 0-1, solid or movable.
# Physics: position, velocity, acceleration, forces, displacement.
# Collisions: normal collisions or bouncy collisions.

# STORAGE
entities_active = []
entities_dict = {}
active_particles = []

def Vector(x,y):
    return np.array([x,y])

class Entity:
    def __init__(self, name, pos, size, movement=[0,0,0,0]):
        self.name = name
        self.x = pos[0]+camera[0]
        self.y = pos[1]+camera[1]
        self.width = size[0]
        self.height = size[1]
        self.x_a = movement[0]
        self.y_a = movement[1]
        self.x_v = movement[2]
        self.y_v = movement[3]
        self.forces = {}
        entities_dict.update({self.name:self})
        entities_active.append(self)

    def rect(self):
        return pygame.Rect(int(self.x+camera[0]),int(self.y+camera[1]),int(self.width),int(self.height))

    def update(self, time_delta):
        self.x_a = 0
        self.y_a = 0
        for force in self.forces:
            vector = self.forces[force]
            self.x_a += vector[0] 
            self.y_a += vector[1]
        self.x_v += self.x_a
        self.y_v += self.y_a
        self.x += self.x_v
        self.y -= self.y_v

    def update_force(self,force_name,vector):
        pass
            
        
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