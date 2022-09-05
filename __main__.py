from game_module import *
import pygame
import random

crashed = False
pygame.init()
screen.init()

while True:

    while not util.checkKeyPress():  # Game Menu
        resources.events = pygame.event.get() #get events for calculate quit and start actions.
        util.checkQuit() #check if quit

        screen.renderMenuScreen() #blit menu screen
        screen.update() #update pygame screen.

    while score.stage == 1:
        resources.events = pygame.event.get() #get events for calculate wasd and quit actions.
        util.checkQuit() #check if quit

        #enemy.bullet.create(random.randint(0, screen.panelWidth - 10), 0, player.posx, player.posy)

        enemy.bullet.cycle() #add bullet (x, y) by angle(sin, cos).
        player.bullet.createCycle() #add bullet if spacebar is pressed.
        player.bullet.cycle() #add bullet y by 5 px.
        player.cycle() #add player (x, y) change by wasd and calculate boundaries detection.

        screen.renderBackground() #calculate and blit background to screen.
        screen.renderEnemyBullet() #blit all enemy's bullets to screen.
        screen.renderPlayerBullet() #blit all player's bullets to screen
        screen.renderPlayer() #blit player with (x, y) to screen.
        screen.update() #update pygame screen.

        score.add(1) #add score by calculate game ticks.
        score.checkStage() #check stage by score.

        print([len(enemy.bullet.list), player.bullet.isShooting , player.bullet.list ])
        clock.tick(50)

    score.reset()
