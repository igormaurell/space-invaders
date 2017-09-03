import pygame
from pygame.locals import *
from pygame.sprite import Group, GroupSingle, groupcollide, spritecollide

from random import randint

from game import *
import json

class Stage:
    def __init__(self, key, screen, fps = 50):
        self.key = key
        self.json_data = None
        self.screen = screen
        self.bg = None
        self.FPS = fps
        self.done = False
        self.CLOCK = None
        
        self.player = None
        self.monsters = Group()
    
    def start(self):
        config = json.loads(open('definitions/stages.json').read())
        config = config[self.key]

        self.bg = pygame.image.load(config['background']).convert_alpha()
        self.screen.blit(self.bg, (0, 0))

        entities_config = json.loads(open('definitions/entities.json').read())
        conf = entities_config['player']

        self.player = Player('player', tuple(config['player_position']),
        conf['shot'], conf['shot_speed'], conf['life'], conf['demage'])
     
        y = config['monsters_position'][1]
        for i in range(1, 5):
            line = config['line' + str(i)]
            x = config['monsters_position'][0]
            y_M = 0
            for c in line:
                conf = entities_config['monster' + c] 
                self.monsters.add(Monster('monster' + c, (x, y), conf['shot'],
                conf['shot_speed'], conf['life'], conf['demage'], conf['value']))
                x += conf['size'][0]
                if conf['size'][1]>y_M:
                    y_M = conf['size'][1]
            y += y_M

        self.run()

    def run(self):
        framesSinceLastEnemyShot = 0
        lastMove = "right"

        self.CLOCK = pygame.time.Clock()
        temp_effects = []

        while not self.done:
                #Keyboard press and exit events
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()

            #Keyboard hold
            keys = pygame.key.get_pressed()    
            if keys[K_LEFT] or keys[K_a]:
                if(not self.player.touchingLeftBorder()):
                    self.player.setSpeed((-1, 0))
            if keys[K_RIGHT] or keys[K_d]:
                if(not self.player.touchingRightBorder()):
                    self.player.setSpeed((1, 0))
            if keys[K_SPACE]:
                self.player.attempt_shoot(self.CLOCK)
            self.player.do()

            #Checking if monsters can be moved
            canMoveLeft = canMoveRight = True
            for monster in self.monsters:
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

            for monster in self.monsters:
                monster.setSpeed(monsSpeed)
                monster.do()

            #Player-Shot collision with monster
            collided = groupcollide(self.player.shots, self.monsters, True, False)
            for key, values in collided.items():
                for value in values:
                    value.life -= self.player.demage
                    if value.life == 0:
                        self.player.score += value.value
                    collision_pos = value.getPosition()
                    temp_effects.append(TempEffect("hit_blue", "effects", collision_pos))

            #Monsters-Shots collision with player
            for monster in self.monsters:
                collided = spritecollide(self.player, monster.shots, True)
                if(len(collided)):
                    self.player.life -= monster.demage
                    collision_pos = self.player.getPosition()
                    temp_effects.append(TempEffect("hit_blue", "effects", collision_pos))

            #Select random enemy to shot and control time between shots
            indexMonShooting = randint(0, len(self.monsters))
            if((framesSinceLastEnemyShot > 30 and len(self.monsters) > 4) or \
            (framesSinceLastEnemyShot > 60)):
                for i, monster in enumerate(self.monsters):
                    if(i == indexMonShooting):
                        monster.shoot()
                        framesSinceLastEnemyShot = 0
            else:
                framesSinceLastEnemyShot += 1

            #Updating and rendering objects

            map = pygame.sprite.RenderUpdates()
            
            self.screen.blit(self.bg, (0, 0))

            map.update()
            map.draw(self.screen)


            self.player.update()
            self.player.update_attack_clock(self.CLOCK)
            if(self.player.life > 0):
                self.player.draw(self.screen)


            for monster in self.monsters:
                monster.update()
                monster.draw(self.screen)

            for i, tmp in enumerate(temp_effects):
                if(tmp.is_dead()):
                    temp_effects.pop(i)
                else:
                    tmp.update_time(self.CLOCK)
                    tmp.draw(self.screen)

            pygame.display.flip()

            if self.player.life <= 0:
                print ("Perdeu! SCORE: " + str(self.player.score))
                self.done = True
            elif len(self.monsters) <= 0:
                self.done = True


            self.CLOCK.tick(self.FPS)
