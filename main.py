import pygame

from game import *

def main():
    WIDTH = 640
    HEIGHT = 480

    pygame.init()

    screen_size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(screen_size)

    pygame.display.set_caption("Space Invaders")

    stage = Stage('stage3', screen, 60)
    stage.start()

main()
