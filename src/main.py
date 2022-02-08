import pygame, sys
from pygame.locals import *
from settings import *
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.displaysurf = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.DOUBLEBUF | pygame.RESIZABLE, vsync=True)
        pygame.display.set_caption("Top Down")
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            self.displaysurf.fill("black")
            self.level.run()
            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
