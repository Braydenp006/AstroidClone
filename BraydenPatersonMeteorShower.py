#   BRAYDEN PATERSON
#   2022-12-11
#   METEORSHOWER.py
#   this is my program for a astroids like game

import pygame           # tell it to use the pygame library of code
import random           # tell it to use the random generator

pygame.init()           # activate it


# ****** variables ******

current_time = pygame.time.get_ticks()
explosion_group = pygame.sprite.Group()
clock = pygame.time.Clock()

bolCOUNTDOWN = False
bolHEALTHBULLET = False
bolDAMAGEBULLET = False
bolDEAD = False
bolWIN = False
bolPLAY = False
bolSTARTSCREEN = True

win_W,win_H = 800,800
brd_W,brd_H = 800,600
numbMeteors = 9
numbDestroyed = 0
intSCORE = 0
intHIGHSCORE = 0
shipSpeed = 5
inthealthbullet = 1
intdamagebullet = 1
intHEALTH = 3
intcountdown = 0
countdowntimer = 0

X = 400
Y = 400

screen = pygame.display.set_mode((win_W,win_H)) # window
pygame.display.set_caption("METEOR SHOWER")
screen.fill((0,255,0)) # Green

board= pygame.Surface((brd_W, brd_H))
board.fill((0, 0, 255))  # Blue

startboard = pygame.Surface((brd_W,brd_H))

board_score= pygame.Surface((brd_W, 200))
board_score.fill((70,70,70))
font = pygame.font.Font('freesansbold.ttf', 32)
font2 = pygame.font.Font('freesansbold.ttf', 48)
intSHIP = 1
pygame.display.update()

# **** USER EVENTS *****

BIGHIT = pygame.USEREVENT + 3
HIT = pygame.USEREVENT + 1
SHIPHIT = pygame.USEREVENT + 2
HEARTHIT = pygame.USEREVENT + 4
STARHIT = pygame.USEREVENT + 5

# ***** Ship *****
pHAimg = pygame.image.load(f'images\ship{intSHIP}.png').convert_alpha()
pHA = pygame.transform.scale(pHAimg,(80,50))

shipImg = pHA    
particles = []
shipLOC = pygame.Rect(win_W/2-40,500, 20, 50)  #x,y,width,height
X_loc,Y_loc = shipLOC.x,shipLOC.y


# ***** images *****

BigMeteorimg = pygame.image.load('images\BigMeteor.png').convert_alpha()
BigMeteor = pygame.transform.scale(BigMeteorimg,(60,60))
meteorGimg=pygame.image.load('images\pelletG.png').convert_alpha()
starimg = pygame.image.load('images\star.png').convert_alpha()
star = pygame.transform.scale(starimg,(55,55))
meteorG = pygame.transform.scale(meteorGimg,(25,60))
missleEimg = pygame.image.load('images\pelletE.png').convert_alpha()
missleE = pygame.transform.scale(missleEimg,(55,55))
HEALTHimg = pygame.image.load('images\HEALTH.png').convert_alpha()
HEALTH = pygame.transform.scale(HEALTHimg,(50,50))
HEALTHbulletimg = pygame.image.load('images\healthpellet.png').convert_alpha()
HEALTHbullet = pygame.transform.scale(HEALTHbulletimg,(40,40))
HEALTHbulletbig = pygame.transform.scale(HEALTHbulletimg,(60,60))
NUKEbulletimg = pygame.image.load('images\damagepellet.png').convert_alpha()
NUKEbullet = pygame.transform.scale(NUKEbulletimg,(110,110))
SPACEimg = pygame.image.load('images\SpaceBackground.jpg').convert_alpha()
SPACEBackground = pygame.transform.scale(SPACEimg,(brd_W + 200 ,brd_H))
GAMEOVERimg = pygame.image.load('images\GAMEOVER.png').convert_alpha()
GAMEOVER = pygame.transform.scale(GAMEOVERimg,(500,400))
GAMEBOARDERimg = pygame.image.load('images\Boarder.png').convert_alpha()
GAMEBOARDER = pygame.transform.scale(GAMEBOARDERimg,(brd_W + 42 ,205))
SCOREBOARDERimg = pygame.image.load('images\Boarder1.png').convert_alpha()
startbutton = pygame.image.load('images\startbutton.png').convert_alpha()
quitbuttonimg = pygame.image.load('images\quitbutton.png').convert_alpha()
quitbutton = pygame.transform.scale(quitbuttonimg,(320,160))
chestimg = pygame.image.load('images\locker.png')
chest = pygame.transform.scale(chestimg,(150,100))

