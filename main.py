import py2app
import mysql.connector
import pygame       #package for games
from pygame import mixer
import os           #package for file interaction

import random
import time


WIDTH, HEIGHT = 900, 500  # this sets constants for the height and width of the game window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
reset = pygame.image.load(os.path.join("assets", "reset.png"))
collect = pygame.image.load(os.path.join("assets", "collect.png"))
lose = pygame.image.load(os.path.join("assets", "lose.png"))
win = pygame.image.load(os.path.join("assets", "win.png"))
resetcorner = pygame.transform.scale(pygame.image.load(os.path.join("assets", "resetcorner.png")), (40, 85))
zap = pygame.transform.scale(pygame.image.load(os.path.join("assets", "zap.png")), (6,6))
scoreLabel = pygame.image.load(os.path.join("assets", "score.png"))
usernameLabel = pygame.transform.scale(pygame.image.load(os.path.join("assets", "username.png")), (610, 350))
leaderboard = pygame.image.load(os.path.join("assets", "leaderboard.png"))
pygame.font.init()
pygame.init()
##mySQL DB
db = mysql.connector.connect(
    host="lokinew.c36z6rrzjsnf.us-east-2.rds.amazonaws.com",
    user = "root",
    passwd = "Sylvie123",
    database = "lokinew"
)
execute = db.cursor()



class User():
    def __init__(self, username, time):
        self.userF = username
        self.bestTime = f"{time}"


def main():

  mainMenu(login())

#########################################################################################

def leaderboards(user):
    rowY = 167
    inc = 0
    userPass = user
    run = True
    clicked = False
    CLOCK = pygame.time.Clock()
    userFont = pygame.font.SysFont("Times New Roman", 23, True, False)
    tempUser = User("null", 0)
    userList = []
    # loading in users to userlist
    execute.execute("SELECT * FROM scores")
    for i in execute:
        x, y = i
        newUser = User(x, y)
        if y > 0:
            userList.append(newUser)

    for i in range(len(userList)):
        for x in range(len(userList)):
            if i == 0:
                if x > 0:
                    if userList[i].bestTime < userList[x].bestTime:
                        tempUser = userList[x]
                        userList[x] = userList[i]
                        userList[i] = tempUser
            else:
                if userList[i].bestTime < userList[x].bestTime:
                    tempUser = userList[x]
                    userList[x] = userList[i]
                    userList[i] = tempUser





    while run:
        mX, mY = pygame.mouse.get_pos()

        #back to main
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True
        if clicked == True and 27 < mX < 90 and 22 < mY < 86:
            run = False
            mainMenu(userPass)







        WIN.blit(leaderboard, (0, 0))
        for i in userList:
            if inc < 6:
                userText = userFont.render(i.userF, True, (250, 235, 40))
                WIN.blit(userText, (213, rowY + (35 * inc)))
                userText = userFont.render(i.bestTime, True, (250, 235, 40))
                WIN.blit(userText, (513, rowY + (34 * inc)))
                inc += 1
            else:
                break
        inc = 0
        pygame.display.update()

##############################################################################################

def mainMenu(user):

    userFont = pygame.font.SysFont("Times New Roman", 23, True, False)
    select = False
    index = 0
    mainList = []
    for i in range(1, 4):
        img = pygame.image.load(os.path.join("assets", f"main{i}.png"))
        mainList.append(img)
    view = mainList[index]
    run = True


    execute.execute(f"SELECT * FROM scores WHERE user = '{user}'")

    for x in execute:
        username, time = x
        break
    else:
        execute.execute(f"insert into scores(user, time) values ('{user}', 0) ")
        db.commit()
        execute.execute(f"SELECT * FROM scores WHERE user = '{user}'")
        for x in execute:
            username, time = x
            break
        print("Created new user")

    timeText = userFont.render(f"{time}", True, (250, 235, 40))




    while run:
        if select:
            if index == 0:
                game(username, time)
                run = False
            if index == 1:
                leaderboards(username)
                run = False


        select = False
        WIN.blit(view, (0,0))
        WIN.blit(pygame.image.load(os.path.join("assets", "bestScore.png")), (0,0))
        WIN.blit(timeText, (205,20))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    index += 1
                    if index > 2:
                        index = 0
                    view = mainList[index]
                if event.key == pygame.K_LEFT:
                    index -= 1
                    if index < 0:
                        index = 2
                    view = mainList[index]

                if event.key == pygame.K_SPACE:
                    select = True

