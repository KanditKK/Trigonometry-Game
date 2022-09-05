import pygame
import math
import random


class util:
    def checkQuit():
        crashed = False
        for event in resources.events:
            if event.type == pygame.QUIT:
                crashed = True
                pygame.quit()
                quit()
        return crashed

    def checkKeyPress():
        pressed = False
        for event in resources.events:
            if event.type == pygame.KEYDOWN: pressed = True
        return pressed


class screen:
    displayWidth = 1280
    displayHeight = 720
    panelxOfset = 0
    panelyOfset = 0
    panelWidth = displayWidth - (panelxOfset * 2)
    panelHeight = displayHeight - (panelyOfset * 2)

    gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))

    backgroundY1 = -panelHeight
    backgroundY2 = -(panelHeight * 3)
    backgroundY3 = -(panelHeight * 3)

    def init():
        pygame.display.set_caption('Trigonometry Game!')
        screen.gameDisplay.fill((200, 200, 200))

    def update():
        pygame.display.update()

    def renderBackground():
        screen.backgroundY1 += 5
        screen.backgroundY2 += 5
        if screen.backgroundY1 >= screen.panelHeight: screen.backgroundY1 = -(screen.panelHeight * 3)
        if screen.backgroundY2 >= screen.panelHeight: screen.backgroundY2 = -(screen.panelHeight * 3)
        screen.gameDisplay.blit(resources.image.background, (0, screen.backgroundY1))
        screen.gameDisplay.blit(resources.image.background, (0, screen.backgroundY2))

    def renderMenuScreen():
        screen.gameDisplay.fill((200, 200, 200))

    def renderEnemyBullet():
        for data in enemy.bullet.list:
            screen.gameDisplay.blit(resources.image.enemyBullet, (data[0] + screen.panelxOfset + 7, data[1] + screen.panelyOfset + 7))

    def renderPlayerBullet():
        for data in player.bullet.list:
            screen.gameDisplay.blit(resources.image.playerBullet, (data[0] + screen.panelxOfset, data[1] + screen.panelyOfset))
    def renderPlayer():
        screen.gameDisplay.blit(resources.image.player, (player.posx + screen.panelxOfset, player.posy + screen.panelyOfset))


class player:
    posx = screen.panelWidth // 2
    posy = (screen.panelHeight // 2) + 100
    width = 100
    height = 108
    xpc = 0
    xmc = 0
    ypc = 0
    ymc = 0
    class bullet:
        list = []
        width = 10
        height = 15
        isShooting = False
        cooldown = 10
        def createCycle():
            if player.bullet.isShooting == True and player.bullet.cooldown <= 0:
                player.bullet.list.append([player.posx+(player.width//2)-(player.bullet.width//2), player.posy])
                player.bullet.cooldown = 10

        def cycle():
            player.bullet.cooldown -= 1
            for i in range(len(player.bullet.list)):
                player.bullet.list[i][1] -= 15


    def cycle():
        for event in resources.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.xmc = 10
                if event.key == pygame.K_d:
                    player.xpc = 10
                if event.key == pygame.K_w:
                    player.ymc = 10
                if event.key == pygame.K_s:
                    player.ypc = 10
                if event.key == pygame.K_SPACE:
                    player.bullet.isShooting = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.xmc = 0
                if event.key == pygame.K_d:
                    player.xpc = 0
                if event.key == pygame.K_w:
                    player.ymc = 0
                if event.key == pygame.K_s:
                    player.ypc = 0
                if event.key == pygame.K_SPACE:
                    player.bullet.isShooting = False

        # print([player.posx,player.posy,player.xc,player.yc])
        player.posx += (player.xpc - player.xmc)
        player.posy += (player.ypc - player.ymc)
        if player.posx >= screen.panelWidth - player.width: player.posx = screen.panelWidth - player.width
        if player.posy >= screen.panelHeight - player.height: player.posy = screen.panelHeight - player.height
        if player.posx <= 0: player.posx = 0
        if player.posy <= 0: player.posy = 0
class enemy:
    list = []  # [x, y, type]
    class bullet:
        list = []  # [x, y, angle_in_degrees]
        speed = 5

        def create(enemyX, enemyY, playerX, playerY):
            deltaX = enemyX - (playerX + (player.width // 2))
            deltaY = enemyY - (playerY + (player.height // 2))
            angle = int(math.degrees(math.atan2(deltaY, deltaX))) - 180
            enemy.bullet.list.append([enemyX, enemyY, angle])

        def cycle():
            for i in range(len(enemy.bullet.list)):
                angle = enemy.bullet.list[i][2]
                enemy.bullet.list[i][0] += enemy.bullet.speed * math.cos(math.radians(angle))
                enemy.bullet.list[i][1] += enemy.bullet.speed * math.sin(math.radians(angle))

class score:
    Score = 0
    highScore = 0
    heart = 3
    stage = 1
    def add(type):
        if type == 0:
            score.Score += 1
        if type == 1:
            pass
    def removeHeart():
        score.heart -= 1

    def reset():
        score.Score = 0
        score.heart = 3
        score.stage = 1

    def update():
        highscoretxt = open('resource/score.txt', 'r')
        score.highScore = int(str(highscoretxt.readline()))
        highscoretxt.close()
        if score.Score > score.highScore:
            highscoretxt = open('resource/score.txt', 'w')
            highscoretxt.write(str(score))
            highscoretxt.close()
            score.highScore = score.Score

    def checkStage():
        if score.Score >= 1000: score.stage = 2
        if score.Score >= 2000: score.stage = 3

class resources:
    class image:
        enemyBullet = pygame.image.load('resource/enmBullet1.PNG')
        playerBullet = pygame.image.load('resource/plyBullet1.png')
        player = pygame.image.load('resource/battleplane.png')
        background = pygame.image.load('resource/background.png')

    class sound:
        pass

    events = pygame.event.get()


clock = pygame.time.Clock()