#***** sounds ******

shoot_sound = pygame.mixer.Sound('Sounds\pew.wav')
meteorexplosion_sound = pygame.mixer.Sound('Sounds\explosion.wav')
shipexplosion_sound = pygame.mixer.Sound('Sounds\dead.wav')
meteorhit_sound = pygame.mixer.Sound('Sounds\meteorhit.wav')
newgame_sound = pygame.mixer.Sound('Sounds\startnewgame.wav')
shipdead_sound = pygame.mixer.Sound('Sounds\superdead.wav')
loadbullet_sound = pygame.mixer.Sound('Sounds\Loadingbullet.wav')
starhit_sound = pygame.mixer.Sound('Sounds\starhit.wav')
hearthit_sound = pygame.mixer.Sound('Sounds\collectheart.wav')

#***** Music *****

Music3 = pygame.mixer.music.load('Sounds\Music3.mp3')

# ************************ Classes ***********************

class cls_Meteor:
    cnt = 1

    def __init__(self,X_loc,Y_loc):

        self.X_loc = X_loc      # object x value
        self.Y_loc = Y_loc      # object y value
            
        self.active = True
        self.heartmeteor = False
        self.meteorImgint = int(random.randint(0,13)) # setting the initail meteor types
        if self.meteorImgint == 2 or self.meteorImgint == 3 or self.meteorImgint == 4 or self.meteorImgint == 5:
            self.meteorImg = BigMeteor
            self.big = True
            self.star = False
            self.health = 3 #setting the meteor health if the meteor is big
        elif self.meteorImgint == 1:
            self.meteorImg = star
            self.star = True
            self.big = False
        else: #setting the meteors that dont have meteorImgint of 1-5 to be normal
            self.meteorImg = meteorG 
            self.big = False
            self.star = False
            # no health since they die in one hit anyways
            
        if self.star == True:
            self.V_speed = int(random.randint(6,12))
        elif self.star == False:
            self.V_speed = int(random.randint(2,8)) # the Y speed of each
        self.pel_rect = (X_loc,Y_loc,20,20) # define the hit box

    def MeteorType():
        #resetting the types of meteors for different uses
        for x in range(numbMeteors):
            #adding more big meteors and stars depending on the score
            if intSCORE <= 200:
                Meteor[x].meteorImgint = int(random.randint(0,13))

            elif intSCORE <= 400:
                Meteor[x].meteorImgint = int(random.randint(0,10))

            elif intSCORE <= 650:
                Meteor[x].meteorImgint = int(random.randint(0,8))

            elif intSCORE <= 900:
                Meteor[x].meteorImgint = int(random.randint(0,6))
            #setting meteor types based off random intergers
            if Meteor[x].meteorImgint == 2 or Meteor[x].meteorImgint == 3 or Meteor[x].meteorImgint == 4 or Meteor[x].meteorImgint == 5:
                Meteor[x].meteorImg = BigMeteor
                Meteor[x].big = True
                Meteor[x].health = 3
                
            elif Meteor[x].meteorImgint == 1:
                Meteor[x].meteorImg = star 
                Meteor[x].big = False
                Meteor[x].star = True
            else:
                Meteor[x].meteorImg = meteorG
                Meteor[x].big = False
                Meteor[x].star = False

class cls_Missle:       # class for missles

    def __init__(self,X_loc,Y_loc):   # will recieve X and Y locations
                                                        # when calling this class

        self.X_loc = X_loc      # missle X value
        self.Y_loc = Y_loc      # missle Y value

        if bolHEALTHBULLET == False and bolDAMAGEBULLET == False:
            self.missleImg = missleE  # what image to use
            
        self.active = False      # set this missle to active

        # the Y speed of this missle fixed as 5
        self.V_speed =  12

        # create an invisble box around this missle
        self.missle_rect = (X_loc,Y_loc,20,20) # define the hit box

    def UpdateMissle(self): #method to update missle to the different abilities
        if bolHEALTHBULLET == False and bolDAMAGEBULLET == False:
            self.missleImg = missleE  # what image to use
        elif bolHEALTHBULLET == True:
            self.missleImg = HEALTHbullet
        elif bolDAMAGEBULLET == True:
            self.missleImg = NUKEbullet
            
