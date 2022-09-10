import pygame
import math
import random
import time
pygame.init()

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

    selectedMessage = 'resources.messages.died[random.randint(0,len(resources.messages.died)-1)]'
    def init():
        pygame.display.set_caption('Trigonometry Game!')
        screen.gameDisplay.fill((200, 200, 200))

    def update():
        pygame.display.update()

    def renderBackground(stage):
        screen.backgroundY1 += 3
        screen.backgroundY2 += 3
        if screen.backgroundY1 >= screen.panelHeight: screen.backgroundY1 = -(screen.panelHeight * 3)
        if screen.backgroundY2 >= screen.panelHeight: screen.backgroundY2 = -(screen.panelHeight * 3)
        screen.gameDisplay.blit(resources.image.background[stage-1], (0, screen.backgroundY1))
        screen.gameDisplay.blit(resources.image.background[stage-1], (0, screen.backgroundY2))

    def renderMenuScreen():
        screen.renderBackground(1)
        screen.gameDisplay.blit(resources.image.overlay1,(0,0))
        text = resources.font.big.render('Trigonometry Game!', False, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (screen.panelWidth // 2, screen.panelHeight // 2)
        screen.gameDisplay.blit(text, textRect)

    def renderDiedScreen():
        screen.renderBackground(score.lastestStage)
        screen.renderEnemyBullet() #blit all enemy's bullets to screen.
        screen.renderPlayerBullet() #blit all player's bullets to screen
        screen.renderPlayer() #blit player with (x, y) to screen.
        screen.renderEnemy()
        screen.gameDisplay.blit(resources.image.overlay1,(0,0))
        text = resources.font.big.render('You Died.', False, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (screen.panelWidth // 2, screen.panelHeight // 2)
        screen.gameDisplay.blit(text, textRect)
        text = resources.font.regular.render(screen.selectedMessage, False, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (screen.panelWidth // 2, (screen.panelHeight // 2)+50)
        screen.gameDisplay.blit(text, textRect)
        text = resources.font.small.render('Score: '+str(score.Score), False, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (screen.panelWidth // 2, 30)
        screen.gameDisplay.blit(text, textRect)
        text = resources.font.small.render('Highscore: '+str(score.highScore), False, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (screen.panelWidth // 2, 55)
        screen.gameDisplay.blit(text, textRect)
        if score.Score == score.highScore:
            text = resources.font.regular.render('New Highscore!', False, (255,255,255))
            textRect = text.get_rect()
            textRect.center = (screen.panelWidth // 2, 100)
            screen.gameDisplay.blit(text, textRect)

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
    def renderScore():
        text = resources.font.small.render(str(score.Score), False, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (screen.panelWidth // 2, 50)
        screen.gameDisplay.blit(text, textRect)
    def renderStar():
        for data in enemy.star.list:
            screen.gameDisplay.blit(resources.image.star, (data[0],data[1]))
    def transition():
        for i in range(100):
            resources.events = pygame.event.get() #get events for calculate quit and start actions.
            screen.gameDisplay.blit(resources.image.overlay2, (0,0))
            screen.update()
            time.sleep(0.005)
class player:
    posx = screen.panelWidth // 2
    posy = (screen.panelHeight // 2) + 100
    width = 100
    height = 100
    xpc = 0
    xmc = 0
    ypc = 0
    ymc = 0
    speed = 1
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
                        score.add(1)
                        enemy.star.create(enemyX, enemyY)

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
                if event.key == pygame.K_l:
                    player.speed = 2
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
                if event.key == pygame.K_l:
                    player.speed = 1
                if event.key == pygame.K_SPACE:
                    player.bullet.isShooting = False

        # print([player.posx,player.posy,player.xc,player.yc])
        player.posx += (player.xpc - player.xmc)//player.speed
        player.posy += (player.ypc - player.ymc)//player.speed
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
            for b in range(len(enemy.bullet.list)):
                bulletX = enemy.bullet.list[b][0]
                bulletY = enemy.bullet.list[b][1]
                playerX = player.posx
                playerY = player.posy

                if bulletX >= playerX+28 and bulletX <= playerX+player.width-28 and bulletY >= playerY and bulletY <= playerY+player.height:
                    return True
        def despawn():
            newls = []
            for i in range(len(enemy.bullet.list)):
                if enemy.bullet.list[i][1] < screen.panelHeight and enemy.bullet.list[i][1] > -enemy.bullet.height: newls.append(enemy.bullet.list[i])
            enemy.bullet.list.clear()
            for data in newls:
                enemy.bullet.list.append(data)
        def reset(): enemy.bullet.list = []

    class star:
        list = [] #[x, y, age]
        width = 15
        height = 15
        def create(x,y):
            enemy.star.list.append([x,y,0])
        def hitbox():
            for b in range(len(enemy.star.list)):
                bulletX = enemy.star.list[b][0]
                bulletY = enemy.star.list[b][1]
                playerX = player.posx
                playerY = player.posy
                enemy.star.list[b][2] += 1

                if bulletX >= playerX and bulletX <= playerX+player.width-28 and bulletY >= playerY and bulletY <= playerY+player.height:
                    score.add(2)
                    enemy.star.list[b][1] = screen.displayHeight
        def despawn():
            newls = []
            for i in range(len(enemy.star.list)):
                if enemy.star.list[i][1] < screen.panelHeight and enemy.star.list[i][1] > -enemy.star.height and enemy.star.list[i][2] <= 500: newls.append(enemy.star.list[i])
            enemy.star.list.clear()
            for data in newls:
                enemy.star.list.append(data)
        def reset():
            enemy.star.list.clear()
class score:
    Score = 0
    highScore = 0
    heart = 3
    stage = 1
    lastestStage = 1
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
            highscoretxt.write(str(score.Score))
            highscoretxt.close()
            score.highScore = score.Score

    def checkStage():
        if score.stage != 5:
            if score.stage != 3:
                if score.Score >= 50: score.stage = 2; score.lastestStage = 2
            if score.Score >= 200: score.stage = 3; score.lastestStage = 3

class resources:
    class image:
        enemyBullet = [pygame.image.load('resource/enmBullet1.PNG'), pygame.image.load('resource/enmBullet2.png'), pygame.image.load('resource/enmBullet2.png')]
        playerBullet = pygame.image.load('resource/plyBullet1.png')
        player = pygame.image.load('resource/player.png')
        background = [pygame.image.load('resource/background.png'),pygame.image.load('resource/background2.png')]
        enemyType1 = pygame.image.load('resource/enemy1.png')
        enemyType2 = pygame.image.load('resource/enemy2.png')
        enemyType3 = pygame.image.load('resource/enemy3.png')
        overlay1 = pygame.image.load('resource/blackOverlay.png')
        overlay1.set_alpha(100)
        overlay2 = pygame.image.load('resource/blackOverlay.png')
        overlay2.set_alpha(10)
        star = pygame.image.load('resource/star.png')
    class sound:
        pass
    class font:
        regular = pygame.font.Font('resource/Exo-Regular.otf', 24)
        big = pygame.font.Font('resource/Exo-Regular.otf', 54)
        small = pygame.font.Font('resource/Exo-Regular.otf', 18)
    class messages:
        died = ['Ha Ha Ha, So nooooooooob.', 'Sorry to see you died.', 'Oh, Why are you so noob?', 'Have you done your best?', 'Try Harder!', 'Respect, sir', "Can't you beat Bossy_oo?", 'Noobie.', 'So dump.', 'F']
    events = pygame.event.get()


clock = pygame.time.Clock()
