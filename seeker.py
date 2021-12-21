from object import Object
import pygame
"""Logic of seeking behaviour"""
class Seeker(Object):

    def seek(self, target):
        desired = target - self.location
        desired.scale_to_length(self.maxspeed)

        steer = desired - self.velocity
        steer = self.vec_limit(steer, self.maxforce)
        return steer

    def arrive(self, target, arrive_tocenter=300):
        desired = target - self.location
        dist = desired.length()

        if dist < arrive_tocenter:
            speed = (dist/arrive_tocenter)*self.maxspeed
            desired.scale_to_length(speed)
        else:
            desired.scale_to_length(self.maxspeed)

        steer = desired - self.velocity
        steer = self.vec_limit(steer, self.maxforce)
        return steer