####################################################################################################################################

def login():
    CLOCK = pygame.time.Clock()
    pygame.mixer.init()
    userType = ""
    userFont = pygame.font.SysFont("Times New Roman", 23, True, False)
    run = True
    enter = False
    runcount = 0
    user = ""
    time = 0
    letterList = []
    animationList = []
    index = 0
    for i in range(1, 11):
        img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "intro" , f"intro{i}.jpg")), (910, 500))
        animationList.append(img)
    sound = mixer.Sound(os.path.join("assets", 'LokiMainTheme.wav'))
    sound.play(-1)
    currentTime = pygame.time.get_ticks()



    while user == '':

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    enter = True
                elif event.key == pygame.K_BACKSPACE:
                    userType = userType[0:-1]
                else:
                    if len(userType) < 16:
                        userType += event.unicode


        #loki intro pics
        if index < 1:
            if pygame.time.get_ticks() - currentTime > 20:
                index += 1
                currentTime = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() - currentTime > 500:
                if index > 8:
                    index = 5
                    runcount+=1
                else:
                    index += 1
                currentTime = pygame.time.get_ticks()

        if enter:
            sound.stop()
            user = userType

        userText = userFont.render(userType, True, (40,40,40))

        WIN.blit(animationList[index], (-10, 0))
        WIN.blit(usernameLabel, (119, 155))
        pygame.draw.rect(WIN, (255, 255, 255), (383, 430, 274, 29))
        pygame.draw.rect(WIN, (0,0,0), (384, 431, 271, 27), 1)
        WIN.blit(userText, (389, 431))
        pygame.display.update()

    return user

###########################################################################################

class Loki(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.update_Time = pygame.time.get_ticks()
        self.health = 3
        self.isCollidingR = False
        self.isCollidingL = False
        self.isDead = False
        self.x = 232
        self.y = 351
        walkAnimIndex = 1
        self.position = (self.x, self.y)
        self.index = 0
        self.anim_list = []
        self.img = pygame.image.load(os.path.join("assets", "start", "start1.png"))
        for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,12,13,14,15,16,17, 18, 19]:
            if i < 6:
                img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "start", f"start{i}.png")),(55, 65))
                self.anim_list.append(img)
            if i == 6:
                img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "start", f"start{i}.png")), (67, 103))
                self.anim_list.append(img)
            if i == 7:
                img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "start", f"start{i}.png")), (109, 77))
                self.anim_list.append(img)
            if i == 8:
                img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "start", f"start{i}.png")),(73, 87))
                self.anim_list.append(img)
            if 7 < i < 12:
                img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "start", f"start{i}.png")), (73, 87))
                self.anim_list.append(img)
            if i == 12:
                img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "walk", f"walk{walkAnimIndex}.png")), (73, 87))
                self.anim_list.append(img)
                walkAnimIndex += 1
            if 12 < i < 18:
                img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "walk", f"walk{walkAnimIndex}.png")), (94, 87))
                self.anim_list.append(img)
                walkAnimIndex += 1
            if i == 18:
                img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "jump.png")),(94, 87))
                self.anim_list.append(img)
            if i == 19:
                img = pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join("assets", "jump.png")),(94, 87)), True, False)
                self.anim_list.append(img)
        self.view = self.anim_list[self.index]


#start animation
    def startAnim(self):
        COOLDOWN = 100
        if self.index < 11:
            if pygame.time.get_ticks() - self.update_Time > COOLDOWN:
                self.update_Time = pygame.time.get_ticks()
                self.index += 1
        self.view = self.anim_list[self.index]

