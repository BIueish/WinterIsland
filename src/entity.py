import math
import pygame
from pygame.locals import *
from pygame.gfxdraw import *
from settings import *


class Entity(pygame.sprite.Sprite):
    def __init__(self, file, pos, groups, rect, lines, face, options):
        super().__init__(groups)
        self.image = pygame.transform.scale(pygame.image.load(file).subsurface(rect).convert_alpha(), (TILESIZE, TILESIZE))
        self.face = pygame.transform.scale(pygame.image.load(face).convert_alpha(), (200, 200))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        self.sentences = lines
        self.curLine = -1
        self.talkimg = pygame.transform.scale(pygame.image.load("../Images/Extra/talk.png").convert_alpha(), (32, 16))
        self.talking = False
        self.font = pygame.font.Font("../Fonts/PressStart2P-Regular.ttf", 25)
        self.talkCount = 0
        self.curLetter = 0
        self.curSentence = ''
        self.curLetterCount = 0
        self.optionString = ''
        self.options = []
        self.optionsList = options
        self.curOption = 0

    def talk(self, player):
        if len(self.sentences) > 0:
            dist = math.sqrt((player.rect.left-self.rect.left)**2+(player.rect.top-self.rect.top)**2)
            if dist <= 100.0:
                pygame.display.get_surface().blit(self.talkimg, (self.rect.left+16-player.rect.x+HALF_WIDTH, self.rect.top-20-player.rect.y+HALF_HEIGHT))
                self.talking = True
            else:
                self.talking = False
            if self.talking:
                keys = pygame.key.get_pressed()
                if self.talkCount > 0:
                    self.talkCount -= 1
                if keys[K_DOWN]:
                    self.curOption += 1
                    if self.curOption == len(self.options):
                        self.curOption = len(self.options)-1
                elif keys[K_UP]:
                    self.curOption -= 1
                    if self.curOption < 0:
                        self.curOption = 0
                if keys[K_SPACE] and self.talkCount == 0:
                    if len(self.options) == 0:
                        self.curLine += 1
                        while self.curLine in self.optionsList:
                            self.curLine += 1
                    else:
                        self.curLine = int(self.options[self.curOption][-1])
                    player.talking = True
                    self.curLetter = 0
                    self.curSentence = ''
                    self.curLetterCount = 0
                    self.options = []
                    self.curOption = 0
                    if self.curLine == len(self.sentences):
                        self.curLine = -1
                        self.talking = False
                        player.talking = False
                    self.talkCount = 15
                    self.optionString = self.sentences[self.curLine].split('<o>')
                    if len(self.optionString) > 1:
                        self.options = self.optionString[1].split('<>')
                if self.curLine != -1:
                    if self.curLetter < len(self.optionString[0]) and self.curLetterCount%TALK_SPEED == 0:
                        self.curSentence += self.optionString[0][self.curLetter]
                        self.curLetter += 1
                    self.curLetterCount += 1
                    pygame.draw.rect(pygame.display.get_surface(), "White", (20, 20, WIDTH-40, 210))
                    pygame.draw.rect(pygame.display.get_surface(), "Black", (20, 20, WIDTH-40, 210), 5)
                    filled_trigon(pygame.display.get_surface(), WIDTH-60, 190, WIDTH-50, 195, WIDTH-60, 200, (0, 0, 0))
                    text = self.font.render(self.curSentence, False, "Black")
                    pygame.display.get_surface().blit(text, (240, 40))
                    y = 50
                    for index, option in enumerate(self.options):
                        text = self.font.render(option[:-1], False, "Black")
                        pygame.display.get_surface().blit(text, (260, 40+y))
                        if index == self.curOption:
                            filled_trigon(pygame.display.get_surface(), 240, 45+y, 250, 50+y, 240, 55+y, (0, 0, 0))
                        y += 50
                    pygame.display.get_surface().blit(self.face, (25, 25))

