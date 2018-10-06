## pokemonEditor.pyw
'''
	File for creating / editing pokemon
'''

from time import time
from random import randrange
from colorsys import hsv_to_rgb
import sys

import pygame
from pygame.locals import *
import pygame.draw as pd

from pokemon import *
from mouse import *
from element import Element

def setIcon(R, G, B):
	icon = pygame.Surface((32, 32))
	icon.fill((R,G,B))
	pygame.display.set_icon(icon)

def blitText(surface, text, pos, color=(0,0,0), textSize=15, font="Arial"):
	surface.blit(pygame.font.SysFont(font, textSize).render(text, True, color), pos)

def keyPressed(key, unicode):
	global tempText, EDITING

	if key == K_BACKSPACE:
		if len(tempText) > 0:
			tempText = tempText[:-1]
	elif unicode.lower() in "abcdefghijklmnopqrstuv[](),.!?{}1234567890 +-=_*/":
		if EDITING != "":
			tempText += unicode
	elif key == K_RETURN:
		if EDITING == "ID":
			try:
				newID = int(tempText)
				workingmon.id = newID
				workingmon.unloadSprites()
			except:
				pass
		elif EDITING == "NAME":
			workingmon.name = tempText.strip(" ")
		elif EDITING == "FORMS":
			try:
				if True:
					workingmon.regular = False
					formlist = tempText.split(",")
					workingmon.unloadSprites()
					if formlist[0] != "":
						workingmon.forms = []
						for i in formlist:
							workingmon.forms.append(i.strip(" ").upper())
			except:
				pass

		elif EDITING == "FSCALE":
			try:
				newfscale = float(tempText)
				workingmon.spriteFScale = newfscale
			except:
				pass
		elif EDITING == "BSCALE":
			try:
				newbscale = float(tempText)
				workingmon.spriteBScale = newbscale
			except:
				pass
		elif EDITING == "HP":
			try:
				workingmon.baseStats["HP"] = int(tempText)
			except:
				pass
		elif EDITING == "SPEED":
			try:
				workingmon.baseStats["SPEED"] = int(tempText)
			except:
				pass
		elif EDITING == "ATTACK":
			try:
				workingmon.baseStats["Attack"]["Physical"] = int(tempText)
			except:
				pass
		elif EDITING == "DEFENSE":
			try:
				workingmon.baseStats["Defense"]["Physical"] = int(tempText)
			except:
				pass
		elif EDITING == "S ATTACK":
			try:
				workingmon.baseStats["Attack"]["Special"] = int(tempText)
			except:
				pass
		elif EDITING == "S DEFENSE":
			try:
				workingmon.baseStats["Defense"]["Special"] = int(tempText)
			except:
				pass
		elif EDITING == "TYPES":
			try:
				workingmon.typing = Element()
				typeAvailable = tempText.split(",")
				for i in typeAvailable:
					workingmon.typing += Element(i.strip(" "))
			except:
				pass
		elif EDITING == "ABILITIES":
			try:
				abil = tempText.split(",")
				workingmon.abilities = []
				for i in abil:
					workingmon.abilities.append(i.strip(" ").lower())
			except:
				pass
		elif EDITING == "EVO COND":
			if True:
				cond = tempText.strip(" ").lower().split(",")
				cmd = cond[0]
				args = [cmd]
				if cmd == "level":
					args.append(int(cond[1])) # level
				elif cmd == "levelwitem":
					args.append(int(cond[1])) # level
					args.append(cond[2]) # itemname
				elif cmd == "levelwhappiness":
					args.append(cond[1]) # happiness
				elif cmd == "levelwarea":
					args.append(cond[1]) # area
				elif cmd == "needitem":
					args.append(cond[1]) # itemname
				elif cmd == "levelwtime":
					args.append(cond[1]) # time
					try:
						args.append(cond[2]) ## item
					except:
						pass
				elif cmd == "levelwgender":
					args.append(int(cond[1])) # level
					args.append(cond[2]) # gender
				elif cmd in ["levelwgender+item","levelwitem+gender"]:
					args = ["levelwgender+item"]
					args.append(int(cond[1])) # level
					args.append(cond[2]) # gender
					args.append(cond[3]) # item
				elif cmd == "levelwparty":
					args.append(int(cond[1])) # level
					args.append(cond[2]) # party member
				elif cmd == "levelwopen":
					args.append(int(cond[1])) # level
					args.append(cond[2]) # new poke
				args.append(cond[-1])

				workingmon.evolution = args

		elif EDITING == "EXP GROUP":
			workingmon.expgroup = tempText[0].strip(' ').upper()+tempText[1:].strip(' ').lower()
		elif EDITING == "EGG GROUP":
			workingmon.eggGroup = tempText[0].strip(' ').upper()+tempText[1:].strip(' ').lower()
		elif EDITING == "EXP DROP":
			try:
				workingmon.expDro = int(tempText)
			except:
				pass
		elif EDITING == "FEMALE RATE":
			try:
				workingmon.femaleRate = float(tempText)
			except:
				pass
		elif EDITING == "SHINY RATE":
			try:
				workingmon.shinyRate = 1/int(tempText)
			except:
				pass
		elif EDITING == "CAPTURE RATE":
			try:
				workingmon.captureRate = int(tempText)
			except:
				pass
		EDITING = ""


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
	Y = 50
	X = 50
	global EDITING, tempText
	for button in range(23):
		if x > X and x < X+15:
			if y > Y and y < Y+15:
				EDITING = ["ID", "NAME", "FORMS?", "FORMS", "FSCALE", "BSCALE", "", "", "", "HP", "SPEED", "ATTACK", "DEFENSE", "S ATTACK", "S DEFENSE", "TYPES", "ABILITIES", "EVOLVES?", 
				"EVO COND", "EXP GROUP", "EXP DROP", "EGG GROUP", "FEMALE RATE", "SHINY RATE", "CAPTURE RATE"][button]
				tempText = ""
				return None
		Y += 20
