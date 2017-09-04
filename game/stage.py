import pygame
from pygame.locals import *
from pygame.sprite import Group, groupcollide, spritecollide

from random import randint

from game.soundplayer import *
from game import *
import json

MAX_STAGE = 10
MONSTERS_SPEED = 2

class Stage:
    def __init__(self, screen, fps = 60, key = 1):
        self.key = key
        self.json_data = None
        self.screen = screen
        self.map = None
        self.temp_effects = []
        self.bg = None
        self.FPS = fps
        self.done = False
        self.CLOCK = pygame.time.Clock()
        
        self.player = None
        self.monsters = Group()

        playBackgroundMusic()
    
    def start(self):

        config = json.loads(open('definitions/stages.json').read())
        config = config['stage' + str(self.key)]

        self.bg = pygame.image.load(config['background']).convert_alpha()
        self.screen.blit(self.bg, (0, 0))

        entities_config = json.loads(open('definitions/entities.json').read())
        conf = entities_config['player']

        self.player = Player('player', tuple(config['player_position']),
        conf['shot'], conf['shot_speed'], conf['life'], conf['demage'])
     
        #botando os monstros a partir do y = 0
        y = 0
        for i in range(1, 5):
            line = config['line' + str(i)]
            x = config['monsters_position'][0]
            y_M = 0
            for c in line:
                conf = entities_config['monster' + c] 
                self.monsters.add(Monster('monster' + c, (x, y), conf['shot'],
                conf['shot_speed'], conf['life'], conf['demage'], conf['value'], MONSTERS_SPEED))
                x += conf['size'][0]
                if conf['size'][1] > y_M:
                    y_M = conf['size'][1]
            y += y_M

        #subindo os monstros para fazer animacao de descida, onde y = altura das 4 linhas
        for monster in self.monsters:
            monster.rect.y -= y

        #descendo eles com velocidade normal para ficarem em sua posicao padrao
        yMovToPos = 0
        while True:
            if yMovToPos < (y + config['monsters_position'][1])/MONSTERS_SPEED:
                for monster in self.monsters:
                    monster.setSpeed((0,1))
                    monster.do()
                yMovToPos += 1
            else:
                break
            self.renderObjects()
            self.CLOCK.tick(self.FPS)

        self.run()

    def run(self):
        framesSinceLastEnemyShot = 0
        lastMove = "right"

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
                if(self.player.attempt_shoot(self.CLOCK)):
                    playSoundPlayerShot()
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
                    if value.life <= 0:
                        self.player.score += value.value
                    collision_pos = value.getPosition()
                    self.temp_effects.append(TempEffect("hit_blue", "effects", collision_pos))

            #Monsters-Shots collision with player
            for monster in self.monsters:
                collided = spritecollide(self.player, monster.shots, True)
                if(len(collided)):
                    self.player.life -= monster.demage
                    collision_pos = self.player.getPosition()
                    self.temp_effects.append(TempEffect("hit_blue", "effects", collision_pos))

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

            if self.player.life <= 0:
                self.done = True

                text = "You lost!  Score: " + str(self.player.score)
                self.showText(text)
                playSoundDeath()
            elif len(self.monsters) <= 0:
                self.done = True

            #Updating and rendering objects
            self.renderObjects()


            self.CLOCK.tick(self.FPS)

        if(len(self.monsters) <= 0):
            if(self.key < MAX_STAGE):
                self.done = False
                self.key += 1
                self.start()
            else:
                text = "You won!  Score: " + str(self.player.score)
                self.showText(text)
                pygame.time.delay(2000)
        

    def showText(self, text):
        font = pygame.font.Font('freesansbold.ttf', 40)
        textSurface = font.render(text, True, (0,0,0))
        dest = textSurface.get_rect()
        dest.center = (320,240)
        self.screen.blit(textSurface, dest)
        pygame.display.flip()

    
    def renderObjects(self):
        self.map = pygame.sprite.RenderUpdates()
        
        self.screen.blit(self.bg, (0, 0))

        self.map.update()
        self.map.draw(self.screen)


        self.player.update()
        self.player.update_attack_clock(self.CLOCK)
        if(self.player.life > 0):
            self.player.draw(self.screen)


        for monster in self.monsters:
            monster.update()
            monster.draw(self.screen)

        for i, tmp in enumerate(self.temp_effects):
            if(tmp.is_dead()):
                self.temp_effects.pop(i)
            else:
                tmp.update_time(self.CLOCK)
                tmp.draw(self.screen)

        pygame.display.flip()
