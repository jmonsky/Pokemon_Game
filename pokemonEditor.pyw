import pygame, sys
from pygame.locals import *
from time import time
from mouse import *
from random import randrange
from colorsys import hsv_to_rgb

## DAVID WAS HERE

def setIcon(R, G, B):
	icon = pygame.Surface((32, 32))
	icon.fill((R,G,B))
	pygame.display.set_icon(icon)

def blitText(surface, text, pos, color=(0,0,0), textSize=15, font="Arial"):
	surface.blit(pygame.font.SysFont(font, textSize).render(text, True, color), pos)

def keyPressed(key, unicode):
	print(unicode)
def keyHeld(key, unicode, time):
	pass
def keyReleased(key, unicode, time):
	pass

def mouseClicked(x, y, button):
	pass
def mouseDragged(drag, button):
	pass
def mouseReleased(x, y, button):
	pass
def mousePressed(x, y, button):
	pass
def mouseMoved(x, y, dy, dx, button):
	pass


def init():
	pass

def run():
	##  Running
	pass

def draw(surface):
	## Draw the Dots
	surface.fill((255,255,255))
	blitText(surface, "Hello", (10,10))
	## Draw the obstacles

	## Draw the Overlay

	## Draw the gui
	return surface


if __name__ == "__main__":
	size = width, height = 800, 800
	pygame.init()
	pygame.display.set_mode(size, RESIZABLE)
	pygame.display.set_caption("Smart Dots")
	setIcon(255,0,0)

	mouse = Mouse()
	mouse.setFunctions(mouseClicked, mouseDragged, mouseMoved, mousePressed, mouseReleased)
	keysDown = dict()
	unicodes = dict()

	frameRate = 60
	frameTime = 1/frameRate
	lFrame = 0
	runRate = 60
	runTime = 1/runRate
	lRun = 0
	while 1:
		## Run the clock stuff
		if abs(time() - lRun) > runTime:
			run()
			lRun = time()

		if abs(time() - lFrame) > frameTime:
		## Draw stuff to the screen
			mainSurface = draw(pygame.Surface(size))
			pygame.display.get_surface().blit(mainSurface, (0,0))
			lFrame = time()
		pygame.display.flip()

		## Handle inputs and events
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == VIDEORESIZE:
				width = event.w
				height = event.h
				size = (width, height)
				pygame.display.set_mode((width, height), RESIZABLE)
			if event.type == MOUSEMOTION:
				mouse.move(event.pos[0], event.pos[1])
			if event.type == MOUSEBUTTONDOWN:
				mouse.mouseDown(event.pos[0], event.pos[1], event.button)
			if event.type == MOUSEBUTTONUP:
				mouse.mouseUp(event.pos[0], event.pos[1], event.button)
			if event.type == KEYDOWN:
				if event.key in keysDown.keys():
					if keysDown[event.key] == 0.0:
						keysDown[event.key] = time()
						keyPressed(event.key, event.unicode)
						unicodes[event.key] = event.unicode.lower()
					else:
						keyHeld(event.key, event.unicode, time()-keysDown[event.key])
				else:
					keysDown[event.key] = time()
					keyPressed(event.key, event.unicode)
					unicodes[event.key] = event.unicode.lower()
			if event.type == KEYUP:
				if keysDown[event.key] != 0:
					keyReleased(event.key, unicodes[event.key], time() - keysDown[event.key])
					keysDown[event.key] = 0.0