class Explosion(pygame.sprite.Sprite):  #class for Explosion
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
        ######### Add these images to the folder
            img = pygame.image.load(f"images\exp{num}.png")
            img = pygame.transform.scale(img, (100, 100))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 4
        #update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        #if the animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

class  cls_Particle(): #class for particles under ship, behind bullets.
    def __init__(self,x, y, x_vel, y_vel, radius, colour, lifetime):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.radius = radius 
        self.colour = colour
        self.lifetime = lifetime #variable to determime when to take the particle off of the screen
        
    def DrawParticles(self,board): #method for drawing the particles with the values provided when creating a instance of the class
        self.lifetime -= 1
        self.x += self.x_vel
        self.y += self.y_vel
        pygame.draw.circle(board, self.colour,(self.x,self.y),self.radius)
    
# ***** FUNCTIONS *****

def draw_window(pacInfo):
    board.blit(SPACEBackground,(0,0))
    
    #**** text variables ****
    
    healthtext = font.render('LIVES', True, (180,0,200), (0,0,0))
    abilitiestext = font.render('ABILITIES (Q,E)', True, (180,0,200), (0,0,0))
    scoretext = font.render('SCORE', True, (180,0,200), (0,0,0))
    scoreNUMtext = font2.render('%d'%intSCORE, True, (180,0,200), (70,70,70))
    highscoretext = font.render('HIGHSCORE: %d'%intHIGHSCORE, True,(180,0,200),(0,0,0))
    losetext = font.render('PRESS "R" TO PLAY AGAIN', True, (255,150,0), (40, 40, 50))
    menutext = font.render('PRESS "F" TO GO TO MENU', True,(255,150,0),(40,40,50))
    counttext = font.render('%s'%intcountdown, True, (255, 150,0), (40, 40, 50))
    GAMEOVERrect = GAMEOVER.get_rect()
    GAMEOVERrect.center = (brd_W/2, brd_H/2  - 40)
    scoretextRect = scoretext.get_rect()
    scoreNUMtextRect = scoreNUMtext.get_rect()
    highscoretextRect = highscoretext.get_rect()
    highscoretextRect.center = (400,40)  
    scoretextRect.center = (117,80)
    scoreNUMtextRect.center = (115, 140)
    counttextRect = counttext.get_rect()
    SCOREBOARDER = pygame.transform.scale(SCOREBOARDERimg,(scoreNUMtextRect.w + 60, scoreNUMtextRect.h + 30))
    SCOREBOARDERRect = SCOREBOARDER.get_rect()
    SCOREBOARDERRect.center = (scoreNUMtextRect.centerx, scoreNUMtextRect.centery - 2)
    counttextRect.center = (100,50)
    board_score.fill((70,70,70))
    board_score.blit(scoretext, scoretextRect)
    board_score.blit(scoreNUMtext,scoreNUMtextRect)
    board_score.blit(highscoretext, highscoretextRect)
    healthtextRect = healthtext.get_rect()
    healthtextRect.center = (675,70)
    abilitiestextRect = abilitiestext.get_rect()
    abilitiestextRect.center = (400, 80)
    losetextrect = losetext.get_rect()
    menutextrect = menutext.get_rect()
    # drawing different text based of different things
    
    if intHEALTH >= 1:
        board_score.blit(HEALTH,(590,90))
    if intHEALTH >= 2:
        board_score.blit(HEALTH,(650, 90))
    if intHEALTH >= 3:
        board_score.blit(HEALTH,(710, 90))
    if intdamagebullet == 1:
        board_score.blit(NUKEbullet,(385, 80))
    if inthealthbullet == 1:
        board_score.blit(HEALTHbulletbig,(320, 105))
    if bolDEAD: 
        board.blit(GAMEOVER,(GAMEOVERrect))
        board.blit(losetext,(win_W/2 - losetextrect.w/2,win_H/2 - losetextrect.h/2 + 60))
        board.blit(menutext,(win_W/2 - menutextrect.w/2,win_H/2 - menutextrect.h + 115))
    if bolCOUNTDOWN:
        board.blit(counttext,(win_W/2 - counttextRect.w/2,win_H/2 - counttextRect.h/2))
        #Adding particles to the board
    particles.append(cls_Particle(shipLOC.x + 40, shipLOC.y + 30, random.randrange(-3,3), random.randrange(4,10), 6, (0,130,200),random.randint(10,30))) #defining the ships particles
    for cls_Particle_ in particles:
        if cls_Particle_.lifetime > 0: #checking to see if the particles lifespan is 
            cls_Particle_.DrawParticles(board) #using the draw method to draw each particle in the list
        else:
            particles.pop(particles.index(cls_Particle_))#getting rid of the particles once lifespan is over
    if miss_Fire.active == True:
        if bolDAMAGEBULLET == False and bolHEALTHBULLET == False:#adding particles to normal bullets
            particles.append(cls_Particle(miss_Fire.X_loc + 27,miss_Fire.Y_loc + 13,(random.randrange(-15,15)/10), random.randrange(4,8),4,(255,255,255),random.randint(5,10)))
        elif bolDAMAGEBULLET == True: # adding different particles to the damage bullet
            particles.append(cls_Particle(miss_Fire.X_loc + 60,miss_Fire.Y_loc + 30,(random.randrange(-19,19)/10), random.randrange(4,6),7,(255,200,0),random.randint(5,15)))
        elif bolHEALTHBULLET == True: # adding different particles to the health bullet
            particles.append(cls_Particle(miss_Fire.X_loc + 23,miss_Fire.Y_loc + 20,(random.randrange(-15,15)/10), random.randrange(4,8),5,(200,0,0),random.randint(5,10)))
        board.blit(miss_Fire.missleImg,(miss_Fire.X_loc, miss_Fire.Y_loc)) #adding the bullet to the screen
    for x in range(numbMeteors):     # loop to draw all the different Meteors
        if Meteor[x].active == True:
            board.blit(Meteor[x].meteorImg, (Meteor[x].X_loc, Meteor[x].Y_loc))
    board_score.blit(GAMEBOARDER,(-17,-5))
    board_score.blit(SCOREBOARDER,(SCOREBOARDERRect))
    board.blit(shipImg, (shipLOC.x, shipLOC.y))    # draw ship on screen
    explosion_group.draw(board)
    explosion_group.update()
    screen.blit(board, (0,0)) # redraw the board to remove old images
    board_score.blit(healthtext, healthtextRect)
    board_score.blit(abilitiestext, abilitiestextRect)
    screen.blit(board_score, (0,  win_H-200))
    
