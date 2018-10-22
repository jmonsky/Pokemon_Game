## sprite+animationtesting.py
'''
    Temporary script to lazy load all sprites and animations and sequence through them
'''

import pygame
pokeMANS = []

from pokemon import Pokemon

POKEMON = Pokemon()
POKEMON.id = 1

def nextDir(direction):
    return {"up":"down", "down":"left", "left":"right", "right":"up"}[direction]

if __name__ == "__main__":
    from sprite import *
    from pygame.locals import *
    pygame.init()
    pygame.display.set_mode((200,200))
    poke = 0
    pokes = []
    types = []
    sets = range(1, 722)
    for p in sets:
        pokes.append(OverworldSprite(str(p), False))
    sets = [f for f in listdir(".\\Assets\\Sprites\\")]
    for s in sets:
        types.append(Sprite(s[:-4]))
    frame = 0
    t = 0
    surface = pygame.display.get_surface()
    while True:
        frame += 1
        if frame > 1:
            frame = 0
            t += 1
            if t >= len(types):
                t = 0
            poke += 1
            if poke >= len(pokes):
                poke = 0
            POKEMON.id += 1
            if POKEMON.id >= 801:
                POKEMON.id = 1
            POKEMON.unloadSprites()

        surface = pygame.display.get_surface()
        surface.fill((255,0,255))
        #types[t].draw(surface, (100, 10))
        POKEMON.drawOverworld(surface, (50,60))
        POKEMON.drawBattle(surface, (100,120))
        #pokes[poke].draw(surface, (10,10))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYUP:
                poke += 1
                if poke >= len(pokes):
                    poke = 0
                
            elif event.type == MOUSEBUTTONUP:
                POKEMON.overworldDir = nextDir(POKEMON.overworldDir)
                POKEMON.shiny = not POKEMON.shiny
                POKEMON.forward = not POKEMON.forward