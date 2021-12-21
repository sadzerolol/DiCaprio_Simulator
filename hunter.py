import pygame
from object import Object
from shot import Shot

"""Hunter entity"""
class Hunter(Object):

    moving_force = 300
    bullet_speed = 500
    distance = 400
    spread = 1

    def __init__(self, location):
        super().__init__(location=location,tocenter=9,colour=(1, 1, 1),)
        self.bullets_left = 100
        self.frags = 0
        self.bullets = list()

    def reload(self, objs, dt):
        for bullet in self.bullets:
            bullet.reload(objs, dt)

            if self.location.distance_to(bullet.location) > self.distance:
                self.bullets.remove(bullet)
                continue

            for obj in objs:
                if bullet.is_collide(obj) and not isinstance(obj, Hunter):
                    objs.remove(obj)
                    self.frags += 1
            
        super().reload(dt)

    def go(self, direction):
        if direction.length() > 0:
            direction = pygame.Vector2(direction)
            direction.scale_to_length(self.moving_force)
            self.apply(direction)

    def paint(self, observe, surface, direction=None, triangle=True):
        for bullet in self.bullets:
            bullet.paint(observe, surface)

        super().paint(observe, surface, direction, triangle)

    def shoot(self, direction, shootgun=True):
        if self.bullets_left > 0:
            magazine = list()
            bullet = self.make_bullet(direction)
            magazine.append(bullet)
            self.bullets_left -= 1

            if shootgun and self.bullets_left >= 2:
                bullet = self.make_bullet(direction)
                bullet.velocity.rotate_ip(self.spread)
                magazine.append(bullet)

                bullet = self.make_bullet(direction)
                bullet.velocity.rotate_ip(-self.spread)
                magazine.append(bullet)

                self.bullets_left -=2

            self.bullets.extend(magazine)

    def make_bullet(self, direction):
        bullet = Shot(self.location)
        velocity = pygame.Vector2(direction)
        velocity.scale_to_length(self.bullet_speed)
        bullet.velocity = velocity
        return bullet