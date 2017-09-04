import pygame

def playSoundDeath():
    pygame.mixer.music.stop()
    tempEffect = pygame.mixer.Sound("data/sound/playerDeath.wav")
    tempEffect.set_volume(1)
    tempEffect.play()
    pygame.time.delay(3000)

def playBackgroundMusic():
    pygame.mixer.music.load("data/sound/bgMusic.ogg")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)

def playSoundPlayerShot():
    tempEffect = pygame.mixer.Sound("data/sound/playerShot.wav")
    tempEffect.set_volume(0.5)
    tempEffect.play()

def playSoundClick():
    tempEffect = pygame.mixer.Sound("data/sound/click.wav")
    tempEffect.set_volume(1)
    tempEffect.play()
    pygame.time.delay(750)