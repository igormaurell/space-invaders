import pygame

from game.menu import *
from game import *

def main():
    WIDTH = 640
    HEIGHT = 480

    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()

    screen_size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Space Invaders")
    menu = GameMenu('Space Invaders', screen, 60)
    sequence = menu.run()
    if sequence == 1:
        stage = Stage(screen, 60)

        stage.start()
    else:
        print("Records aqui!")
        #SHOW RECORDS!!!

main()
