import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, file, rect, flipx, flipy, animated, frames):
        super().__init__(groups)
        self.animated = animated
        self.file = pygame.image.load(file).convert_alpha()
        self.flipx = flipx
        self.flipy = flipy
        self.pos = rect.topleft
        if animated:
            self.count = 0
            self.frames = frames
            self.curFrame = 0
            self.curRect = (self.curFrame*TILEMAPSIZE+self.pos[0], self.pos[1], TILEMAPSIZE, TILEMAPSIZE)
            self.image = pygame.transform.scale(pygame.transform.flip(self.file.subsurface(self.curRect), flipx, flipy), (TILESIZE, TILESIZE))
        else:
            self.image = pygame.transform.scale(pygame.transform.flip(self.file.subsurface(rect), flipx, flipy),(TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -10)

    def update(self):
        if self.animated:
            self.count += 1
            if self.count % 8 == 0:
                self.curFrame += 1
                if self.curFrame >= self.frames:
                    self.curFrame = 0
                self.curRect = (self.curFrame * TILEMAPSIZE+self.pos[0], self.pos[1], TILEMAPSIZE, TILEMAPSIZE)
                self.image = pygame.transform.scale(
                    pygame.transform.flip(self.file.subsurface(self.curRect), self.flipx, self.flipy),
                    (TILESIZE, TILESIZE))
