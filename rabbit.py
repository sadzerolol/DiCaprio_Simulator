import pygame
from wanderer import Wanderer
from pack import Pack
from wallfear import WallFear

class Rabbit(Wanderer, Pack, WallFear):

    view_radius = 100

    def __init__(self, location, **kwargs):
        super().__init__(location=location,tocenter=5,colour=(153, 153, 102),
            **kwargs)

    def reload(self, objs, dt):
        wander = self.wander(dt)
        separate = self.separate(objs, self.view_radius)
        walls = self.avoid_wall()
        
        self.apply(wander*0.4)
        self.apply(separate)
        self.apply(walls*2)

        super().reload(dt)