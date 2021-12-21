import pygame
from view import View
from model import Model
pygame.init()
screen = pygame.display.set_mode((900,600))
model = Model((1500,1000),rabbits=5,wolves=2,packs=3)
entry_point = View(screen, model, 1.3)
entry_point.start()

