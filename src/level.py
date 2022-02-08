import pygame
import pygame.sprite
import json
from settings import *
from tile import Tile
from player import Player
from entity import Entity


class Level:
    def __init__(self):
        self.displaysurf = pygame.display.get_surface()
        self.visible = YSortCameraGroup()
        self.obstacle = pygame.sprite.Group()
        self.floor = Floor()
        self.create_map()

    def create_map(self):
        world = open(WORLD_MAP, 'r')
        data = json.loads(world.read())
        levels = data["levels"]
        tileset = {0:4, 16:4}
        tilesets = data["defs"]["tilesets"]
        level = levels[0]["layerInstances"][1]
        tiles = level["gridTiles"]
        floor = levels[0]["layerInstances"][2]["gridTiles"]
        animated = levels[0]["layerInstances"][3]["gridTiles"]
        animatedTile = levels[0]["layerInstances"][3]["__tilesetRelPath"]
        for tile in floor:
            Tile((tile["px"][0]*(TILESIZE/TILEMAPSIZE), tile["px"][1]*(TILESIZE/TILEMAPSIZE)), [self.floor], level["__tilesetRelPath"], pygame.rect.Rect(tile["src"][0], tile["src"][1], TILEMAPSIZE, TILEMAPSIZE), tile["f"] == 1 or tile["f"] == 3, tile["f"] >= 2, False, 1)
        for tile in tiles:
            Tile((tile["px"][0]*(TILESIZE/TILEMAPSIZE), tile["px"][1]*(TILESIZE/TILEMAPSIZE)), [self.visible, self.obstacle], level["__tilesetRelPath"], pygame.rect.Rect(tile["src"][0], tile["src"][1], TILEMAPSIZE, TILEMAPSIZE), tile["f"] == 1 or tile["f"] == 3, tile["f"] >= 2, False, 1)
        for tile in animated:
            Tile((tile["px"][0] * (TILESIZE / TILEMAPSIZE), tile["px"][1] * (TILESIZE / TILEMAPSIZE)),
                 [self.visible, self.obstacle], animatedTile,
                 pygame.rect.Rect(tile["src"][0], tile["src"][1], TILEMAPSIZE, TILEMAPSIZE),
                 tile["f"] == 1 or tile["f"] == 3, tile["f"] >= 2, True, tileset[tile["src"][1]])
        player = levels[0]["layerInstances"][0]["entityInstances"][0]
        self.player = Player((player["__grid"][0]*TILESIZE, player["__grid"][1]*TILESIZE), [self.visible], self.obstacle)
        entities = levels[0]["layerInstances"][0]["entityInstances"][1:]
        self.entities = []
        for entity in entities:
            for i in tilesets:
                if i["uid"] == entity["__tile"]["tilesetUid"]:
                    file = i["relPath"]
                    break
            self.entities.append(Entity(file, (entity["__grid"][0]*TILESIZE, entity["__grid"][1]*TILESIZE), [self.visible, self.obstacle], entity["__tile"]["srcRect"], entity["fieldInstances"][1]["__value"], entity["fieldInstances"][0]["__value"], entity["fieldInstances"][2]["__value"]))
        world.close()

    def run(self):
        self.floor.custom_draw(self.player)
        self.visible.custom_draw(self.player)
        self.visible.update()
        for entity in self.entities:
            entity.talk(self.player)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaysurf = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(100, 200)
        self.hw = self.displaysurf.get_width()/2
        self.hh = self.displaysurf.get_height()/2

    def custom_draw(self, player):
        self.offset.x = -player.rect.x+self.hw
        self.offset.y = -player.rect.y+self.hh
        for sprite in sorted(self.sprites(), key= lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft+self.offset
            self.displaysurf.blit(sprite.image, offset_pos)


class Floor(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaysurf = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(100, 200)
        self.hw = self.displaysurf.get_width() / 2
        self.hh = self.displaysurf.get_height() / 2

    def custom_draw(self, player):
        self.offset.x = -player.rect.x + self.hw
        self.offset.y = -player.rect.y + self.hh
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft + self.offset
            self.displaysurf.blit(sprite.image, offset_pos)