def MeteorReset(indexNumber):
 # send it back to the top
    Meteor[indexNumber].Y_loc = -100
    Meteor[indexNumber].X_loc = random.randrange(0,win_W - 60)
    # give it a new speed
    if intSCORE <= 200:
        if Meteor[indexNumber].star == False:
            Meteor[indexNumber].V_speed = int(random.randint(2,8))
        elif Meteor[indexNumber].star == True:
            Meteor[indexNumber].V_speed = int(random.randint(8,12))
    elif intSCORE <= 400:
        if Meteor[indexNumber].star == False:
            Meteor[indexNumber].V_speed = int(random.randint(4,8))
        elif Meteor[indexNumber].star == True:
            Meteor[indexNumber].V_speed = int(random.randint(10,12))
    elif intSCORE <= 650:
        if Meteor[indexNumber].star == False:
            Meteor[indexNumber].V_speed = int(random.randint(6,10))
        elif Meteor[indexNumber].star == True:
            Meteor[indexNumber].V_speed = int(random.randint(12,14))
    elif intSCORE <= 900:
        if Meteor[indexNumber].star == False:
            Meteor[indexNumber].V_speed = int(random.randint(8,10))
        elif Meteor[indexNumber].star == True:
            Meteor[indexNumber].V_speed = int(random.randint(14,16))
            
