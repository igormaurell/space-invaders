import pygame
from pygame.locals import *

from game import *


def main():
    pygame.init()

    screen_size = (640, 480)
    screen = pygame.display.set_mode(screen_size)

    pygame.display.set_caption("Space Invaders")

    player = Player('player', (200, 440), 4)
    monsters = []
    monsters.append(Monster('monster1', (200, 100), 2))

    bg = pygame.image.load('data/backgrounds/3.png')
    screen.blit(bg, (0, 0))

    done = False
    while 1:
        for event in pygame.event.get():
				if event.type == QUIT:
					exit()

        keys = pygame.key.get_pressed()

        if keys[K_LEFT] or keys[K_a]:
            player.setSpeed((-1, 0))
        if keys[K_RIGHT] or keys[K_d]:
            player.setSpeed((1, 0))
        player.do()

        if keys[K_SPACE]:
            player.shoot()

        for monster in monsters:
            monster.do()

        map = pygame.sprite.RenderUpdates()
        
        screen.blit(bg, (0, 0))

        map.update()
        map.draw(screen)

        player.update()
        player.draw(screen)

        for monster in monsters:
            monster.update()
            monster.draw(screen)

        pygame.display.flip()

        pygame.time.Clock().tick(50)

main()
