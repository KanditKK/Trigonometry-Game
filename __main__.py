from game_module import *
import pygame
import random
import time

crashed = False
pygame.init()
screen.init()

while True:

    while not util.checkKeyPress():  # Game Menu
        resources.events = pygame.event.get() #get events for calculate quit and start actions.
        util.checkQuit() #check if quit

        screen.renderMenuScreen() #blit menu screen
        screen.update() #update pygame screen.
        print([score.stage,enemy.bullet.hitbox()])
    while score.stage == 1:
        resources.events = pygame.event.get() #get events for calculate wasd and quit actions.
        util.checkQuit() #check if quit
        print([score.stage,enemy.bullet.hitbox()])
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

        enemy.star.hitbox()
        enemy.star.despawn()

        if score.stage != 5: score.latestStage = score.stage
        if enemy.bullet.hitbox(): score.stage = 5

        screen.renderBackground(1) #calculate and blit background to screen.
        screen.renderStar()
        screen.renderEnemyBullet() #blit all enemy's bullets to screen.
        screen.renderPlayerBullet() #blit all player's bullets to screen
        screen.renderPlayer() #blit player with (x, y) to screen.
        screen.renderEnemy()
        screen.renderScore()
        screen.update() #update pygame screen.

        score.checkStage() #check stage by score.

        clock.tick(50)
    if score.stage == 2:
        screen.transition()
        player.reset()
        enemy.reset()
        enemy.bullet.reset()
        enemy.star.reset()
        print([score.stage,enemy.bullet.hitbox()])
    while score.stage == 2:
        resources.events = pygame.event.get() #get events for calculate wasd and quit actions.
        util.checkQuit() #check if quit
        print([score.stage,enemy.bullet.hitbox()])
        if pygame.time.get_ticks() % 100 and len(enemy.list) < 4 and enemy.spawnCooldown <= 0: enemy.spawn(random.randint(1,3)); enemy.spawnCooldown = 25

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

        enemy.star.hitbox()
        enemy.star.despawn()
        if enemy.bullet.hitbox(): score.stage = 5
        print([score.stage,enemy.bullet.hitbox()])
        screen.renderBackground(2) #calculate and blit background to screen.
        screen.renderStar()
        screen.renderEnemyBullet() #blit all enemy's bullets to screen.
        screen.renderPlayerBullet() #blit all player's bullets to screen
        screen.renderPlayer() #blit player with (x, y) to screen.
        screen.renderEnemy()
        screen.renderScore()
        screen.update() #update pygame screen.

        score.checkStage() #check stage by score.

        clock.tick(50)
    if score.stage == 5:
        screen.selectedMessage = resources.messages.died[random.randint(0,len(resources.messages.died)-1)]
        screen.transition()
        score.update()
    while score.stage == 5:  # Died
        util.checkQuit() #check if quit
        print([score.stage,enemy.bullet.hitbox()])
        if util.checkKeyPress(): score.stage = 1
        resources.events = pygame.event.get() #get events for calculate quit and start actions.
        screen.renderDiedScreen() #blit menu screen
        screen.update() #update pygame screen.
    score.reset()
    player.reset()
    enemy.reset()
    enemy.bullet.reset()
    enemy.star.reset()
    print([score.stage,enemy.bullet.hitbox()])