def RoundReset():
    global numbDestroyed
    for x in range(numbMeteors):
        Meteor[x].Y_loc = -100
        Meteor[x].active = True
        Meteor[x].heartmeteor = False
        cls_Meteor.MeteorType() # reseting the types of meteors
        # give it a new speed
    if intSCORE <= 200:
        if Meteor[x].star == False:
            Meteor[x].V_speed = int(random.randint(2,8))
        elif Meteor[x].star == True:
            Meteor[x].V_speed = int(random.randint(8,12))
    elif intSCORE <= 400:
        if Meteor[x].star == False:
            Meteor[x].V_speed = int(random.randint(4,8))
        elif Meteor[x].star == True:
            Meteor[x].V_speed = int(random.randint(10,12))
    elif intSCORE <= 650:
        if Meteor[x].star == False:
            Meteor[x].V_speed = int(random.randint(6,10))
        elif Meteor[x].star == True:
            Meteor[x].V_speed = int(random.randint(12,14))
    elif intSCORE <= 900:
        if Meteor[x].star == False:
            Meteor[x].V_speed = int(random.randint(8,10))
        elif Meteor[x].star == True:
            Meteor[x].V_speed = int(random.randint(14,16))
    numbDestroyed = 0
def MeteorMove():
    for x in range(numbMeteors): # cycle through all Meteors moving them down by their speed
        Meteor[x].Y_loc = Meteor[x].Y_loc + Meteor[x].V_speed
        if (Meteor[x].Y_loc > 600): #if off the bottom
            MeteorReset(x)
def MissleMove():       # move each missle up the screen
    # calculate the new Y location as the old + the V_speed
    miss_Fire.Y_loc = miss_Fire.Y_loc - miss_Fire.V_speed

def colideCheck():
    global shipImg, numbDestroyed, bolHEALTHBULLET,bolDAMAGEBULLET, inthealthbullet, intdamagebullet
    ship_rect = shipImg.get_rect(topleft = (shipLOC.x, shipLOC.y))  # hit box for the ship
    miss_rect = miss_Fire.missleImg.get_rect(topleft=(miss_Fire.X_loc, miss_Fire.Y_loc))

    for x in range(numbMeteors):    # cycle though all Meteors checking for collision
        meteorHitbox = Meteor[x].meteorImg.get_rect(topleft = (Meteor[x].X_loc, Meteor[x].Y_loc))
            
        # Meteor collide checking
        if miss_rect.colliderect(meteorHitbox) and miss_Fire.active == True and Meteor[x].active == True:  # check to see if one hitbox touched the other
            if Meteor[x].big == False and Meteor[x].heartmeteor == False and Meteor[x].star == False: 
                if bolHEALTHBULLET == False:
                    pygame.mixer.Sound.play(meteorexplosion_sound)
                    Meteor[x].active = False
                    numbDestroyed = numbDestroyed + 1
                    pygame.event.post(pygame.event.Event(HIT))
                if bolHEALTHBULLET == True:
                    Meteor[x].meteorImg = HEALTH
                    Meteor[x].heartmeteor = True
            elif Meteor[x].big == True: #checking types of meteors since different meteors have different score they give and different health
                pygame.mixer.Sound.play(meteorhit_sound)
                if bolDAMAGEBULLET == True:
                    Meteor[x].health -=3
                elif bolHEALTHBULLET == True:
                    Meteor[x].meteorImg = HEALTH
                    Meteor[x].heartmeteor = True
                    Meteor[x].health = 1
                    Meteor[x].big = False
                elif bolDAMAGEBULLET == False and bolHEALTHBULLET == False:
                    Meteor[x].health -= 1
                if Meteor[x].health <= 0:
                    pygame.mixer.Sound.play(meteorexplosion_sound)
                    Meteor[x].active = False
                    numbDestroyed = numbDestroyed + 1
                    pygame.event.post(pygame.event.Event(BIGHIT))
            elif Meteor[x].star == True:
                    pygame.mixer.Sound.play(starhit_sound)
                    Meteor[x].active = False
                    numbDestroyed = numbDestroyed + 1
                    pygame.event.post(pygame.event.Event(STARHIT))
            elif Meteor[x].heartmeteor == True:
                pygame.mixer.Sound.play(hearthit_sound)
                numbDestroyed = numbDestroyed + 1
                Meteor[x].active = False
                Meteor[x].heartmeteor = False
                pygame.event.post(pygame.event.Event(HEARTHIT))
            bolDAMAGEBULLET = False
            bolHEALTHBULLET = False
            miss_Fire.active = False
            explosion = Explosion(miss_Fire.X_loc, miss_Fire.Y_loc)
            explosion_group.add(explosion)
            if numbDestroyed >= numbMeteors:
                inthealthbullet += 1
                intdamagebullet += 1
                RoundReset()  # reset the Meteor to the top and change type and speed
        
        if ship_rect.colliderect(meteorHitbox) and Meteor[x].active == True: #ship collide checks
            if intHEALTH > 1:
                pygame.mixer.Sound.play(shipexplosion_sound)
            elif intHEALTH == 1:
                pygame.mixer.Sound.play(shipdead_sound)
            explosion = Explosion(Meteor[x].X_loc, Meteor[x].Y_loc)
            explosion_group.add(explosion)
            Meteor[x].active = False
            numbDestroyed = numbDestroyed + 1
            pygame.event.post(pygame.event.Event(SHIPHIT))
            if numbDestroyed >= numbMeteors:
                RoundReset()
                
