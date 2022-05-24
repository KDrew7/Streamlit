import pygame, sys, time
import pyganim
from pygame.locals import *
import random
from random import randint

pygame.init()



class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = randint(0, 700)
        self.y = randint(0, 700)
        self.rect = pygame.Rect(0, 0, 22, 61)
        self.rect.topleft = (self.x + 20, self.y + 20)

    def behavior(self):

        self.x += randint(-1, 1)
        self.y += randint(-1, 1)
        self.rect = pygame.Rect(170, 170, 22, 61)
        self.rect.topleft = (self.x+35, self.y+30)


class Ore(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 300
        self.y = 800
        self.oreAmount = 500





class Stuff:
    def __init__(self):
        self.OreWidth = 15
        self.OreHeight = 17
        self.oreList = []

    def oreSplatter(self):
        xc = (self.OreWidth / 2)
        yc = (self.OreHeight / 2)
        for x in range (0,self.OreWidth):
            posX = (300 + (x*60))
            for y in range(0,self.OreHeight):
                place = False
                posY = 700 + (y*60)

                if (abs(x-xc) < xc*(.7)) & (abs(y-yc) < yc*(.7)):
                    place = True
                else:
                    if randint(0,1) == 0:
                        place = True
                if place == True:
                    self.oreList.append(Ore())
                    self.oreList[-1].x = posX
                    self.oreList[-1].y = posY
