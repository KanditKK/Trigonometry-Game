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
        screen.backgroundY1 += 3
        screen.backgroundY2 += 3
        if screen.backgroundY1 >= screen.panelHeight: screen.backgroundY1 = -(screen.panelHeight * 3)
        if screen.backgroundY2 >= screen.panelHeight: screen.backgroundY2 = -(screen.panelHeight * 3)
        screen.gameDisplay.blit(resources.image.background, (0, screen.backgroundY1))
        screen.gameDisplay.blit(resources.image.background, (0, screen.backgroundY2))

    def renderMenuScreen():
        screen.gameDisplay.fill((200, 200, 200))

    def renderEnemyBullet():
        for data in enemy.bullet.list:
            screen.gameDisplay.blit(resources.image.enemyBullet[data[3]-1], (data[0] + screen.panelxOfset + 7, data[1] + screen.panelyOfset + 7))

    def renderPlayerBullet():
        for data in player.bullet.list:
            screen.gameDisplay.blit(resources.image.playerBullet, (data[0] + screen.panelxOfset, data[1] + screen.panelyOfset))
    def renderPlayer():
        screen.gameDisplay.blit(resources.image.player, (player.posx + screen.panelxOfset, player.posy + screen.panelyOfset))
    def renderEnemy():
        for data in enemy.list:
            if data[2] == 1:
                screen.gameDisplay.blit(resources.image.enemyType1, (data[0] + screen.panelxOfset, data[1] + screen.panelyOfset))
            if data[2] == 2:
                screen.gameDisplay.blit(resources.image.enemyType2, (data[0] + screen.panelxOfset, data[1] + screen.panelyOfset))
            if data[2] == 3:
                screen.gameDisplay.blit(resources.image.enemyType3, (data[0] + screen.panelxOfset, data[1] + screen.panelyOfset))