def Write(): #writing the users highscore into a text file for saving
    filBANK = open("HIGHSCORE.txt","w")
    filBANK.write(str(intHIGHSCORE))
    filBANK.close()
#funtion for reading the text file and adding the highscore
def Read():
    global highscore
    filBANK = open("HIGHSCORE.txt","r")
    for strREAD in filBANK:
        intHIGHSCORE = (int(strREAD))
    filBANK.close()
#funtion to create the text file on the users device if they dont have it already
def Append():
    filBANK = open("HIGHSCORE.txt","a")
    filBANK.close()
    
def ScoreCheck(event): 
    global bolWIN, intSCORE
    if event.type == HIT: #if the player has hit a small astrod, add score
        intSCORE += 10
    elif event.type == BIGHIT: # if the player has killed the large astroids, add more score
        intSCORE += 20
    elif event.type == STARHIT:
     intSCORE += 50
    HighScoreCheck() #check high score
def HighScoreCheck(): #check to see if the players score has beaten the high score
    global intHIGHSCORE
    if intSCORE > intHIGHSCORE:
        intHIGHSCORE = intSCORE
        Write()
def HealthCheck(event): #checking the players health
    global intHEALTH,bolDEAD, bolCOUNTDOWN
    if event.type == HEARTHIT:
        if intHEALTH < 3:
            intHEALTH += 1
    elif event.type == SHIPHIT: #if player is hit subtract health
        intHEALTH -= 1
        shipLOC.x = win_W/2 - shipLOC.w
        shipLOC.y = 500
        RoundReset() # resetting the meteors if player is hit
        if intHEALTH >= 1:
            bolCOUNTDOWN = True #making it count down if the player has another life left
    if intHEALTH <= 0:
        bolDEAD = True #setting dead variable to be true to have other things be possible

def CountDown(): #making the countdown on the screen switch(sorry countdown is bad i couldnt figure out better way)
    global intcountdown, bolCOUNTDOWN, countdowntimer
    
    countdowntimer += 1
    if intcountdown > 0:
        for x in range(numbMeteors):
            Meteor[x].active = False
    clock.tick(3)
    if countdowntimer >= 0 and countdowntimer < 360:
        intcountdown += 1
        print (countdowntimer)
    elif countdowntimer >= 360 and countdowntimer < 720:
        intcountdown = 2
        print (countdowntimer)
    elif countdowntimer >= 720 and countdowntimer < 1080:
        intcountdown = 3
        print (countdowntimer)
    if intcountdown > 3:
        bolCOUNTDOWN = False
        intcountdown = 0
        countdowntimer = 0
    if intcountdown == 0:
        for x in range(numbMeteors):
            Meteor[x].active = True

def StartColideCheck(): #seperate collide function for start screen 
    global bolPLAY, intSHIP,bolSTARTSCREEN
    miss_rect = miss_Fire.missleImg.get_rect(topleft=(miss_Fire.X_loc, miss_Fire.Y_loc))
    startbuttonrect = startbutton.get_rect(topleft = (0,45))
    quitbuttonrect = quitbutton.get_rect(topleft = (420,50))
    chestRect = chest.get_rect(topleft = (325,200))
    if miss_Fire.active == True:
        if miss_rect.colliderect(startbuttonrect):
            bolPLAY = True
            bolSTARTSCREEN = False
        if miss_rect.colliderect(quitbuttonrect):
            bolSTARTSCREEN = False
        if miss_rect.colliderect(chestRect):
            miss_Fire.active = False
            intSHIP += 1 #changing variable within the ship img to change ship
            if intSHIP > 7: #resetting the variable to make it a loop of ships
                intSHIP = 1
            
        
