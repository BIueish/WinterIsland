import pygame
from settings import *


class Entity(pygame.sprite.Sprite):
    def __init__(self, file, pos, groups, rect):
        super().__init__(groups)
        self.image = pygame.transform.scale(pygame.image.load(file).subsurface(rect).convert_alpha(), (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
