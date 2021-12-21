from seeker import Seeker
import pygame
"""Pack logic"""
class Pack(Seeker):
    des_sep = 20
    align_tocenter = 50
    coh_tocenter = 50

    def separate(self, objects, desired_separation=des_sep):
        sum_vec = pygame.Vector2(0, 0)
        amount = 0

        for obj in objects:
            dist = self.location.distance_to(obj.location)

            if dist > 0 and dist < desired_separation:
                diff_vec = self.location - obj.location
                diff_vec.normalize_ip()
                diff_vec /= dist

                sum_vec += diff_vec
                amount += 1

        if sum_vec.length() > 0:
            sum_vec /= amount
            sum_vec.normalize_ip()
            sum_vec *= self.maxspeed

            steer = sum_vec - self.velocity
            steer = self.vec_limit(steer, self.maxforce)
            return steer
        else:
            return pygame.Vector2(0, 0)

    def align(self, objects, align_tocenter=align_tocenter):
        amount = 0
        sum_vec = pygame.Vector2(0, 0)
        for obj in objects:
            dist = self.location.distance_to(obj.location)

            if dist > 0 and dist < align_tocenter:
                sum_vec += obj.velocity
                amount += 1

        # if amount > 0:
        if sum_vec.length() > 0:
            sum_vec /= amount

            sum_vec.scale_to_length(self.maxspeed)

            steer = sum_vec - self.velocity
            steer = self.vec_limit(steer, self.maxforce)
            return steer
        else:
            return pygame.Vector2(0, 0)

    def cohase(self, objects, cohesion_tocenter=coh_tocenter):
        sum_vec = pygame.Vector2(0, 0)
        amount = 0

        for obj in objects:
            dist = self.location.distance_to(obj.location)

            if dist > 0 and dist < cohesion_tocenter:
                sum_vec += obj.location
                amount += 1

        if sum_vec.length() > 0:
            sum_vec /= amount
            return self.seek(sum_vec)
        else:
            return pygame.Vector2(0, 0)