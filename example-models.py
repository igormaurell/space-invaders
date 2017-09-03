import pygame
from pygame.locals import *
from pygame.sprite import Group, GroupSingle, groupcollide, spritecollide

from random import randint

from game import *

WIDTH = 640
HEIGHT = 480

CLOCK = pygame.time.Clock()

temp_effects = []

def main():

    #TODO: Work on a better way to make randomized shots
    framesSinceLastEnemyShot = 0
    lastMove = ""

    #Initialinz pygame and creating the main surface
    pygame.init()

    screen_size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(screen_size)

    pygame.display.set_caption("Space Invaders")

    #Creating objects of the stage
    #TODO: Include a stage reader from config files
    player = Player('player', (200, 440), 4)

    monsters = Group()
    for x in range(0, 640, 128):
        monsters.add(Monster('monster1', (x, 100), 2))

    #Setting the background
    bg = pygame.image.load('data/backgrounds/3.png').convert_alpha()
    screen.blit(bg, (0, 0))

    while 1:

        #Keyboard press and exit events
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            #elif event.type == pygame.KEYDOWN:
            #    if event.key == pygame.K_SPACE:
            #        player.shoot()

        #Keyboard hold
        keys = pygame.key.get_pressed()

        if keys[K_LEFT] or keys[K_a]:
            if(not player.touchingLeftBorder()):
                player.setSpeed((-1, 0))
        if keys[K_RIGHT] or keys[K_d]:
            if(not player.touchingRightBorder()):
                player.setSpeed((1, 0))
        if keys[K_SPACE]:
            player.attemptShoot(CLOCK)
        player.do()

        #Checking if monsters can be moved
        canMoveLeft = canMoveRight = True
        for monster in monsters:
            if(monster.touchingLeftBorder()):
                lastMove = "left"
                canMoveLeft = False
            if(monster.touchingRightBorder()):
                lastMove = "right"
                canMoveRight = False

        if(canMoveRight and lastMove == "left"):
            monsSpeed = (1,0)
        elif(canMoveLeft and lastMove == "right"):
            monsSpeed = (-1,0)
        else:
            monsSpeed = (0,0)

        for monster in monsters:
            monster.setSpeed(monsSpeed)
            monster.do()

        #Player-Shot collision with monster
        collided = groupcollide(player.shots, monsters, True, False)
        for key, values in collided.items():
            for value in values:
                value.life -= 1
                player.score += 1
                collision_pos = value.getPosition()
                temp_effects.append(TempEffect("hit_blue", "effects", collision_pos))

        #Monsters-Shots collision with player
        for monster in monsters:
            collided = spritecollide(player, monster.shots, True)
            if(len(collided)):
                player.life -= 1
                collision_pos = player.getPosition()
                temp_effects.append(TempEffect("hit_blue", "effects", collision_pos))

        #Select random enemy to shot and control time between shots
        indexMonShooting = randint(0, len(monsters))
        if((framesSinceLastEnemyShot > 30 and len(monsters) > 4) or \
           (framesSinceLastEnemyShot > 60)):
            for i, monster in enumerate(monsters):
                if(i == indexMonShooting):
                    monster.shoot(4, (0, 1), '3')
                    framesSinceLastEnemyShot = 0
        else:
            framesSinceLastEnemyShot += 1

        #Updating and rendering objects

        map = pygame.sprite.RenderUpdates()
        
        screen.blit(bg, (0, 0))

        map.update()
        map.draw(screen)


        player.update()
        if(player.life > 0):
            player.draw(screen)


        for monster in monsters:
            monster.update()
            monster.draw(screen)

        for i, tmp in enumerate(temp_effects):
            if(tmp.is_dead()):
                temp_effects.pop(i)
            else:
                tmp.update_time(CLOCK)
                tmp.draw(screen)

        pygame.display.flip()

        CLOCK.tick(60)

main()