class player:
    posx = screen.panelWidth // 2
    posy = (screen.panelHeight // 2) + 100
    width = 100
    height = 100
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

        def hitbox():
            for b in range(len(player.bullet.list)):
                for e in range(len(enemy.list)):
                    bulletX = player.bullet.list[b][0]
                    bulletY = player.bullet.list[b][1]
                    enemyX = enemy.list[e][0]
                    enemyY = enemy.list[e][1]

                    if bulletX >= enemyX and bulletX <= enemyX+enemy.width and bulletY >= enemyY and bulletY <= enemyY+enemy.height:
                        player.bullet.list[b][1] = -player.bullet.height-10
                        enemy.list[e][1] = screen.displayHeight
                        score.add(2)

        def despawn():
            newls = []
            for i in range(len(player.bullet.list)):
                if player.bullet.list[i][1] > 0-player.bullet.height: newls.append(player.bullet.list[i])
            player.bullet.list.clear()
            for data in newls:
                player.bullet.list.append(data)
    def reset():
        player.posx = screen.panelWidth // 2
        player.posy = (screen.panelHeight // 2) + 100
        player.xpc = 0
        player.xmc = 0
        player.ypc = 0
        player.ymc = 0
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
                if event.key == pygame.K_g:
                    player.bullet.isShooting = not player.bullet.isShooting
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
    list = []  # [x, y, type, nextXpath, bulletcooldown, shootcooldown]
    width = 50
    height = 50
    spawnCooldown = 25
    #enemy type
    #1 : target locked
    #2 : randomly shoot

    def spawn(type):
        spawnX = (random.randint(0,screen.panelWidth-enemy.width)//2)*2
        spawnY = -enemy.height
        nextXpath = (random.randint(0,(screen.panelWidth-enemy.width)//2))*2
        enemy.list.append([spawnX, spawnY, type, nextXpath, 50, 30])
    def cycle():
        enemy.spawnCooldown -= 1
        for i in range(len(enemy.list)):
            enemy.list[i][1] += 2
            enemy.list[i][4] -= 1
            if enemy.list[i][0] < enemy.list[i][3]: enemy.list[i][0] += 2
            elif enemy.list[i][0] > enemy.list[i][3]: enemy.list[i][0] -= 2
            elif enemy.list[i][0] == enemy.list[i][3]: enemy.list[i][3] = (random.randint(0,(screen.panelWidth-enemy.width)//2))*2
            if enemy.list[i][4] <= 0 :
                if enemy.list[i][2] == 1 and enemy.list[i][5] % 10 == 0:
                    enemy.bullet.create(enemy.list[i][0], enemy.list[i][1], player.posx, player.posy, enemy.list[i][2])
                if enemy.list[i][2] == 2:
                    for n in range(6):
                        enemy.bullet.createWithAngle(enemy.list[i][0]+enemy.width//2, enemy.list[i][1]+enemy.height//2, n*60, enemy.list[i][2])
                    enemy.list[i][5] = 0
                if enemy.list[i][2] == 3:
                    enemy.bullet.createWithAngle(enemy.list[i][0]+enemy.width//2, enemy.list[i][1]+enemy.height//2, 180, enemy.list[i][2])
                    enemy.list[i][4] = 50
                enemy.list[i][5] -= 1
            if enemy.list[i][5] < 0:
                enemy.list[i][4] = 100
                enemy.list[i][5] = 30

    def despawn():
        newls = []
        for i in range(len(enemy.list)):
            if enemy.list[i][1] < screen.panelHeight: newls.append(enemy.list[i])
        enemy.list.clear()
        for data in newls:
            enemy.list.append(data)

    def reset():
        enemy.list = []
        enemy.spawnCooldown = 25

    class bullet:
        list = []  # [x, y, angle_in_degrees, type]
        width = 15
        height = 15
        speed = 5

        def create(enemyX, enemyY, playerX, playerY, type):
            deltaX = enemyX - (playerX + (player.width // 2))
            deltaY = enemyY - (playerY + (player.height // 2))
            angle = int(math.degrees(math.atan2(deltaY, deltaX))) - 180
            enemy.bullet.list.append([enemyX, enemyY, angle, type])

        def createWithAngle(enemyX, enemyY, angle, type):
            enemy.bullet.list.append([enemyX, enemyY, angle, type])

        def cycle():
            for i in range(len(enemy.bullet.list)):
                if enemy.bullet.list[i][3] == 3:
                    enemy.bullet.list[i][1] += 5
                else:
                    angle = enemy.bullet.list[i][2]
                    enemy.bullet.list[i][0] += enemy.bullet.speed * math.cos(math.radians(angle))
                    enemy.bullet.list[i][1] += enemy.bullet.speed * math.sin(math.radians(angle))
        def hitbox():
            isHit = False
            for b in range(len(enemy.bullet.list)):
                bulletX = enemy.bullet.list[b][0]
                bulletY = enemy.bullet.list[b][1]
                playerX = player.posx
                playerY = player.posy

                if bulletX >= playerX and bulletX <= playerX+player.width and bulletY >= playerY and bulletY <= playerY+player.height:
                    enemy.bullet.list[b][1] = -enemy.bullet.height-10
                    isHit = True
            return isHit
        def despawn():
            newls = []
            for i in range(len(enemy.bullet.list)):
                if enemy.bullet.list[i][1] < screen.panelHeight and enemy.bullet.list[i][1] > -enemy.bullet.height: newls.append(enemy.bullet.list[i])
            enemy.bullet.list.clear()
            for data in newls:
                enemy.bullet.list.append(data)
        def reset(): enemy.bullet.list = []
class score:
    Score = 0
    highScore = 0
    heart = 3
    stage = 1
    def add(type):
        if type == 1:
            score.Score += 1
        if type == 2:
            score.Score += 10
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
        enemyBullet = [pygame.image.load('resource/enmBullet1.PNG'), pygame.image.load('resource/enmBullet2.png'), pygame.image.load('resource/enmBullet2.png')]
        playerBullet = pygame.image.load('resource/plyBullet1.png')
        player = pygame.image.load('resource/player.png')
        background = pygame.image.load('resource/background.png')
        enemyType1 = pygame.image.load('resource/enemy1.png')
        enemyType2 = pygame.image.load('resource/enemy2.png')
        enemyType3 = pygame.image.load('resource/enemy3.png')

    class sound:
        pass

    events = pygame.event.get()


clock = pygame.time.Clock()
