import pygame, sys, time
import pyganim
from pygame.locals import *
import random
from random import randint
from math import sqrt
from auxil import *
s = Stuff()
pygame.init()

#Global
DisplayWidth = 1000; DisplayHeight = 800
DisplaySurf  = pygame.display.set_mode((DisplayWidth, DisplayHeight), 0, 32)
pygame.display.set_caption('Tanks a Lot')
FPS = 120; FPSClock = pygame.time.Clock() 

createList = 0
unitList = []
enemyList = []
enemyTankList = []
fireBallList = []
explodeList = []

explodeTime = 50
enemyTankRate = 0
OreWidth = 5
OreHeight = 7
coll = .7
halfUnit = 30
destClicked = False
timeCreate = 500
unitCost = 50
flushRate = unitCost / timeCreate
factoryX = 250
factoryY = 250
oreRate = 1




keys = pygame.key.get_pressed()

#Sprites
factoryPic = pygame.image.load('factory.png').convert_alpha()
unitPic = pygame.image.load('unit.png').convert_alpha()
enemyPic = pygame.image.load('enemy.png').convert_alpha()
attackPic = pygame.image.load('attack.png').convert_alpha()
orePic = pygame.image.load('ore.png').convert_alpha()
harvesterPic = pygame.image.load('harvester.png').convert_alpha()
firePic = pygame.image.load('fire.png').convert_alpha()
enemyTankPic = pygame.image.load('enemyTank.png').convert_alpha()

#Animation
animObjx = {}
imagesAndDurationsx = [('%s.%s.png' % ('xplosion/explode',str(num).rjust(3, '0')), 0.05) for num in range(13)]
animObjx['explode'] = pyganim.PygAnimation(imagesAndDurationsx)
moveConductorX = pyganim.PygConductor(animObjx)


