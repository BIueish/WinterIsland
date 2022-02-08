import pygame
from pygame.locals import *
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle):
        super().__init__(groups)
        self.walkRect = [0, 0, TILEMAPSIZE, TILEMAPSIZE]
        self.file = pygame.image.load("Walk.png").convert_alpha()
        self.image = pygame.transform.scale(self.file.subsurface(self.walkRect), (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.curFrame = 0
        self.count = 0
        self.obstacle = obstacle
        self.hitbox = self.rect.inflate(0, -26)

    def walk(self):
        if self.direction.x != 0 or self.direction.y != 0:
            self.count += 1
            if self.count%8 == 0:
                self.curFrame += 1
                if self.curFrame == 4:
                    self.curFrame = 0
                self.walkRect[1] = self.curFrame*TILEMAPSIZE
        else:
            self.walkRect[1] = 0

    def update(self):
        self.input()
        self.move(self.speed)
        self.walk()
        self.image = pygame.transform.scale(self.file.subsurface(self.walkRect), (TILESIZE, TILESIZE))

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collision("h")
        self.hitbox.y += self.direction.y * speed
        self.collision("v")
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'h':
            for sprite in self.obstacle:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'v':
            for sprite in self.obstacle:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.direction.x = -1
            self.walkRect[0] = 32
        elif keys[K_RIGHT]:
            self.direction.x = 1
            self.walkRect[0] = 48
        else:
            self.direction.x = 0
        if keys[K_UP]:
            self.direction.y = -1
            self.walkRect[0] = 16
        elif keys[K_DOWN]:
            self.direction.y = 1
            self.walkRect[0] = 0
        else:
            self.direction.y = 0