def StartScreen():
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if miss_Fire.active != True: # if there are no active missles
               
                if event.key == pygame.K_SPACE: 
                    miss_Fire.X_loc = shipLOC.x + 15 
                    miss_Fire.Y_loc = shipLOC.y        
                    miss_Fire.active = True
                    cls_Missle.UpdateMissle(miss_Fire)
                    pygame.mixer.Sound.play(shoot_sound)# make the missle active
                    
    keys_pressed = pygame.key.get_pressed()   # check what key was pressed
    if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:           # to go left
        shipLOC.x -= shipSpeed
        if shipLOC.x < 0:
            shipLOC.x = 0

    elif keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:         # to go right
        shipLOC.x += shipSpeed                   # this is the actual move
        if shipLOC.x > brd_W - shipLOC.w - 60:
            shipLOC.x = brd_W - shipLOC.w - 60

    elif keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:       
        shipLOC.y -= shipSpeed
        if shipLOC.y < 300:
            shipLOC.y = 300

    elif keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:      
        shipLOC.y += shipSpeed               
        if shipLOC.y + shipLOC.width > brd_W:
            shipLOC.y = brd_W - shipLOC.width
        if shipLOC.y >= 550:
            shipLOC.y = 550

    if (miss_Fire.Y_loc < 0):
        miss_Fire.active = False
    if miss_Fire.active == True:
        MissleMove()
    DrawStartScreen()
    StartColideCheck()

def DrawStartScreen():
    global shipImg
    pHAimg = pygame.image.load(f'images\ship{intSHIP}.png').convert_alpha()
    pHA = pygame.transform.scale(pHAimg,(80,50))
    shipImg = pHA
    tutorialtext = font.render('WASD TO MOVE, SPACE TO SHOOT', True,(230,180,0),(10,10,10))
    tutorialtext2 = font.render('SHOOT AT OPTION YOU WISH TO CHOOSE',True,(230,180,0),(10,10,10))
    changetext = font.render('CHANGE SHIP', True, (255,150,0), (40, 40, 50))
    tutorialtextRect = tutorialtext.get_rect()
    tutorialtextRect2 = tutorialtext2.get_rect()
    changetextRect = changetext.get_rect()
    changetextRect.center = (brd_W/2,210)
    tutorialtextRect.center = (brd_W/2, 80)
    tutorialtextRect2.center = (brd_W/2, 130)
    board.blit(SPACEBackground,(0,0))
    particles.append(cls_Particle(shipLOC.x + 40, shipLOC.y + 30, random.randrange(-3,3), random.randrange(4,10), 6, (0,130,200),random.randint(10,30))) #defining the ships particles
    for cls_Particle_ in particles:
        if cls_Particle_.lifetime > 0: #checking to see if the particles lifespan is 
            cls_Particle_.DrawParticles(board) #using the draw method to draw each particle in the list
        else:
            particles.pop(particles.index(cls_Particle_))#getting rid of the particles once lifespan is over
    board.blit(shipImg, (shipLOC.x, shipLOC.y))    # draw ship on screen
    if miss_Fire.active == True:
        board.blit(miss_Fire.missleImg,(miss_Fire.X_loc, miss_Fire.Y_loc)) #adding the bullet to the screen
        particles.append(cls_Particle(miss_Fire.X_loc + 27,miss_Fire.Y_loc + 13,(random.randrange(-15,15)/10), random.randrange(4,8),4,(255,255,255),random.randint(5,10)))
    board.blit(startbutton,(35 ,45))
    board.blit(quitbutton,(420 ,50))
    board.blit(chest,(325,220))
    board.blit(changetext,(changetextRect))
    screen.blit(board,(0,0))
    board_score.fill((70,70,70))
    board_score.blit(tutorialtext,(tutorialtextRect))
    board_score.blit(tutorialtext2,(tutorialtextRect2))
    screen.blit(board_score, (0,  win_H-200))
    pygame.display.update()

# ***** BODY *****

pygame.mixer.music.play(-1)
miss_Fire = cls_Missle(shipLOC.x, shipLOC.y)

Append()
Read()
while bolSTARTSCREEN:
    StartScreen()

# create the Meteors instances from the class ****