class Factory(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = factoryX
        self.y = factoryY
        self.selected = False
        self.rect = pygame.Rect(0, 0, 87, 136)
        self.rect.topleft = (self.x + 73, self.y + 59)
        self.destX = self.x
        self.destY = self.y


class enemyTank(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 1500
        self.y = 500
        self.rect = pygame.Rect(0, 0, 60, 60)
        self.rect.topleft = (self.x + 30, self.y + 30)
        self.health = 70
        self.newDestination = True
        self.canFire = False
        self.destX = 0
        self.destY = 0

        self.fireRate = 70
        self.fireAgain = self.fireRate

    def behavior(self):
        self.rect = pygame.Rect(0, 0, 60, 60)
        self.rect.topleft = (self.x + 30, self.y + 30)
        if self.canFire == False:
            self.fireAgain -= 1
        if self.fireAgain < 0:
            self.canFire = True
            self.fireAgain = self.fireRate
        if (abs(self.x - (self.destX)) < 50) and (abs(self.y - (self.destY) < 50)):
            self.newDestination = True
        if self.newDestination == True:
            self.destX = randint(1000, 1600)
            self.destY = randint(2, 700)
            self.newDestination = False

        if self.x <= self.destX:
            self.x += .5
        else:
            self.x -= .5
        if self.y <= self.destY:
            self.y += .5
        else:
            self.y -= .5


f = Factory()
waypointX = f.x
waypointY = f.y
enemyTankList.append(enemyTank())



class fireBall(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.speed = 3
        self.x = 0
        self.y = 0
        self.destX = 0
        self.destY = 0
        self.calculatedHypotenuse = False
        #self.hypotenuse = sqrt(distX*distX + distY*distY)

    def behavior(self):
        if self.calculatedHypotenuse == False:
            self.distX = abs(self.x - self.destX)
            self.distY = abs(self.y - self.destY)
            self.segmentX = sqrt( abs((self.speed * self.speed) - (self.distX)))
            self.segmentY = sqrt(abs((self.speed * self.speed) - (self.distY)))
            self.calculatedHypotenuse = True
        if self.x <= self.destX:
            self.x += self.segmentX
        else:
            self.x -= self.segmentX
        if self.y <= self.destY:
            self.y += self.segmentY
        else:
            self.y -= self.segmentY


class anyUnit(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.x = f.x + 70
        self.y = f.y + 100
        self.initialDest = True
        self.destX = waypointX
        self.destY = waypointY
        self.initDestX = waypointX
        self.initDestY = waypointY


        self.destClicked = True

        self.rect = pygame.Rect(0, 0, 87, 136)
        self.rect.topleft = (self.x + 73, self.y + 59)
        self.maxHealth = 50
        self.health = self.maxHealth
        self.selected = False


        self.canFire = False
        self.fireRate = 1
        self.fireAgain = self.fireRate

    def behavior(self):

        if self.initialDest >= 0:
            self.destX = self.initDestX


            self.destY = self.initDestY
            self.initialDest -= 1


        self.rect = pygame.Rect(0, 0, 60, 60)
        self.rect.topleft = (self.x + 30, self.y + 30)
        self.healthBar = (float(self.health)/float(self.maxHealth)) * 60
        if self.healthBar > 40:
            self.Color = (0,200,150)
        elif self.healthBar > 20:
            self.Color = (255,255,0)
        else:
            self.Color = (255,50,50)

        if self.canFire == False:
            self.fireAgain -= 1
        if self.fireAgain < 0:
            self.canFire = True
            self.fireAgain = self.fireRate

        if self.destClicked == True:

            if self.x <= self.destX:
                self.x += 1
            else:
                self.x -= 1
            if self.y <= self.destY:
                self.y += 1
            else:
                self.y -= 1

            if self.destClicked == False:
                self.destX = self.x
                self.destY = self.y





class Harvester(anyUnit):
    def __init__(self):
        self.anyUnitPic = harvesterPic
        anyUnit.__init__(self)
        self.oreStored = 0
        self.oreSearch = True
        self.oreFound = False

    def behavior(self):
        if (abs(self.x - (f.x + 150)) < 50) and (abs(self.y - (f.y+120) < 50)):
            global moola
            moola += oreRate
            if self.oreStored <= 0:
                self.oreSearch = True
            else:
                moola += oreRate
                self.oreStored -= oreRate

        if self.oreSearch == True:
            for o in s.oreList:
                if self.oreSearch == True:
                    if (abs(self.x - o.x) < 1000) and (abs(self.y - o.y) < 1000):
                        self.oreSearch = False
                        self.destX = o.x
                        self.destY = o.y
                        self.currentOre = o
                        self.destClicked = True
                        self.oreFound = True

        for o in s.oreList:
            if ((self.destX > o.x) and (self.destX < o.x+60)) and \
            ((self.destY > o.y) and (self.destY < o.y+60)):
                self.oreFound = True
                self.currentOre = o
                self.destX = o.x
                self.destY = o.y

        if self.oreFound == True:
            if (abs(self.x - self.currentOre.x) < 20) and (abs(self.y - self.currentOre.y) < 20):
                self.oreStored += oreRate
                self.currentOre.oreAmount -= oreRate
        if self.oreStored == 800:
            self.destX = f.x+150
            self.destY = f.y+120
            self.oreFound = False

        super(Harvester, self).behavior()


class Unit(anyUnit):
    def __init__(self):
        self.anyUnitPic = unitPic
        anyUnit.__init__(self)



def main():
    global moola
    moola = 500

    POSX = 0
    POSY = 0

    enemyTankRate = 0
    timeCreate = 500
    unitCost = 100
    flushRate = unitCost / timeCreate
    shakeRate = 55

    costCount = 0
    create = False
    createRate = 0
    createProgress = 0
    createList = 0
    createStart = True

    dragged = False
    leftButtonDown = False
    factoryX = 250
    factoryY = 250
    f = Factory()
    waypointX = f.x
    waypointY = f.y

    group1 = []


    unitList.append(Harvester())

    selectInitX, selectInitY, selectFinX, selectFinY = 0,0,0,0


    #Point Within Area Template
    #    px         px         py        py
    #if (( > ) and ( < )) and (( > ) and ( < )):


    while True:

        # Screen Position
        tx, ty = (pygame.mouse.get_pos())
        if tx < 5:
            POSX -= 2
        if tx > DisplayWidth - 5:
            POSX += 2
        if ty < 5:
            POSY -= 2
        if ty > DisplayHeight - 5:
            POSY += 2
        x, y = tx +POSX, ty +POSY


        #Mouse Button Interactions
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                #Left Mouse Button Down
                if event.button == 1:
                    dragged = False
                    selectInitX, selectInitY = x, y
                    selectFinX, selectFinY = x, y
                    leftButtonDown = True
                    for u in unitList:
                        u.selected = False

                #Right Mouse Button Down
                if event.button == 3:
                    if f.selected == True:
                        f.destX = x
                        f.destY = y
                        waypointX = x
                        waypointY = y



                    for u in unitList:
                        if u.selected == True:
                            u.destClicked = True
                            u.destX, u.destY = x, y

                    selectInitX, selectFinX, selectInitY, selectFinY = 0, 0, 0, 0


            #Left Mouse Button Down and Dragged
            elif event.type == pygame.MOUSEMOTION and leftButtonDown:
                selectFinX, selectFinY = x, y
                dragged = True

            #Left Mouse Button Up
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if dragged == False:
                    if ((x > f.x) and (x < f.x+150)) and ((y > f.y) and (y < f.y+150)):
                        f.selected = True
                    else:
                        f.selected = False
                else:
                    f.selected = False



                selectFinX, selectFinY = x - halfUnit, y - halfUnit
                leftButtonDown = False





            #Keyboard Interactions
            if event.type == pygame.KEYDOWN:

                #Assign Groups
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if event.key == K_1:
                        group1 = []
                        for u in unitList:
                            if u.selected == True:
                                group1.append(u)

                if len(group1) > 0:
                    if event.key == K_1:
                        print group1
                        for g1 in group1:
                            g1.selected = True


                if event.key == K_UP:
                    f.y -= 3
                elif event.key == K_DOWN:
                    explodeList.append([]*4)
                    explodeList[-1].extend([randint(0,DisplayWidth)])
                    explodeList[-1].extend([randint(0,DisplayHeight)])
                    explodeList[-1].extend([explodeTime])
                    explodeList[-1].extend([1])

                elif event.key == K_SPACE:
                    enemyList.append(Enemy())
                    createList += 1


                elif event.key == K_s:
                    for u in unitList:
                        if u.selected == True:
                            u.destClicked = False

                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        #Unit Creation Cycle
        if createList > 0 and createStart:
            if moola >= unitCost:
                create = True
                costCount = 0
        if create == True:
            if costCount < unitCost:
                costCount += .5
                createRate += (150.0/200.0)
                if costCount % 1 == 0:
                    moola -= 1
                shakeRate = randint(55,60)
                createStart = False
            else:
                unitList.append(Unit())
                create = False
                createRate = 0
                shakeRate = 55
                createList -=1
                createStart = True


        #Blit Everything
        FPSClock.tick(FPS)
        DisplaySurf.fill((100,200,50))
        DisplaySurf.blit(factoryPic, (f.x -POSX, f.y -POSY))


        for o in s.oreList:
            if o.oreAmount <= 0:
                s.oreList.remove(o)
            DisplaySurf.blit(orePic, (o.x - POSX, o.y - POSY))

        #Unit Interactions
        #h.behavior()
        for u in unitList:
            u.behavior()
            xc = u.x + halfUnit
            yc = u.y + halfUnit

            if u.health <= 0:
                moveConductorX.play()
                explodeList.append([] * 4)
                explodeList[-1].extend([u.x])
                explodeList[-1].extend([u.y])
                explodeList[-1].extend([explodeTime])
                explodeList[-1].extend([1])
                unitList.remove(u)


            if ((xc > selectInitX) and (xc < selectFinX)) and ((yc > selectInitY) and (yc < selectFinY)):
                u.selected = True
            for otherU in unitList:
                #if unitList.index(u) != unitList.index(otherU):
                if u != otherU:
                    if pygame.sprite.collide_rect(u, otherU):
                        if u.x > otherU.x:
                            u.x += coll
                            otherU.x -= coll
                        else:
                            u.x -= coll
                            otherU.x += coll
                        if u.y > otherU.y:
                            u.y += coll
                            otherU.y -= coll
                        else:
                            u.y -= coll
                            otherU.y += coll


            DisplaySurf.blit(u.anyUnitPic, (u.x -POSX, u.y -POSY))
            if u.selected == True:
                pygame.draw.line(DisplaySurf, (255,255,255), (u.x - POSX, u.y - POSY),(u.x + 60 - POSX, u.y - POSY))
                pygame.draw.line(DisplaySurf, (255, 255, 255), (u.x - POSX, u.y-1 - POSY), (u.x + 60 - POSX, u.y-1 - POSY))
                pygame.draw.line(DisplaySurf, (u.Color), (u.x - POSX, u.y+1 - POSY), (u.x + u.healthBar - POSX, u.y+1 - POSY))
                pygame.draw.line(DisplaySurf, (u.Color), (u.x -POSX, u.y -POSY), (u.x + u.healthBar -POSX, u.y -POSY))
            for e in enemyList:
                if pygame.sprite.collide_rect(u, e):
                    enemyList.remove(e)

            for e in enemyTankList:
                if u.canFire == True:
                    if (abs(u.x - e.x) < 300) and (abs(u.y - e.y) < 300):
                        u.canFire = False
                        fireBallList.append(fireBall())
                        fireBallList[-1].x = u.x
                        fireBallList[-1].y = u.y
                        fireBallList[-1].destX = e.x
                        fireBallList[-1].destY = e.y

                if e.canFire == True:
                    if (abs(u.x - e.x) < 500) and (abs(u.y - e.y) < 500):
                        e.canFire = False
                        fireBallList.append(fireBall())
                        fireBallList[-1].x = e.x
                        fireBallList[-1].y = e.y
                        fireBallList[-1].destX = u.x
                        fireBallList[-1].destY = u.y


        #Enemy Interactions
        enemyTankRate += 1
        if enemyTankRate> 800:
            enemyTankList.append(enemyTank())
            enemyTankRate = 0
            DisplaySurf.blit(enemyTankPic, (e.x - POSX, e.y - POSY))


        for e in enemyTankList:
            e.behavior()
            if e.health <= 0:
                explodeList.append([] * 4)
                explodeList[-1].extend([e.x ])
                explodeList[-1].extend([e.y ])
                explodeList[-1].extend([explodeTime])
                explodeList[-1].extend([1])
                enemyTankList.remove(e)
            DisplaySurf.blit(enemyTankPic, (e.x - POSX, e.y - POSY))
            if (x > e.x) and (x< e.x + 60):
                if (y > e.y) and (y < e.y + 60):
                    DisplaySurf.blit(attackPic, (x - 32 -POSX, y - 32 -POSY))



        for e in enemyList:
            e.behavior()
            DisplaySurf.blit(enemyPic, (e.x -POSX, e.y -POSY))
            if (x > e.x) and (x< e.x + 22):
                if (y > e.y) and (y < e.y + 61):
                    DisplaySurf.blit(attackPic, (x - 32 -POSX, y - 32 -POSY))


        for fb in fireBallList:
            fb.behavior()
            if (abs(fb.x - (fb.destX)) < 20) and (abs(fb.y - (fb.destY) < 20)):
                for e in enemyTankList:
                    if (abs(fb.x - e.x) < 100) and (abs(fb.y - e.y) < 100):
                        e.health -= 5
                for u in unitList:
                    if (abs(fb.x - u.x) < 50) and (abs(fb.y - u.y) < 50):
                        u.health -= 5
                fireBallList.remove(fb)
            DisplaySurf.blit(firePic, (fb.x - POSX, fb.y - POSY))


        for exp in explodeList:
            expX =exp[0]
            expY =exp[1]
            exp[2] -= 1
            exp[3] = 1
            if exp[2] <= 0:
                explodeList.remove(exp)
            animObjx['explode'].blit(DisplaySurf, (expX -70 -POSX, expY -70 -POSY))


        #Draw Selection Square
        if leftButtonDown == True:
            pygame.draw.line(DisplaySurf, (255, 255, 255), (selectInitX -POSX, selectInitY -POSY), (selectFinX -POSX, selectInitY -POSY))
            pygame.draw.line(DisplaySurf, (255, 255, 255), (selectInitX -POSX, selectInitY -POSY), (selectInitX -POSX, selectFinY -POSY))
            pygame.draw.line(DisplaySurf, (255, 255, 255), (selectFinX -POSX, selectFinY -POSY), (selectFinX -POSX, selectInitY -POSY))
            pygame.draw.line(DisplaySurf, (255, 255, 255), (selectFinX -POSX, selectFinY -POSY), (selectInitX -POSX, selectFinY -POSY))


        #Draw Money Count
        pygame.draw.rect(DisplaySurf, pygame.Color(0, 100,200),(DisplayWidth - 180, 10, createRate, 60))

        BASICFONT3 = pygame.font.Font('freesansbold.ttf', shakeRate)
        instructionSurf3 = BASICFONT3.render(str(moola), True, (255, 255, 255))
        instructionRect3 = instructionSurf3.get_rect()
        instructionRect3.bottomleft = (DisplayWidth - 170, 70 )
        DisplaySurf.blit(instructionSurf3, instructionRect3)

        if len(enemyTankList) == 0:
            BASICFONT1 = pygame.font.Font('freesansbold.ttf', 200)
            instructionSurf1 = BASICFONT1.render("ween", True, (255, 255, 255))
            instructionRect1 = instructionSurf1.get_rect()
            instructionRect1.bottomleft = (DisplayWidth /4, DisplayHeight/2)
            DisplaySurf.blit(instructionSurf1, instructionRect1)

        if f.selected == True:
            pygame.draw.line(DisplaySurf, (255, 255, 255), (f.x - POSX, f.y - POSY), (f.x + 150 - POSX, f.y  - POSY))

        for u in unitList:
            u.initDestX = waypointX
            u.initDestY = waypointY



        pygame.display.update()


s.oreSplatter()
main()
