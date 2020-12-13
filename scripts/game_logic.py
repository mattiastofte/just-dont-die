import pygame
from pygame.locals import *

def Move_Entity(keys,entity):
    if keys[K_RIGHT]:
        entity.forces.update({"LEFT":[0.1,0]})
    else:
        if "LEFT" in entity.forces:
            entity.forces.pop("LEFT")
    if keys[K_LEFT]:
        entity.forces.update({"RIGHT":[-0.1,0]})
    else:
        if "RIGHT" in entity.forces:
            entity.forces.pop("RIGHT")
    if keys[K_SPACE]:
        entity.forces.update({"JUMP":[0,0.3]})
    else:
        if "JUMP" in entity.forces:
            entity.forces.pop("JUMP")