from object import Object
import pygame
class WallFear(Object):

    wallfear = 100

    def __init__(self, 
            walls_rect=(
                pygame.Vector2(-450, 300),
                pygame.Vector2(450, -300)),
            **kwargs):
        super().__init__(**kwargs)
        self.walls_rect = walls_rect

    def avoid_wall(self):
        top_left = self.walls_rect[0]
        bottom_right = self.walls_rect[1]

        desired = pygame.Vector2(0, 0)
        if self.location.x < top_left.x + self.wallfear:     
            desired += pygame.Vector2(self.maxspeed, self.velocity.y)
        elif self.location.x > bottom_right.x - self.wallfear:
            desired += pygame.Vector2(-self.maxspeed, self.velocity.y)

        if self.location.y > top_left.y - self.wallfear:     
            desired += pygame.Vector2(self.velocity.x, -self.maxspeed)
        elif self.location.y < bottom_right.y + self.wallfear:
            desired += pygame.Vector2(self.velocity.x, self.maxspeed)

        if desired.length() > 0:
            steer = desired - self.velocity
            steer = self.vec_limit(steer, self.maxforce)
            steer.scale_to_length(self.maxforce)
            return steer
        else:
            return pygame.Vector2(0, 0)