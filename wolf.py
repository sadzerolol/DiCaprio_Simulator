import pygame
from wanderer import Wanderer
from pack import Seeker
from wallfear import WallFear
class Wolf(Seeker, Wanderer, WallFear):

    view_radius = 100
    aggr_distance = 8
    hungry_coeff = 3

    def __init__(self, location, **kwargs):
        super().__init__(location=location,tocenter=4,colour=(0, 0, 0),
            **kwargs)
        self.helth = 100

    def reload(self, objs, dt):
        self.reload_helth(dt)
        if self.helth <= 0:
            objs.rego(self)
            return

        min_dist = float('inf')
        prey = None
        for obj in objs:
            if not isinstance(obj, Wolf):
                dist = self.location.distance_to(obj.location)
                if dist < self.aggr_distance:
                    obj.kill()
                    objs.remove(obj)
                    self.helth = 100
                elif dist < self.view_radius and dist < min_dist:
                    min_dist = dist
                    prey = obj

        wander = self.wander(dt)
        walls = self.avoid_wall()

        if prey:
            seek = self.seek(prey.location)
            self.apply(seek*2)
        else:
            self.apply(wander*0.3)
    
        self.apply(walls*2)

        super().reload(dt)

    def reload_helth(self, dt):
        self.helth -= self.hungry_coeff*dt