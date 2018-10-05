import pygame
from pygame.locals import *

class Animation(object):

    def __init__(self, anim):
        self.sprite_sheet = pygame.image.load(".\\Assets\\SpriteSheets\\"+anim+"_SS.png")
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
        if self.tick >= self.fTime:
            self.tick = 0
            self.index += 1
            if self.index >= self.frames:
                self.index = 0

        self.tick += 1

    def draw(self, surface, pos):
        surface.blit(self.get_image(self.index), pos)

def pad0(num):
    n = str(num)
    if len(n) == 1:
        n = "00"+n
    elif len(n) == 2:
        n = "0"+n
    return n

pygame.init()
pygame.display.set_mode((200,200))
variants = ["NF", "NB", "SF", "SB"]
poke = 120
UPDATE = False
v = 0
test = Animation(pad0(poke)+"_"+variants[v])
surface = pygame.display.get_surface()
while True:
    if UPDATE:
        del test
        test = Animation(pad0(poke)+"_"+variants[v])
        UPDATE = False
    del surface
    surface = pygame.display.get_surface()
    test.update()
    surface.fill((255,255,255))
    test.draw(surface, (0,0))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == MOUSEBUTTONUP:
            v += 1
            if v >= len(variants):
                v = 0
            UPDATE = True
        if event.type == KEYDOWN:
            if event.unicode == "w":
                poke += 1
            elif event.unicode == "s":
                poke -= 1
                if poke <= 0:
                    poke = 1
            UPDATE = True