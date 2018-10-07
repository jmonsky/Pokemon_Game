## sprite+animationtesting.py
'''
    Temporary script to lazy load all sprites and animations and sequence through them
'''

import pygame
from pokemon import Pokemon
pokeMANS = []

if True:
    for t in range(1,200):
        test = Pokemon()
        test.id = t
        test.loadSprites()
        pokeMANS.append(test)
if __name__ == "__main__":
    from sprite import *
    from pygame.locals import *
    pygame.init()
    pygame.display.set_mode((200,200))
    sets = [f for f in listdir(".\\Assets\\Animations\\")]
    pokes = []
    poke = 0
    types = []
    for p in sets:
        pokes.append(AnimatedSprite(p))
    sets = [f for f in listdir(".\\Assets\\Sprites\\")]
    for s in sets:
        types.append(Sprite(s[:-4]))
    frame = 0
    t = 0
    surface = pygame.display.get_surface()
    while True:
        frame += 1
        if frame > 120:
            frame = 0
            t += 1
            if t >= len(types):
                t = 0
            poke += 1
            if poke >= len(pokes):
                poke = 0
        surface = pygame.display.get_surface()
        surface.fill((255,0,255))
        types[t].draw(surface, (100, 10))
        pokes[poke].draw(surface, (10,10))
        for POKE in pokeMANS:
            POKE.draw(surface, (0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYUP:
                poke += 1
                if poke >= len(pokes):
                    poke = 0
            elif event.type == MOUSEBUTTONUP:
                for i in pokeMANS:
                    i.forward = not i.forward
                    i.shiny = not i.shiny