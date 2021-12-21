import pygame

from object import Object

class Shot(Object):

    def __init__(self, location):
        super().__init__(location=location,tocenter=3,colour=(1, 1, 1))

    def reload(self, objs, dt):
        super().reload(dt)

    def paint(self, observe, surface, direction=None, triangle=False):
        super().paint(observe, surface, direction, triangle)