#run forward
    def runF(self, tf):
        COOLDOWN = 100
        if self.index < 17:
            if pygame.time.get_ticks() - self.update_Time > COOLDOWN:
                self.update_Time = pygame.time.get_ticks()
                self.index += 1
                if self.index > 16:
                    self.index = 12
        self.view = self.anim_list[self.index]
        if tf == True:
            self.view = self.anim_list[18]

#run back
    def runB(self, tf):
            COOLDOWN = 100

            if self.index < 17:
                if pygame.time.get_ticks() - self.update_Time > COOLDOWN:
                    self.update_Time = pygame.time.get_ticks()
                    self.index += 1
                    if self.index > 16:
                        self.index = 12
            self.view = pygame.transform.flip(self.anim_list[self.index], True, False)

            if tf == True:
                self.view = self.anim_list[19]

#set position
    def setpos(self, x, y):
        self.x = x
        self.y = y
        self.position = (self.x, self.y)

#set view
    def setView(self, index):
        self.index = index
        self.view = self.anim_list[self.index]

class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.update_Time = pygame.time.get_ticks()
        self.isAlive = True
        self.didCollide = False
        self.shootZap = False
        self.x = x
        self.y = y
        self.position = (self.x, self.y)
        self.animIndex = 4
        self.animList = []
        self.seconds = pygame.time.get_ticks()
        self.secondsT = pygame.time.get_ticks()
        self.RL = True
        for i in range(1,5):
            img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "turn", f"turn{i}.png")),(55, 65))
            self.animList.append(img)
        for i in range(1,2):
            img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "idle.png")),(55, 65))
            self.animList.append(img)
        for i in range(1,5):
            img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "turnL", f"turnL{i}.png")),(55, 65)) # L should be R lol
            self.animList.append(img)
        for i in range(1,2):
            img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "left.png")),(55, 65))
            self.animList.append(img)
        self.view = self.animList[self.animIndex]

    def animate(self):
        current = pygame.time.get_ticks()
        if self.RL:
            if self.animIndex > 4:
                self.x += 1
        else:
            if self.animIndex < 4:
                self.x -= 1
        self.position = (self.x, self.y)
        if current - self.seconds > 100:
            if self.RL:
                if self.animIndex < 8:
                    self.animIndex += 1
                else:
                    self.RL = False
            else:
                if self.animIndex > 0:
                    self.animIndex -= 1
                else:
                    self.RL = True
            self.view = self.animList[self.animIndex]
            self.seconds = pygame.time.get_ticks()

    def setView(self, index):
        self.view = self.animList[index]

    def collided(self, x, y):
        if self.x < x < self.x + 55 and self.y < y < self.y + 65:
            self.isAlive = False
            self.didCollide = True

    def zapTime(self):

        if self.shootZap == True:
            self.shootZap = False
        if pygame.time.get_ticks() - self.secondsT > 1400:
            self.shootZap = True
            self.secondsT = pygame.time.get_ticks()

class Bullet():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.view = pygame.transform.scale(pygame.image.load(os.path.join("assets", "green.png")), (11, 11))
        self.BullRect = self.view.get_rect()

class Grounds():
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.position = (self.x, self.y)
        self.view = pygame.transform.scale(pygame.image.load(os.path.join("assets", "blockmid.png")), (self.width, self.height))

class Reset():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.taken = False
        self.view = pygame.transform.scale(reset, (30, 20))

class Zap():
    def __init__(self, x, y, lX, lY):
        self.x = x
        self.y = y
        self.incX = (lX - x)/ 200
        self.incY = (lY - y)/ 200

    def didCollide(self, x, xEnd, y, yEnd):
        self.Cx = x
        self.CxE = xEnd
        self.Cy = y
        self.CyE = yEnd

        if self.Cx < self.x < self.CxE and self.Cy < self.y < self.CyE:
            return True
        else:
            return False

class tempPad():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.view = pygame.transform.scale(pygame.image.load(os.path.join("assets", "tempPad.png")), (35, 35))

