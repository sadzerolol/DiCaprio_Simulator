import pygame
from wolf import Wolf
from hunter import Hunter
from wanderer import Wanderer
from pack import Pack
from wallfear import WallFear

"""Deer entity"""

class Deer(Wanderer, Pack, WallFear):

    view_distance = 100
    align_tocenter = 50
    desired_sep = 20
    coh_tocenter = 1000

    def __init__(self, location, family_id=0, **kwargs):
        super().__init__(location=location,tocenter=5,colour=(102, 51, 0),**kwargs)
        self.family_id = family_id

    def reload(self, objs, dt):
        family = list()
        animals = list()
        for obj in objs:
            if isinstance(obj, Deer) and obj.family_id == self.family_id:
                family.append(obj)
            elif isinstance(obj, (Wolf, Hunter)):
                animals.append(obj)

        wander = self.wander(dt)
        separate_animals = self.separate(animals, self.view_distance)
        walls = self.avoid_wall()
        align = self.align(family, self.align_tocenter)
        separate = self.separate(family, self.desired_sep)
        cohase = self.cohase(family, self.coh_tocenter)

        self.apply(wander*0.2)
        if separate_animals.length() > 0:
            self.apply(separate_animals*2)
        else:
            self.apply(separate*3)
            self.apply(align)
            self.apply(cohase)
        self.apply(walls*2)
        super().reload(dt)