def mouseMoved(x, y, dy, dx, button):
	pass


def init():
	pass

def run():
	##Running
	global EDITING
	if EDITING == "FORMS?":
		workingmon.regular = not workingmon.regular
		EDITING = ""
		workingmon.forms = []
		workingmon.unloadSprites()
	elif EDITING == "EVOLVES?":
		workingmon.evolves = not workingmon.evolves
		EDITING = ""
		workingmon.evolution = []

def draw(surface):
	surface.fill((255,255,255))
	dw = int(width*(3/5))
	dh = int(height*(1/4))
	bw = int(width*1/4)
	bh = int(height*1/4)
	dex = pygame.Surface((dw,  dh))
	battle1 = pygame.Surface((bw, bh))
	battle2 = pygame.Surface((bw, bh))
	battle1.fill((255,0,255))
	battle2.fill((255,0,255))
	## Draw the workingmon
	if not workingmon.regular:
		workingmon.form = random.choice(workingmon.forms)
	try:
		workingmon.forward = False
		workingmon.draw(battle1, (int(bw/2),int(bh/2)))
		workingmon.forward = True
		workingmon.draw(battle2, (int(bw/2), int(bh/2)))
		setIcon(0,255,0)
	except:
		setIcon(0,0,255)
	## Draw the stat editor
	X = 50
	buttons = [
		"ID: %d" % workingmon.id,
		"Name: %s" % workingmon.name,
		"Has Forms? : %r" % (not workingmon.regular),
		"Forms: {0}".format(workingmon.forms),
		"Sprite Scale (F): %d" % workingmon.spriteFScale,
		"Sprite Scale (B): %d" % workingmon.spriteBScale,
		"$NB$Sprite Offset (F): {0}".format(workingmon.spriteFPosition),
		"$NB$Sprite Offset (B): {0}".format(workingmon.spriteBPosition),
		"$NB$BASE STATS",
		"HP: %d" % workingmon.baseStats["HP"],
		"Speed: %d" % workingmon.baseStats["Speed"],
		"Attack: %d" % workingmon.baseStats["Attack"]["Physical"],
		"Defense: %d" % workingmon.baseStats["Defense"]["Physical"],
		"S Attack: %d" % workingmon.baseStats["Attack"]["Special"],
		"S Defense: %d" % workingmon.baseStats["Defense"]["Special"],
		"Types: {0}".format(workingmon.typing.names),
		"Abilities: {0}".format(workingmon.abilities),
		"Evolves? : %r" % workingmon.evolves,
		"Conditions: {0}".format(workingmon.evolution),
		"Experience Group: %s" % workingmon.expgroup,
		"Experience Drop: %d" % workingmon.expDrop,
		"Egg Group: %s" % workingmon.eggGroup,
		"Female Rate (-1 for genderless): %.2f" % workingmon.femaleRate,
		"Shiny Rate: 1 in %d" % int(workingmon.shinyRate ** -1),
		"Capture Rate: %d" % workingmon.captureRate,
	]
		## Id
	Y = 50
	for button in buttons:
		if button[:4] == "$NB$":
			text = button[4:]
		else:
			text = button
			pd.rect(surface, (120, 120, 120), pygame.Rect(X, Y, 15, 15))
		blitText(surface, text, (X+20, Y))
		Y += 20
	if EDITING != "":
		blitText(surface, "Editing %s: %s" % (EDITING, tempText), (int(width*1/5), 35), textSize=30)
	
		## Sprite Settings (scale, pos)

		## Base stats + stat mods

		## Typing

		## Ability

		## Evolution

		## Exp statistics, egg group

		## Female rate, shinyRate, capture rate


	## Draw dex data

	## Draw the next / previous pokemon in the dex
	surface.blit(dex, (width - dw, height - bh))
	surface.blit(battle1, (0, height - bw))
	surface.blit(battle2, (width - bw, 0))
	return surface


if __name__ == "__main__":
	## Screen Settings
	size = width, height = 800, 800
	pygame.init()
	pygame.display.set_mode(size, RESIZABLE)
	pygame.display.set_caption("Pokemon Editor")
	setIcon(255,0,0)
	
	## Mouse and keyboard settup
	mouse = Mouse()
	mouse.setFunctions(mouseClicked, mouseDragged, mouseMoved, mousePressed, mouseReleased)
	keysDown = dict()
	unicodes = dict()

	## Call the init function
	init()

	dex = Pokedex()
	workingmon = Pokemon()
	workingmon.id = 1
	tempText = ""
	EDITING = ""


	## Framerate / runrate options
	setIcon(0,255,0)
	frameRate = 60
	lFrame = 0
	runRate = 60
	lRun = 0
	## Main loop
	while 1:
		## Run the clock stuff
		if abs(time() - lRun) > 1/runRate:
		## Run the main run loop
			run()
			lRun = time()

		if abs(time() - lFrame) > 1/frameRate:
		## Draw stuff to the screen
			mainSurface = draw(pygame.Surface(size))
			pygame.display.get_surface().blit(mainSurface, (0,0))
			lFrame = time()
		## Update the display
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