class Spike():
    def __init__(self, x, y, num):
        self.width = num * 20
        self.x = x
        self.y = y
        self.num = num
        animList = []
        index = 0
        for i in range (1, 2):
            img = pygame.transform.scale(pygame.image.load(os.path.join("assets", f"spike{i}.png")), (20, 20))
            animList.append(img)
        self.view = animList[index]


def game(username, curr):
    user = username
    currTime = curr
    #constants
    run = True
    FPS = 80
    CLOCK = pygame.time.Clock()
    BG = pygame.image.load(os.path.join("assets", "bg.jpg"))
    loki = Loki()
    enemyList = []
    enemyList.append(Enemy(700, 200))
    enemyList.append(Enemy(1285, 200))
    enemyList[0].setView(4)
    temp = tempPad(1290, 240)

    #variables
    x = 0  # bg x
    Gravity = 0  # this changes to neg when jumping
    tf = False # to set current pygame time once then set to true
    moving_left = False
    moving_right = False
    holdCam = False
    isJumping = False
    shooting = False
    hasReset = False
    action = False
    teleX = 0
    tele = False
    hasTemp = False
    zapList = []
    spikeList = []
    spikeList.append(Spike(812, 385, 27))
    bulletList = []
    BTF = True #bullet true/false: if true then right if false then left
    resetList = []
    resetList.append(Reset(369,184))
    surfaceList = []
    surfaceList.append(Grounds(0, 417,3600, 100))
    surfaceList.append(Grounds(715, 267, 103, 200))
    surfaceList.append(Grounds(850, 200, 108, 20))
    surfaceList.append(Grounds(985, 143, 65, 20))
    surfaceList.append(Grounds(1105, 340, 145, 20))
    surfaceList.append(Grounds(1255, 265, 100, 20))
    surfaceList.append(Grounds(400 , 330, 30, 10))
    surfaceList.append(Grounds(469, 230,30, 10))
    surfaceList.append(Grounds(420, 120,30, 10))
    surfaceList.append(Grounds(370, 200,30, 10))
    Length = len(surfaceList)
    index = 0
    groundX = surfaceList[index].y
    inAir = False
    ground = surfaceList[0]
    resetTime = pygame.time.get_ticks()
    healthDict = {1 : pygame.image.load(os.path.join("assets", "health1.png"))}
    healthDict[2] =  pygame.image.load(os.path.join("assets", "health2.png"))
    healthDict[3] =  pygame.image.load(os.path.join("assets", "health3.png"))
    healthDict[0] = pygame.image.load(os.path.join("assets", "health0.png"))


    checkList = []
#make starting bg and player
    WIN.blit(BG, (x, 0))
    WIN.blit(healthDict[3], (20, 20))
    for i in range(4, Length):
        WIN.blit(surfaceList[i].view, (surfaceList[i].x, surfaceList[i].y))
    WIN.blit(loki.view, loki.position)
    for i in enemyList:
        WIN.blit(i.view, i.position)
    for i in resetList:
        WIN.blit(i.view, (i.x, i.y))
    pygame.display.update()
    toggle = False

#to delay start anim
    while toggle == False:
        startTime = pygame.time.get_ticks()
        if startTime > 1500:
            toggle = True

#beginning animation
    while loki.index < 11:
        loki.startAnim()
        WIN.blit(BG, (x, 0))
        WIN.blit(healthDict[3], (20, 20))
        for i in enemyList:
            WIN.blit(i.view, i.position)
        for i in range(4, Length):
            WIN.blit(surfaceList[i].view, (surfaceList[i].x, surfaceList[i].y))
        for i in resetList:
            WIN.blit(i.view, (i.x, i.y))
        if loki.index < 4:
            loki.setpos(232, 351)
            WIN.blit(loki.view, loki.position)
            pygame.display.update()
        if loki.index == 4:
            loki.setpos(229, 351)
            WIN.blit(loki.view, loki.position)
            pygame.display.update()
        if loki.index == 5:
            loki.setpos(226, 333)
            WIN.blit(loki.view, loki.position)
            pygame.display.update()
        if loki.index == 6:
            loki.setpos(206, 345)
            WIN.blit(loki.view, loki.position)
            pygame.display.update()
        if loki.index > 6:
            loki.x = 222; loki.y = 335
            loki.setpos(loki.x, loki.y)
            WIN.blit(loki.view,loki.position)
            pygame.display.update()


    startTime = pygame.time.get_ticks()
    soundA = mixer.Sound(os.path.join("assets", 'lokiTheme2.wav'))
    soundA.play(-1)

