import pygame
from pygame.locals import *
from os import listdir
from os.path import isfile, join
from time import sleep, time

class AnimatedSprite(object):
    def __init__(self, anim):
        self.source = anim
        self.loaded = False
        self.index = 0
        self.ptime = time()
        self.frameRate = 120
        self.runStep = 1
        self.running = True

    def load(self):
        if not self.loaded:
            anim = self.source
            inDir = ".\\Assets\\Animations\\"+anim+"\\"
            self.sprite_sheet = [pygame.image.load(inDir+f) for f in listdir(inDir) if isfile(join(inDir, f))]
            self.fWidth = self.sprite_sheet[0].get_width()
            self.fHeight = self.sprite_sheet[0].get_height()
            self.path = anim
            self.frames = len(self.sprite_sheet)
            self.runTime = self.frames / self.frameRate
            self.loaded = True

    def copy(self):
        new = AnimatedSprite(self.source)
        new.runStep = self.runStep
        new.frameRate = self.frameRate
        return new

    def get_image(self, frame):
        if self.loaded:
            image = pygame.Surface((self.fWidth, self.fHeight))
            image.fill((0,255,0))
            image.blit(self.sprite_sheet[frame], (0, 0))

            image.set_colorkey((0,255,0))

            return image


    def draw(self, surface, pos):
        if self.loaded:
            surface.blit(self.get_image(self.index), pos)
            if self.running:
                if time()-self.ptime > 1/self.frameRate:
                    self.ptime = time()
                    self.index += self.runStep
                    if self.index >= self.frames:
                        self.index = 0
                    if self.index < 0:
                        self.index = self.frames-1
        else:
            self.load()

    def pause(self):
        self.running = False

    def play(self):
        self.running = True

    def reverse(self):
        self.runStep = -abs(self.runStep)

    def forward(self):
        self.runStep = abs(self.runStep)

    def switchDir(self):
        self.runStep *= -1

    def setFrameRate(self, fr):
        self.frameRate = fr
        self.runTime = self.frames / self.frameRate


pygame.init()
pygame.display.set_mode((200,200))
sets = [f for f in listdir(".\\Assets\\Animations\\")]
pokes = []
poke = 0
for p in sets:
    pokes.append(AnimatedSprite(p))
#test = AnimatedSprite("001_NB")
frame = 0
surface = pygame.display.get_surface()
while True:
    frame += 1
    if frame > 120:
        frame = 0
        poke += 1
        if poke >= len(pokes):
            poke = 0
    surface = pygame.display.get_surface()
    surface.fill((255,0,255))
    #test.draw(surface, (0,0))
    pokes[poke].draw(surface, (10,10))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        elif event.type == KEYUP:
            poke += 1
            if poke >= len(pokes):
                poke = 0