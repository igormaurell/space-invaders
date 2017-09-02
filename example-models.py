import pygame
from pygame.locals import *
from pygame.sprite import Group, GroupSingle, groupcollide, spritecollide

from random import randint

from game import *

WIDTH = 640
HEIGHT = 480

def main():
    pygame.init()

    screen_size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(screen_size)

    pygame.display.set_caption("Space Invaders")

    player = Player('player', (200, 440), 4)

    monstersShots = Group()
    monsters = Group()
    for x in range(0, 640, 64):
        monsters.add(Monster('monster1', (x, 100), 2))

    countSinceLastEnemyShot = 0

    bg = pygame.image.load('data/backgrounds/3.png').convert_alpha()
    screen.blit(bg, (0, 0))

    done = False
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        keys = pygame.key.get_pressed()

        if keys[K_LEFT] or keys[K_a]:
            player.setSpeed((-1, 0))
        if keys[K_RIGHT] or keys[K_d]:
            player.setSpeed((1, 0))
        player.do()

        for monster in monsters:
            monster.do()

        map = pygame.sprite.RenderUpdates()
        
        screen.blit(bg, (0, 0))

        map.update()
        map.draw(screen)

        #Player-Shot collision with monster
        collided = groupcollide(player.shots, monsters, True, False)
        for key, values in collided.items():
            for value in values:
                value.life -= 1
                player.score += 1

        #Monsters-Shots collision with player
        collided = spritecollide(player, monstersShots, True)
        if(collided != None):
            player.life -= 1

        player.update()
        player.draw(screen)

        #Select random enemy to shot
        indexMonShooting = randint(0, len(monsters))
        if(countSinceLastEnemyShot > 30):
            for i, monster in enumerate(monsters):
                if(i == indexMonShooting):
                    monster.shoot(4, (0, 1), '3')
                    countSinceLastEnemyShot = 0
        else:
            countSinceLastEnemyShot += 1

        for monster in monsters:
            monster.update()
            monster.draw(screen)

        pygame.display.flip()

        pygame.time.Clock().tick(60)

main()
