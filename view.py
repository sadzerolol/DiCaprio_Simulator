import pygame
from model import Model

"""Magic converter from vector based loc to pix loc"""
class observe(object):

    def __init__(self, x, y, width, height, scale=1):
        # top left point of observe box
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.scale = scale

    def set_center(self, location):
        """Switch loc to passed center."""
        self.x = location.x - self.width*self.scale/2
        self.y = location.y + self.height*self.scale/2

    def adjust(self, location):
        """Convert loc from cort loc to relative"""
        return pygame.Vector2((location.x - self.x)/self.scale,(self.y - location.y)/self.scale)

    def to_location(self, pixel_location):
        return pygame.Vector2((pixel_location.x * self.scale + self.x),(self.y - pixel_location.y * self.scale))

class View():
    """"Show of model and HUD"""
    TEXT_colour = (1, 1, 1)
    HUD_BACGROUND_colour = (255,247,0)
    BACKGROUND_colour = (1, 1, 1)

    winter_colour = (232, 236, 232)
    grid_colour = (232, 236, 232)

    def __init__(self, screen, model, scale):
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        self.observe = observe(0, 0, self.width, self.height, scale)
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.hud_surface = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.hud_surface.fill(View.HUD_BACGROUND_colour)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)

        self.model = model
        self.moving_direction = pygame.Vector2(0, 0)

    def repaint(self):
        """repaint screen accelerationording to model of game."""
        if self.model.hunter.is_exist:
            self.observe.set_center(self.model.hunter.location)

        self.screen.fill(View.BACKGROUND_colour)
        self.paint_winter()
        self.paint_grid()
        self.model.paint(self.observe, self.screen)
        if self.model.hunter.is_exist:
            self.draw_hud()

        pygame.display.flip()

    def start(self):
        """Loop game"""
        vector_map = {
            pygame.K_w: pygame.Vector2(0, 1),
            pygame.K_s: pygame.Vector2(0, -1),
            pygame.K_a: pygame.Vector2(-1, 0),
            pygame.K_d: pygame.Vector2(1, 0),
        }

        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in vector_map:
                        self.moving_direction += vector_map[event.key]
                if event.type == pygame.KEYUP:
                    if event.key in vector_map:
                        self.moving_direction -= vector_map[event.key]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.model.shoot(self.observe)

            self.repaint()
            self.reload()

    def reload(self):
        target = self.observe.to_location(
            pygame.Vector2(
                pygame.mouse.get_pos()))
        self.model.reload(self.delta_time(), target)
        self.model.go(self.moving_direction)

    def paint_winter(self):
        top_left = self.observe.adjust(self.model.dimension[0])
        top_right = self.observe.adjust(
            pygame.Vector2(
                self.model.dimension[1].x,
                self.model.dimension[0].y))

        bottom_right = self.observe.adjust(self.model.dimension[1])
        bottom_left = self.observe.adjust(
            pygame.Vector2(
                self.model.dimension[0].x,
                self.model.dimension[1].y))

        pygame.draw.polygon(
            self.screen,
            self.winter_colour,
            (top_left, top_right, bottom_right, bottom_left))

    def paint_grid(self, step=50):
        """Draw grid if needed"""
        top_left = self.model.dimension[0]
        bottom_right = self.model.dimension[1]

        x = top_left.x
        while x <= bottom_right.x:
            start = pygame.Vector2(x, top_left.y)
            end = pygame.Vector2(x, bottom_right.y)
            pygame.draw.line(
                self.screen,
                self.grid_colour,
                self.observe.adjust(start),
                self.observe.adjust(end))
            x += step

        y = bottom_right.y
        while y <= top_left.y:
            start = pygame.Vector2(bottom_right.x, y)
            end = pygame.Vector2(top_left.x, y)
            pygame.draw.line(
                self.screen,
                self.grid_colour,
                self.observe.adjust(start),
                self.observe.adjust(end))
            y += step

    def draw_text(self, surface, text, location, colour=TEXT_colour, align_center=False):
        text_surface = self.font.render(text, True, colour)
        location = list(location)
        if align_center:
            location[0] -= text_surface.get_width() // 2
            location[1] -= text_surface.get_height() // 2
        surface.blit(text_surface, location)

    def draw_hud(self, padding=(8, 5)):
        bullets_text = 'Bullets: {:6}'.format(self.model.hunter.bullets_left)
        self.paint_hud_item(
             (15, self.height - 30 - 2*padding[1]),(bullets_text,),10,padding)

        frags_text = 'frags: {:6}'.format(self.model.hunter.frags)
        self.paint_hud_item((self.width - 150, 15),(frags_text,),10,padding)

    def paint_hud_item(self, location, lines, maxchars, padding):
        # seacrh max line width
        max_width = max(map(lambda line: self.font.size(line)[0], lines))
        font_height = self.font.get_height()
        # size of HUD item background
        item_size = (
            max_width + 2*padding[0], 
            font_height*len(lines) + 2*padding[1])
        # scaling transparent HUD background
        item_surface = pygame.transform.scale(self.hud_surface, item_size)
        # draw each line
        for i, line in enumerate(lines):
            self.draw_text(
                item_surface,
                line,
                (padding[0], padding[1] + font_height*i))
        self.screen.blit(item_surface, location)

    def delta_time(self):
        return self.clock.tick(self.fps) / 1000
    
