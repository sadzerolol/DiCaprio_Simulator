import random
import pygame
from object import Object


class Wanderer(Object):
    #per second
    change_angle = 45*12
    distance_range = (65, 100)
    radius_range = (50, 60)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wander_angle = 0
        self.wander_distance = random.randint(*self.distance_range)
        self.wander_tocenter = random.randint(*self.radius_range)

    def wander(self, dt):
        delta_angle = self.change_angle*dt
        is_add_angle = random.choice([True, False])

        if is_add_angle:
            self.wander_angle += delta_angle
        else:
            self.wander_angle -= delta_angle

        delta_location = self.direction()
        delta_location.scale_to_length(self.wander_distance)
        future_location = self.location + delta_location

        wander_tocenter_vec = self.direction().rotate(self.wander_angle)
        wander_tocenter_vec.scale_to_length(self.wander_tocenter)
        target = future_location + wander_tocenter_vec

        desired = target - self.location
        desired.scale_to_length(self.maxspeed)

        steer = desired - self.velocity
        steer = self.vec_limit(steer, self.maxforce)
        return steer