#constantly drawing

    while run:
        # runs at 60 fps
        CLOCK.tick(FPS)
        #if hasn't died or won play game
        if loki.health > 0 and hasTemp == False:

            #SPIKES

            for i in spikeList:
                if loki.y < i.y < loki.y + 85:
                    if loki.x < i.x < loki.x + 60 or i.x < loki.x + 25 < i.x + i.width:
                        loki.health = 0


            # ENEMY

            for i in enemyList:
                i.animate()
                if i.isAlive:
                    if len(bulletList) > 0:
                        i.collided(bulletList[0].x + 5, bulletList[0].y + 5)
                        if i.didCollide:
                            bulletList.pop()
                            for y in range(0, len(enemyList)):
                                if enemyList[y].isAlive == False:
                                    enemyList.pop(y)
                                    break
                            else:
                                print("fuk")
                        i.didCollide = False
                if i.x - loki.x < 500:
                    i.zapTime()
                    if i.shootZap == True:
                        zapList.append(Zap(i.x, i.y + 13, loki.x, loki.y + 35))

            if len(zapList) > 0:
                for i in range(0, len(zapList)):
                    if loki.x + 20 < zapList[i].x < 35 + loki.x and loki.y + 5 < zapList[i].y < loki.y + 65:
                        loki.health -= 1
                        zapList[i].y = 900
                        if loki.health < 1:
                            loki.isDead = True
                    if zapList[i].y < 899:
                        if 1 < zapList[i].x < 899 and 1 < zapList[i].y < 400:
                            zapList[i].x += zapList[i].incX
                            zapList[i].y += zapList[i].incY
                            for p in surfaceList:
                                if p.x < zapList[i].x + 4 < p.x + p.width and p.y < zapList[i].y + 4 < p.y + p.height:
                                    zapList[i].y = 900
                        else:
                            zapList[i].y = 900

            # PLAYER

            # to check if colliding
            for i in surfaceList:
                if i.x < loki.x + 50 < i.x + i.width + 50 and i.y < loki.y + 80 < i.y + i.height:
                    if i.x > loki.x:
                        loki.isCollidingR = True
                        loki.isCollidingL = False
                    if i.x < loki.x:
                        loki.isCollidingL = True
                        loki.isCollidingR = False
                    break
            else:
                loki.isCollidingR = False
                loki.isCollidingL = False

            # moving
            # moves based on the boolean event of keys
            if moving_right:
                if loki.isCollidingR == False:
                    if x > -1 and loki.x < 230:
                        loki.runF(isJumping)
                        if inAir:
                            loki.x += 2
                        else:
                            loki.x += 1
                    else:
                        if holdCam == False and loki.x > 350:
                            if x > -2700:
                                x -= 1
                                for i in resetList:
                                    i.x -= 1
                                for i in zapList:
                                    i.x -= 1
                                for i in surfaceList:
                                    i.x -= 1
                                for i in enemyList:
                                    i.x -= 1
                                for i in spikeList:
                                    i.x -= 1
                                for i in checkList:
                                    i.x -= 1
                                temp.x -= 1
                            if loki.x < 700:
                                loki.x += .2
                                if inAir:
                                    loki.x += .8
                                else:
                                    loki.x += .2
                        else:
                            if loki.x < 790:
                                if inAir:
                                    loki.x += 2
                                else:
                                    loki.x += 1
                        loki.runF(isJumping)

            if moving_left:
                if loki.isCollidingL == False:
                    if x < -1:
                        if holdCam == False:
                            x += 1
                            for i in checkList:
                                i.x += 1
                            for i in resetList:
                                i.x += 1
                            for i in surfaceList:
                                i.x += 1
                            for i in zapList:
                                i.x += 1
                            for i in enemyList:
                                i.x += 1
                            for i in spikeList:
                                i.x += 1
                            temp.x += 1
                            if loki.x > 6:
                                if inAir:
                                    loki.x -= .8
                                else:
                                    loki.x -= .2
                        else:
                            if loki.x > 6:
                                if inAir:
                                    loki.x -= 2
                                else:
                                    loki.x -= 1
                        loki.runB(isJumping)
                    else:
                        if loki.x > -1:
                            loki.runB(isJumping)
                            if inAir:
                                loki.x -= 2
                            else:
                                loki.x -= 1

            # chooses the normal idle if both right nd left keys r pressed
            if moving_left == False and moving_right == False and isJumping == False:
                loki.setView(11)
            if moving_left == True and moving_right == True:
                loki.setView(11)

            # gravity and collision

            # automatically set height increase to 13 but will be changed if under a surface
            if isJumping:
                Gravity = -13

            # to change height of jump if below surface
            for i in surfaceList:
                if (i.x + i.width) > (loki.x + 30) > i.x - 10:
                    if loki.y > i.y - 10:
                        if loki.y < i.y:
                            Gravity = -1 * (loki.y - (i.y))

            isJumping = False

            # Shooting
            # if a bullet has been added to the list
            if len(bulletList) > 0 and shooting == False:
                if BTF == False:
                    bulletList[0].x -= 8
                    if bulletList[0].x < 1:
                        bulletList.pop()
                if BTF == True:
                    bulletList[0].x += 8
                    if bulletList[0].x > 890:
                        bulletList.pop()

            # if the x key event sets its bool to true then a bullet will spawn
            if shooting:
                if moving_left:
                    BTF = False
                    newBull = Bullet(loki.x - 5, loki.y + 30)
                else:
                    BTF = True
                    newBull = Bullet(loki.x + 70, loki.y + 30)
                bulletList.append(newBull)
                shooting = False

            # sets gravity to 7
            if Gravity < 6:
                Gravity += .75

            # enacts gravity
            loki.y += Gravity

            # checks to see if loki is in between and on top of surface
            for i in surfaceList:
                if (i.x + i.width) > (loki.x + 30) > i.x - 15:
                    if loki.y + 72 < i.y:
                        if i.y < groundX:
                            ground = i
            if loki.x + 30 > ground.x + ground.width or loki.x + 30 < ground.x - 10:
                ground = surfaceList[0]

            groundX = ground.y

            # sets the ground that the gravity should be stopped at // lokis extra y space is not accounted for in groundX
            if loki.y + 87 > groundX:
                loki.y = groundX - 81

            # checks in air
            if loki.y < groundX - 82:
                inAir = True
            else:
                inAir = False

            # sets lokis position after all of the delta X,Y

            #if loki.index == 11:
            loki.setpos(loki.x, loki.y)
            #else:
               # loki.setpos(loki.x - 1, loki.y + 3)

            # reset
            if action == True:
                if resetList[0].x < loki.x + 30 < resetList[0].x + 30 and resetList[0].y + 23 > loki.y + 85 > resetList[
                    0].y:
                    if resetList[0].taken == False:
                        hasReset = True
                        resetList[0].taken = True

                if loki.x < temp.x < loki.x + 70 and loki.y < temp.y < loki.y + 100:
                    hasTemp = True


            #constantly updating score time
            timeScore = (pygame.time.get_ticks() - startTime) / 1000
            formattedTimeScore = "{:.2f}".format(timeScore)
            timeFont = pygame.font.SysFont("Times New Roman", 22, True, False)
            timeText = timeFont.render(f"{formattedTimeScore}", True, (0, 0, 0))



            # updates everything
            WIN.blit(BG, (x, 0))
            if resetList[0].x < loki.x + 30 < resetList[0].x + 30 and resetList[0].y + 23 > loki.y + 85 > resetList[
                0].y:
                if resetList[0].taken == False:
                    WIN.blit(collect, (0, 0))
            if loki.x < temp.x < loki.x + 70 and loki.y < temp.y < loki.y + 100:
                WIN.blit(collect, (0, 0))
            if hasReset:
                WIN.blit(resetcorner, (20, 410))
            for i in range(6, Length):
                WIN.blit(surfaceList[i].view, (surfaceList[i].x, surfaceList[i].y))
            for i in enemyList:
                if i.isAlive:
                    WIN.blit(i.view, (i.x, i.y))
            for i in zapList:
                WIN.blit(zap, (i.x, i.y))
            if tele:
                if loki.x + 60 + teleX < 900:
                    for i in surfaceList:
                        if i.x < loki.x + 60 + teleX and i.y < loki.y + 50 < i.y + i.height:
                            teleX = 0
                            teleCol = True
                            break
                    else:
                        teleCol = False
                    if teleCol == False:
                        teleX += 1
                    pygame.draw.line(WIN, (0, 255, 0), (loki.x + 60, loki.y + 50), (loki.x + 60 + teleX, loki.y + 50))
            if len(bulletList) > 0:
                WIN.blit(bulletList[0].view, (bulletList[0].x, bulletList[0].y))
            WIN.blit(loki.view, loki.position)
            for i in resetList:
                if i.taken == False:
                    WIN.blit(i.view, (i.x, i.y))
            for i in spikeList:
                for p in range(0, i.num):
                    WIN.blit(i.view, (i.x + (20 * p), i.y))
            for i in checkList:
                WIN.blit(zap, (i.x, i.y))
            WIN.blit(temp.view, (temp.x, temp.y))
            WIN.blit(healthDict[loki.health], (20, 20))
            WIN.blit(scoreLabel, (730,14))
            if timeScore > 100:
                WIN.blit(timeText, (776, 55))
            elif timeScore > 10:
                WIN.blit(timeText, (782, 55))
            else:
                WIN.blit(timeText, (788, 55))
            pygame.display.update()

        # lose screen
        elif loki.health < 1:
            soundA.stop()
            if tf == False:
                current = pygame.time.get_ticks()
                tf = True
            if pygame.time.get_ticks() - current > 2000:
                run = False
                mainMenu(user)
            else:
                WIN.blit(lose, (0, 0))
                pygame.display.update()


        # win screen
        elif hasTemp == True:
            soundA.stop()


            if tf == False:
                score = (pygame.time.get_ticks() - startTime)/1000
                scorefont = pygame.font.SysFont("Times New Roman", 30, True, False)
                scoreText = scorefont.render(f"{score}", True, (0,0,0))
                if currTime == 0 or score < currTime:
                    execute.execute(f"update scores set time = {score} where user = '{user}'")
                    db.commit()
                current = pygame.time.get_ticks()
                tf = True
            if pygame.time.get_ticks() - current > 3200:
                run = False
                mainMenu(user)
            else:
                WIN.blit(win, (0, 0))
                WIN.blit((pygame.transform.rotate(scoreText, -15)), (730, 98))
                pygame.display.update()


        # Sets key triggers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moving_left = True
                if event.key == pygame.K_RIGHT:
                     moving_right = True
                if event.key == pygame.K_z:
                    holdCam = True
                if event.key == pygame.K_SPACE:
                    if loki.y > groundX - 87:
                        isJumping = True
                if event.key == pygame.K_x:
                    if len(bulletList) < 1:
                        shooting = True
                if event.key == pygame.K_c:
                    action = True
                if event.key == pygame.K_v:
                    if hasReset:
                        tele = True


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    moving_left = False
                if event.key == pygame.K_RIGHT:
                    moving_right = False
                if event.key == pygame.K_z:
                    holdCam = False
                if event.key == pygame.K_SPACE:
                    isJumping = False
                if event.key == pygame.K_c:
                    action = False
                if event.key == pygame.K_v:
                    loki.x += teleX
                    teleX = 0
                    hasReset = False
                    tele = False
                    resetList[0].taken = False

main()







