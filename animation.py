import pygame
from pygame.locals import *
from GIFImage_ext import GIFImage

## TEMPOREY
from os import listdir
from os.path import isfile, join
from time import sleep, time

class Animation(object):

    def __init__(self, anim):
        global deadpokes
        self.anim = anim
        self.loadLater = False
        try:
            self.sprite_sheet = pygame.image.load(".\\Assets\\SpriteSheets\\"+anim+"_SS.png")
        except:
            print("out of memory, will save to load later")
            self.path = anim
            self.loadLater = True
            deadpokes.append(anim[:3])
        else:
            self.fHeight = self.sprite_sheet.get_height()
            with open(".\\Assets\\SpriteSheets\\"+anim+".frames", "r") as frameFile:
                self.frames = int(frameFile.read())
            self.fWidth = self.sprite_sheet.get_width()/self.frames


        self.index = 0
        self.tick = 0
        self.fTime = 250

    def get_image(self, frame):

        image = pygame.Surface((self.fWidth, self.fHeight))
        image.fill((0,255,0))
        image.blit(self.sprite_sheet, (0, 0), (frame*self.fWidth, 0, self.fWidth, self.fHeight))

        image.set_colorkey((0,255,0))

        return image

    def update(self):
        if self.loadLater:
            try:
                self.sprite_sheet = pygame.image.load(".\\Assets\\SpriteSheets\\"+self.anim+"_SS.png")
                self.fHeight = self.sprite_sheet.get_height()
                with open(".\\Assets\\SpriteSheets\\"+self.anim+".frames", "r") as frameFile:
                    self.frames = int(frameFile.read())
                self.fWidth = self.sprite_sheet.get_width()/self.frames
                self.loadLater = False
            except:
                print("DMB", self.anim)
        else:
            if self.tick >= self.fTime:
                self.tick = 0
                self.index += 1
                if self.index >= self.frames:
                    self.index = 0

            self.tick += 1

    def draw(self, surface, pos):
        if not self.loadLater:
            surface.blit(self.get_image(self.index), pos)


pygame.init()
pygame.display.set_mode((200,200))

gifmages = []
gifs = [f for f in listdir(".\\Assets\\GIFS\\") if isfile(join(".\\Assets\\GIFS\\", f))]
for gif in gifs:
    if "NF" in gif and "00" in gif:
        gifmages.append(GIFImage(".\\Assets\\GIFS\\"+gif))

poke = 0
frame = 0
surface = pygame.display.get_surface()
while True:
    surface = pygame.display.get_surface()
    surface.fill((255,255,255))
    gifmages[poke].render(surface, (0,0))
    pygame.display.update()
    frame += 1
    if frame > 10000:
        frame = 0
        poke += 1
        if poke >= len(gifmages):
            poke = 0
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

## ['009', '115', '249', '282', '286', '338', '350', '382', '424', '452', '464', '465', '479', '479', '479', '482', '485', '503', '537', '545', '563', '581', '589', '614', '641', '641', '642', '642', '643', '644', '645', '645', '645', '646', '646']
##are all sprites that overload it