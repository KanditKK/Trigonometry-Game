from game_module import *
import pygame
import random

crashed = False
stageCleared = False
pygame.init()
screen.init()

while True:

    while not util.checkKeyPress():  # Game Menu
        resources.events = pygame.event.get()
        util.checkQuit()

        screen.renderMenuScreen()
        screen.update()

    while not stageCleared:
        resources.events = pygame.event.get()
        util.checkQuit()

        bullet.create(random.randint(0, screen.panelWidth - 10), 0, player.posx, player.posy)

        print([screen.backgroundY1, screen.backgroundY2, len(bullet.list)])

        bullet.cycle()
        player.cycle()

        screen.renderBackground()
        screen.renderBullet()
        screen.renderPlayer()
        screen.update()

        #if pygame.time.get_ticks() >= 10000: stageCleared = True

        clock.tick(50)

    stageCleared = False
