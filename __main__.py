############################
# Finding witch's treasure #
#   By kanditkk and team   #
############################

from game_module import *
import pygame
from pygame import mixer
import random
import time

pygame.init()
mixer.init()
screen.init()

while True: #Always run the loop.
    mixer.music.load('resource/intro.mp3')
    mixer.music.play(-1)
    while not util.checkKeyPress():  # Game Menu
        resources.events = pygame.event.get() #get events for calculate quit and start actions.
        util.checkQuit() #check if quit
        util.checkIpress() #how to play loop
        screen.renderMenuScreen() #blit menu screen
        screen.update() #update pygame screen.
    mixer.music.fadeout(2000)
    mixer.music.load('resource/main.mp3')
    mixer.music.play(-1)
    while score.stage == 1: #stage 1
        resources.events = pygame.event.get() #get events for calculate wasd and quit actions.
        util.checkQuit() #check if quit
        if pygame.time.get_ticks() % 100 and len(enemy.list) < 2 and enemy.spawnCooldown <= 0: enemy.spawn(random.randint(1,3)); enemy.spawnCooldown = 25 #spawn enemies

        enemy.bullet.cycle() #add bullet (x, y) by angle(sin, cos).
        player.bullet.createCycle() #add bullet if spacebar is pressed.
        player.bullet.cycle() #add bullet y by 5 px.

        enemy.cycle() #enemies position calculation
        enemy.despawn() #despawn outside boundaries enemies
        enemy.bullet.despawn() #despawn outside boundaries enemies

        player.cycle() #add player (x, y) change by wasd and calculate boundaries detection.
        player.bullet.hitbox() #player's bullets hitbox calculation
        player.bullet.despawn() #despawn outside boundaries player's bullet

        enemy.star.hitbox() #star's (point's) hitbox detection
        enemy.star.despawn() #despawn the star after some time.

        if score.stage != 6: score.latestStage = score.stage #map design variable.
        if enemy.bullet.hitbox(): score.removeHeart() #if player hit enemies's bullet, then remove 1 heart.
        if score.heart <= 0: score.stage = 6 #if heart under 0 -> set stage to died.

        screen.renderBackground(1) #calculate and blit background to screen.
        screen.renderStar() #blit all stars to screen.
        screen.renderEnemyBullet() #blit all enemy's bullets to screen.
        screen.renderPlayerBullet() #blit all player's bullets to screen.
        screen.renderPlayer() #blit player with (x, y) to screen.
        screen.renderEnemy() #blit enemies to screen.
        screen.renderScore() #blit score text to screen.
        screen.renderHeart() #blit hearts to screen
        screen.update() #update pygame screen.

        score.checkStage() #check stage by score.

        clock.tick(50) #set game ticks.
    if score.stage == 2: #stage 2
        screen.transition() #do transition 1 time.
        score.heart += 1 #add 1 heart.
        player.reset() #reset player pos and changes.
        enemy.reset() #clear enemies.
        enemy.bullet.reset() #clear enemy's bullets.
        enemy.star.reset() #clear enemy's stars.
    while score.stage == 2:
        resources.events = pygame.event.get() #get events for calculate wasd and quit actions.
        util.checkQuit() #check if quit
        if pygame.time.get_ticks() % 100 and len(enemy.list) < 4 and enemy.spawnCooldown <= 0: enemy.spawn(random.randint(1,3)); enemy.spawnCooldown = 25 #spawn enemies.

        enemy.bullet.cycle() #add bullet (x, y) by angle(sin, cos).
        player.bullet.createCycle() #add bullet if spacebar is pressed.
        player.bullet.cycle() #add bullet y by 5 px.

        enemy.cycle() #calculate enemies position.
        enemy.despawn() #despawn outside of the screen enemies.
        enemy.bullet.despawn() #despawn outside of the screen bullets.

        player.cycle() #add player (x, y) change by wasd and do boundaries detection.
        player.bullet.hitbox() #check player's bullet hitboxes.
        player.bullet.despawn() #despawn outside of the screen bullets.

        enemy.star.hitbox() #check stars hiboxes.
        enemy.star.despawn() #despawn outside of the screen stars.
        if enemy.bullet.hitbox(): score.removeHeart() #if player hit by a bullet -> remove 1 heart
        if score.heart <= 0: score.stage = 6 #check for dead.
        screen.renderBackground(2) #calculate and blit background to screen.
        screen.renderStar() #blit all stars to screen.
        screen.renderEnemyBullet() #blit all enemy's bullets to screen.
        screen.renderPlayerBullet() #blit all player's bullets to screen
        screen.renderPlayer() #blit player with (x, y) to screen.
        screen.renderEnemy() #blit all enemies to screen.
        screen.renderScore() #blit score text to screen.
        screen.renderHeart() #blit heart(s) by score.heart
        screen.update() #update pygame screen.

        score.checkStage() #check stage by score.

        clock.tick(50) #set game ticks.
    if score.stage == 3: #boss stage.
        mixer.music.fadeout(1000)
        screen.transition() #do transition 1 time.
        score.heart += 1 #add 1 heart.
        player.reset() #reset player's pos, changes.
        enemy.reset() #reset enemy list.
        enemy.bullet.reset() #reset enemies bullets list.
        enemy.star.reset() #clear all stars
        mixer.music.load('resource/finalcountdown.mp3')
        mixer.music.play(-1,8.0)
    while score.stage == 3: #bossy_oo
        resources.events = pygame.event.get() #get events for calculate wasd and quit actions.
        util.checkQuit() #check if quit

        player.bullet.createCycle() #add bullet if spacebar is pressed.
        player.bullet.cycle() #add bullet y by 5 px.

        player.cycle() #add player (x, y) change by wasd and calculate boundaries detection.
        player.bullet.hitbox() #check player's bullet hitboxes.
        player.bullet.despawn() #despawn outside of the screen bullets.

        boss.bullet.cycle()  #add bullet (x, y) by angle(sin, cos).
        boss.bullet.despawn() #despawn outside of the screen bullets.

        if boss.bullet.hitbox(): score.removeHeart() #if player hit by a bullet -> remove 1 heart

        boss.cycle() #cycle boss path finding.
        boss.hitbox() #check boss hitbox.

        if score.heart <= 0: score.stage = 6 #check for dead.
        if boss.blood <= 0: score.stage = 4 #check if boss died.
        screen.renderBackground(3) #calculate and blit background to screen.
        screen.renderPlayerBullet() #blit all player's bullets to screen
        screen.renderBossBullet() #blit bullets to screen.
        screen.renderPlayer() #blit player with (x, y) to screen.
        screen.renderBoss() #blit boss to screen.
        screen.renderScore() #blit score text to screen.
        screen.renderHeart() #blit hearts to screen.
        screen.renderBossbar() #blit bossbar to screen (greenish bar at the top).
        screen.update() #update pygame screen.
        score.checkStage() #check stage by score.
        clock.tick(50) #set game ticks.
    resources.events = pygame.event.get() #get events for calculate wasd and quit actions.
    if score.stage == 4: #treasure stage.
        mixer.Sound.play(resources.sound.bossdied)
        screen.transition() #do transition 1 time.
        treasure.posx = boss.posx #set treasure pos.
        treasure.posy = boss.posy #set treasure pos.
        player.reset() #reset player's pos, changes.
    while score.stage == 4:
        resources.events = pygame.event.get() #get events for calculate wasd and quit actions.
        util.checkQuit() #check if quit

        player.cycle() #add player (x, y) change by wasd and calculate boundaries detection.
        if treasure.hitbox(): score.stage = 5 #win screen.
        screen.renderBackground(3) #calculate and blit background to screen.
        screen.renderPlayer() #blit player with (x, y) to screen.
        screen.renderTreasure() #blit treasure to screen.
        screen.update() #update pygame screen.
    if score.stage == 5: #win screen.
        resources.events = pygame.event.get() #get events for calculate wasd and quit actions.
        mixer.music.fadeout(1000)
        screen.transition() #do transition 1 time.
        time.sleep(1) #sleep 1 sec.
        mixer.music.load('resource/wearethechampion.mp3')
        mixer.music.play(-1,1)
    while score.stage == 5:
        util.checkQuit() #check if quit
        if util.checkKeyPress(): score.stage = 1 #if key were pressed -> reset all.
        screen.renderWinScreen() #blit win screen
        screen.update() #update pygame screen.
        resources.events = pygame.event.get() #get events for calculate wasd and quit actions.
    if score.stage == 6: #died screen
        screen.selectedMessage = resources.messages.died[random.randint(0,len(resources.messages.died)-1)] #select died messages.
        mixer.Sound.play(resources.sound.death)
        mixer.music.fadeout(1000)
        screen.transition() #do transition 1 time.
        score.update() #write max score to file.
        mixer.music.load('resource/intro.mp3')
        mixer.music.play(-1)
    while score.stage == 6:  # Died
        util.checkQuit() #check if quit
        if util.checkKeyPress(): score.stage = 1 #reset all score, stage.
        resources.events = pygame.event.get() #get events for calculate quit and start actions.
        screen.renderDiedScreen() #blit menu screen
        screen.update() #update pygame screen.

    #reset all.
    mixer.music.fadeout(500)
    score.reset()
    player.reset()
    player.bullet.reset()
    enemy.reset()
    boss.reset()
    boss.bullet.reset()
    enemy.bullet.reset()
    enemy.star.reset()
