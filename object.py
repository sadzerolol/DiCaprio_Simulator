import math
from abc import ABC, abstractmethod
import pygame
"""Parent of the things that can influence on the game"""
class Object(ABC):
    @abstractmethod
    def __init__(self,location, tocenter, colour,maxspeed=500, maxforce=1000):
        self.location = pygame.Vector2(location) if location else pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration =  pygame.Vector2(0, 0)
        self.maxspeed = maxspeed
        self.maxforce = maxforce
        self.is_exist = True
        self.tocenter = tocenter
        self.colour = colour
    @classmethod
    #draw to border
    def to_border_colour(cls, colour):
        mult = 0.8
        return [part*mult for part in colour]
    #set limit on the vector
    @classmethod
    def vec_limit(cls, vec, limit):
        vec = pygame.Vector2(vec)
        if vec.length() >= limit:
            vec.scale_to_length(limit)
        return vec

    def paint(self, observe, surface, direction=None, triangle=True):
        if not triangle:
            pygame.draw.circle(surface, self.colour, observe.adjust(self.location), self.tocenter)
            return
        # paint shots
        side_len = (3*self.tocenter)/math.sqrt(3)

        dot1 = direction if direction else self.direction()
        dot1.scale_to_length(self.tocenter)

        dot2 = pygame.Vector2(dot1).rotate(150)
        dot2.scale_to_length(side_len)

        dot3 = pygame.Vector2(dot2).rotate(60)
        dot3.scale_to_length(side_len)

        dot1 += self.location
        dot2 += self.location
        dot3 += self.location

        dots = (observe.adjust(dot1), observe.adjust(dot2), observe.adjust(dot3))
        pygame.draw.polygon(surface, self.colour, dots, width=0)
        pygame.draw.polygon(surface, self.to_border_colour(self.colour), dots,width=1)
    
    def apply(self, force):
        force_cp = self.safe_normalize(force)
        force_cp.scale_to_length(force.length())
        self.acceleration += force_cp

    def kill(self):
        self.is_exist = False

    def reload(self, dt):

        self.velocity += self.acceleration * dt
        self.velocity = self.vec_limit(self.velocity, self.maxspeed)

        self.location += self.velocity * dt
        self.acceleration = pygame.Vector2(0, 0)

    def is_collide(self, obj):
        if self.location.distance_to(obj.location) < self.tocenter + obj.tocenter:
            return True
        return False

    def direction(self):
        return self.safe_normalize(self.velocity)

    def safe_normalize(self, vec):
        try:
            return vec.normalize()
        except ValueError:
            return pygame.Vector2(0, 1)

