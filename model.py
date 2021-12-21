import pygame
import random
from rabbit import Rabbit
from deer import Deer
from wolf import Wolf
from hunter import Hunter

"""Display the state of the game"""

class Model():
    

    def __init__(self, dimension, rabbits, wolves, packs):
        
        # vector based dimension of the map
        self.dimension = (
            pygame.Vector2(-dimension[0]/2, dimension[1]/2),
            pygame.Vector2(dimension[0]/2, -dimension[1]/2))

        self.hunter = Hunter((0, 0))
        
        self.objects = [self.hunter]

        self.create_rabbits(rabbits)
        self.create_packs(packs, (3, 10))
        self.create_wolves(wolves)

    def reload(self, dt, target):
        for obj in self.objects:
            obj.reload(self.objects, dt)

            if self.is_fall_out(obj):
                self.objects.remove(obj)

    def go(self, direction):
        if self.hunter.is_exist:
            self.hunter.go(direction)

    def is_fall_out(self, obj):
        if obj.location.x < self.dimension[0].x or obj.location.x > self.dimension[1].x or \
                obj.location.y > self.dimension[0].y or obj.location.y < self.dimension[1].y:
            return True
        return False

    def shoot(self, observe):
        if self.hunter.is_exist:
            mouse_location = observe.to_location(
                    pygame.Vector2(
                        pygame.mouse.get_pos()))
            direction =  mouse_location - self.hunter.location
            self.hunter.shoot(direction)

    def paint(self, observe, surface):
        #paint the rest of the cells
        for obj in self.objects:
            if isinstance(obj, Hunter):
                target = observe.to_location(
                    pygame.Vector2(pygame.mouse.get_pos()))
                obj.paint(observe, surface, target - obj.location)
                continue

            obj.paint(observe, surface)

    def create_rabbits(self, amount):
        for i in range(amount):
            location = self.get_random_location()
            self.objects.append(
                Rabbit(location, walls_rect=self.dimension))

    def create_packs(self, families_amount, flock_size_range):
        for family_id in range(families_amount):
            location = self.get_random_location()
            flock_size = random.randint(*flock_size_range)
            for j in range(flock_size):
                self.objects.append(
                    Deer(location, family_id=family_id, walls_rect=self.dimension))

    def create_wolves(self, amount):
        for i in range(amount):
            location = self.get_random_location()
            self.objects.append(
                Wolf(location, walls_rect=self.dimension))

    def get_random_location(self):
        x = random.randint(
            self.dimension[0].x,
            self.dimension[1].x)
        y = random.randint(
            self.dimension[1].y,
            self.dimension[0].y)
        return pygame.Vector2(x, y)