Meteor = list()                         # name for list that will hold the instances
for x in range(numbMeteors):            # loop for the number of Meteors
    Meteor.append(cls_Meteor(x*90 + 30 ,-100))   # create instances and put them all in a list

# ***** main loop *****

while bolPLAY:     # game play loop
    clock.tick(60)
    for event in pygame.event.get():    # get user input 
        if event.type == pygame.QUIT:   # if it's the X button then quit
            bolPLAY = False                # gets us out of the while loop

# create the instances of missle class
        ScoreCheck(event)
        HealthCheck(event)
        if event.type == pygame.KEYDOWN:
            if bolDEAD == True:
                if event.key == pygame.K_r:
                    pygame.mixer.Sound.play(newgame_sound)
                    bolDEAD = False
                    bolCOUNTDOWN = True
                    inthealthbullet += 1
                    intdamagebullet += 1
                    CountDown()
                    RoundReset()
                    intHEALTH = 3
                    shipLOC.x = win_W/2 - shipLOC.w
                    shipLOC.y = 500
                    intSCORE = 0
                if event.key == pygame.K_f:
                    bolDEAD = False
                    inthealthbullet += 1
                    intdamagebullet += 1
                    RoundReset()
                    intHEALTH = 3
                    intSCORE = 0
                    bolPLAY = False
                    bolSTARTSCREEN = True
                    while bolSTARTSCREEN:
                        StartScreen()
            if miss_Fire.active != True: # if there are no active missles
               
                if event.key == pygame.K_SPACE: 
                    if bolDAMAGEBULLET == True:
                        miss_Fire.X_loc = shipLOC.x - 20
                        miss_Fire.Y_loc = shipLOC.y - 10
                    else:
                        miss_Fire.X_loc = shipLOC.x + 15 
                        miss_Fire.Y_loc = shipLOC.y        
                    miss_Fire.active = True
                    cls_Missle.UpdateMissle(miss_Fire)
                    pygame.mixer.Sound.play(shoot_sound)# make the missle active

                if event.key == pygame.K_q: #turing on the health bullet ability
                    if inthealthbullet >= 1: #checking to make sure ability hasnt already been used that round
                        bolHEALTHBULLET = True
                        bolDAMAGEBULLET = False #setting other abilty to false so that bullet is only one ability
                        inthealthbullet -= 1
                        cls_Missle.UpdateMissle(miss_Fire)#calling the method
                        pygame.mixer.Sound.play(loadbullet_sound)
                if event.key == pygame.K_e: #turning on health bullet abilty
                    if intdamagebullet >= 1:
                        bolDAMAGEBULLET = True
                        bolHEALTHBULLET = False
                        intdamagebullet -= 1 #taking away the ability charge
                        cls_Missle.UpdateMissle(miss_Fire)
                        pygame.mixer.Sound.play(loadbullet_sound)
            #setting the abilitys to have a 1 charge max
            if inthealthbullet > 1:
                inthealthbullet = 1 
            if intdamagebullet > 1:
                intdamagebullet = 1
                
    keys_pressed = pygame.key.get_pressed()   # check what key was pressed
    if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:           # to go left
        shipLOC.x -= shipSpeed
        if shipLOC.x < 0:
            shipLOC.x = 0

    elif keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:         # to go right
        shipLOC.x += shipSpeed                   # this is the actual move
        if shipLOC.x > brd_W - shipLOC.w - 60:
            shipLOC.x = brd_W - shipLOC.w - 60

    elif keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:       
        shipLOC.y -= shipSpeed
        if shipLOC.y < 300:
            shipLOC.y = 300

    elif keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:      
        shipLOC.y += shipSpeed               
        if shipLOC.y + shipLOC.width > brd_W:
            shipLOC.y = brd_W - shipLOC.width
        if shipLOC.y >= 550:
            shipLOC.y = 550

    if (miss_Fire.Y_loc < 0):
        miss_Fire.active = False
    if bolCOUNTDOWN:
        CountDown()
    if bolDEAD: #setting meteors to false if you die
        for x in range(numbMeteors):
            Meteor[x].active = False
    draw_window(shipLOC)
    colideCheck()
    MeteorMove()
    if miss_Fire.active == True:
        MissleMove()
    pygame.time.delay(10)
    pygame.display.flip() #update the display



pygame.quit()

