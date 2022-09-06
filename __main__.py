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

        if pygame.time.get_ticks() % 100 and len(enemy.list) < 2 and enemy.spawnCooldown <= 0: enemy.spawn(random.randint(1,3)); enemy.spawnCooldown = 25

        enemy.bullet.cycle() #add bullet (x, y) by angle(sin, cos).
        player.bullet.createCycle() #add bullet if spacebar is pressed.
        player.bullet.cycle() #add bullet y by 5 px.

        enemy.cycle()
        enemy.despawn()
        #enemy.bullet.hitbox()
        enemy.bullet.despawn()

        player.cycle() #add player (x, y) change by wasd and calculate boundaries detection.
        player.bullet.hitbox()
        player.bullet.despawn()

        if enemy.bullet.hitbox(): score.stage = 3

        screen.renderBackground() #calculate and blit background to screen.
        screen.renderEnemyBullet() #blit all enemy's bullets to screen.
        screen.renderPlayerBullet() #blit all player's bullets to screen
        screen.renderPlayer() #blit player with (x, y) to screen.
        screen.renderEnemy()
        screen.update() #update pygame screen.

        if pygame.time.get_ticks() % 100 == 0: score.add(1) #add score by calculate game ticks.
        score.checkStage() #check stage by score.

        print([score.Score, len(player.bullet.list), len(enemy.bullet.list)])
        clock.tick(50)

    score.reset()
    player.reset()
    enemy.reset()
    enemy.bullet.reset()

