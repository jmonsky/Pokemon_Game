## pokemonEditor.pyw
'''
	File for creating / editing pokemon
'''

from time import time
from random import randrange
from colorsys import hsv_to_rgb
import sys

import jsonpickle
import pygame
from pygame.locals import *
import pygame.draw as pd

from pokeName import getPokeFile, getPokeByID
from pokemon import *
from mouse import *
from element import Element

def setIcon(R, G, B):
	icon = pygame.Surface((32, 32))
	icon.fill((R,G,B))
	pygame.display.set_icon(icon)

def blitText(surface, text, pos, color=(0,0,0), textSize=15, font="Arial"):
	surface.blit(pygame.font.SysFont(font, textSize).render(text, True, color), pos)

def saveCurrentPoke():
	global workingmon
	with open(".\\Data\\Pokemon\\"+getPokeFile(workingmon.id)+".pokedata", "w+") as file:
		workingmon.unloadSprites()
		file.write(jsonpickle.encode(workingmon))

def loadAPoke(id):
	global workingmon
	with open(".\\Data\\Pokemon\\"+getPokeFile(id)+".pokedata", "r") as file:
		workingmon = jsonpickle.decode(file.read())
		workingmon.unloadSprites()
	try:
		if workingmon.version == 1:
			## Version is 1 convert to 2
			if len(workingmon.evolution) > 0:
				workingmon.evolution = [workingmon.evolution]
			workingmon.version = 2
			saveCurrentPoke()
		elif workingmon.version == 2:
			workingmon.spriteFPosition = (0,0)
			workingmon.spriteBPosition = (0,0)
			workingmon.spriteFScale = 1
			workingmon.spriteBScale = 1
			workingmon.version = 3
	except:
		## Preversion 1, converting to 1EV_yield
		workingmon.version = 1
		workingmon.EV_yield = baseStatDict(0)
		saveCurrentPoke()


def keyPressed(key, unicode):
	global tempText, EDITING, workingmon
	if key == K_BACKSPACE:
		if len(tempText) > 0:
			tempText = tempText[:-1]
	elif key == K_RIGHT:
		lastID = workingmon.id
		workingmon = Pokemon()
		workingmon.id = lastID+1
		if workingmon.id > 649:
			workingmon.id = 1
		try:
			loadAPoke(workingmon.id)
		except:
			workingmon.name = getPokeByID(workingmon.id)
	elif key == K_LEFT:
		lastID = workingmon.id
		workingmon = Pokemon()
		workingmon.id = lastID-1
		if workingmon.id <= 0:
			workingmon.id = 649
		try:
			loadAPoke(workingmon.id)

		except:
			workingmon.name = getPokeByID(workingmon.id)
	elif key == K_ESCAPE:
		EDITING = ""
	elif unicode.lower() in "abcdefghijklmnopqrstuvwxyz[](),.!?{}:;1234567890 +-=_*/":
		if EDITING != "":
			tempText += unicode
		else:
			if unicode == "S":
				saveCurrentPoke()
			elif unicode == "+":
				workingmon.spriteFScale += 0.05
			elif unicode == "_":
				workingmon.spriteFScale -= 0.05
			elif unicode == "=":
				workingmon.spriteBScale += 0.05
			elif unicode == "-":
				workingmon.spriteBScale -= 0.05
			elif unicode == "1":
				workingmon.spriteFPosition = (workingmon.spriteFPosition[0]-1, workingmon.spriteFPosition[1])
			elif unicode == "3":
				workingmon.spriteFPosition = (workingmon.spriteFPosition[0]+1, workingmon.spriteFPosition[1])
			elif unicode == "2":
				workingmon.spriteFPosition = (workingmon.spriteFPosition[0], workingmon.spriteFPosition[1]+1)
			elif unicode == "5":
				workingmon.spriteFPosition = (workingmon.spriteFPosition[0], workingmon.spriteFPosition[1]-1)
			elif unicode == "j":
				workingmon.spriteBPosition = (workingmon.spriteBPosition[0]-1, workingmon.spriteBPosition[1])
			elif unicode == "l":
				workingmon.spriteBPosition = (workingmon.spriteBPosition[0]+1, workingmon.spriteBPosition[1])
			elif unicode == "k":
				workingmon.spriteBPosition = (workingmon.spriteBPosition[0], workingmon.spriteBPosition[1]+1)
			elif unicode == "i":
				workingmon.spriteBPosition = (workingmon.spriteBPosition[0], workingmon.spriteBPosition[1]-1)
	elif key == K_RETURN or key == 271:
		if EDITING == "ID":
			try:
				newID = int(tempText)
				try:
					loadAPoke(newID)
				except:
					workingmon = Pokemon()
					workingmon.id = newID
					workingmon.unloadSprites()
					workingmon.name = getPokeByID(workingmon.id)
			except:
				pass
		elif EDITING == "FORMS":
			formlist = tempText.split(",")
			workingmon.unloadSprites()
			if formlist[0] != "":
				workingmon.forms = []
				for i in formlist:
					workingmon.forms.append(i.upper())

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
		if EDITING in ["HP", "SPEED", "ATTACK", "DEFENSE", "S ATTACK", "S DEFENSE"]:
			temp = tempText.split(",")
			temp2 = tempText.split(":")
			bstat = temp[0]
			statMod = 1
			evyield = 0
			if len(temp) > 1 and len(temp2) > 1:
				temp3 = temp[1].split(":")
				statMod = temp3[0]
				evyield = temp2[1]
			elif len(temp) > 1:
				evyield = temp[1]
			elif len(temp2) > 1:
				statMod = temp2[1]

		if EDITING == "HP":
			try:
				workingmon.baseStats["HP"] = int(bstat)
				workingmon.EV_yield["HP"] = int(evyield)
				workingmon.statMod["HP"] = int(statMod)
			except:
				pass
		elif EDITING == "SPEED":
			try:
				workingmon.baseStats["Speed"] = int(bstat)
				workingmon.EV_yield["Speed"] = int(evyield)
				workingmon.statMod["Speed"] = int(statMod)
			except:
				pass
		elif EDITING == "ATTACK":
			try:
				workingmon.baseStats["Attack"]["Physical"] = int(bstat)
				workingmon.EV_yield["Attack"]["Physical"] = int(evyield)
				workingmon.statMod["Attack"]["Physical"] = int(statMod)
			except:
				pass
		elif EDITING == "DEFENSE":
			try:
				workingmon.baseStats["Defense"]["Physical"] = int(bstat)
				workingmon.EV_yield["Defense"]["Physical"] = int(evyield)
				workingmon.statMod["Defense"]["Physical"] = int(statMod)
			except:
				pass
		elif EDITING == "S ATTACK":
			try:
				workingmon.baseStats["Attack"]["Special"] = int(bstat)
				workingmon.EV_yield["Attack"]["Special"] = int(evyield)
				workingmon.statMod["Attack"]["Special"] = int(statMod)
			except:
				pass
		elif EDITING == "S DEFENSE":
			try:
				workingmon.baseStats["Defense"]["Special"] = int(bstat)
				workingmon.EV_yield["Defense"]["Special"] = int(evyield)
				workingmon.statMod["Defense"]["Special"] = int(statMod)
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
						args.append(int(cond[2])) ## happiness
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
				elif cmd == "levelwstatdiff":
					args.append(int(cond[1])) # level
					args.append(cond[2]) # Stat 1
					args.append(cond[3]) # condition (<, >, =)
					args.append(cond[4]) # Stat 2
				args.append(cond[-1]) # evolved pokemon

				workingmon.evolution.append(args)

		elif EDITING == "EXP GROUP":
			workingmon.expgroup = tempText[0].strip(' ').upper()+tempText[1:].strip(' ').lower()
		elif EDITING == "EGG GROUP":
			workingmon.eggGroup = tempText.lower().split(',')
		elif EDITING == "EXP DROP":
			try:
				workingmon.expDrop = int(tempText)
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
		elif EDITING == "BASE HAPPY":
			try:
				workingmon.baseHappiness = int(tempText)
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
	for button in range(26):
		if x > X and x < X+15:
			if y > Y and y < Y+15:
				if EDITING == "EVO COND":
					workingmon.evolution = []
				EDITING = ["ID", "", "FORMS?", "FORMS", "FSCALE", "BSCALE", "", "", "", "HP", "ATTACK", "DEFENSE", "S ATTACK", "S DEFENSE",  "SPEED",  "TYPES", "ABILITIES", "EVOLVES?", 
				"EVO COND", "EXP GROUP", "EXP DROP", "EGG GROUP", "FEMALE RATE", "SHINY RATE", "CAPTURE RATE", "BASE HAPPY"][button]
				tempText = ""
				return None
		Y += 20
	else:
		EDITING = ""
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
		tSize = int(bh / 2)
		workingmon.forward = False
		workingmon.draw(battle1, (int(bw/2),int(bh/2)), tSize)
		workingmon.forward = True
		workingmon.draw(battle2, (int(bw/2), int(bh/2)), tSize)
		setIcon(0,255,0)
	except:
		setIcon(0,0,255)
	## Draw the stat editor
	X = 50
	buttons = [
		"ID: %d" % workingmon.id,
		"$NB$Name: %s" % workingmon.name,
		"Has Forms? : %r" % (not workingmon.regular),
		"Forms: {0}".format(workingmon.forms),
		"Sprite Scale (F): %.2f" % workingmon.spriteFScale,
		"Sprite Scale (B): %.2f" % workingmon.spriteBScale,
		"$NB$Sprite Offset (F): {0}".format(workingmon.spriteFPosition),
		"$NB$Sprite Offset (B): {0}".format(workingmon.spriteBPosition),
		"$NB$BASE STATS (EV Yield) [StatMod stat^Mod] total: %d" % (workingmon.baseStats["HP"]+workingmon.baseStats["Attack"]["Physical"]+workingmon.baseStats["Defense"]["Physical"]+workingmon.baseStats["Attack"]["Special"]+workingmon.baseStats["Defense"]["Special"]+workingmon.baseStats["Speed"]),
		"HP:           %d (%d) [%d]" % (workingmon.baseStats["HP"], workingmon.EV_yield["HP"], workingmon.statMod["HP"]),
		"Attack:       %d (%d) [%d]" % (workingmon.baseStats["Attack"]["Physical"], workingmon.EV_yield["Attack"]["Physical"], workingmon.statMod["Attack"]["Physical"]),
		"Defense:      %d (%d) [%d]" % (workingmon.baseStats["Defense"]["Physical"], workingmon.EV_yield["Defense"]["Physical"], workingmon.statMod["Defense"]["Physical"]),
		"S Attack:     %d (%d) [%d]" % (workingmon.baseStats["Attack"]["Special"], workingmon.EV_yield["Attack"]["Special"], workingmon.statMod["Attack"]["Special"]),
		"S Defense:    %d (%d) [%d]" % (workingmon.baseStats["Defense"]["Special"], workingmon.EV_yield["Defense"]["Special"], workingmon.statMod["Defense"]["Special"]),
		"Speed:        %d (%d) [%d]" % (workingmon.baseStats["Speed"], workingmon.EV_yield["Speed"], workingmon.statMod["Speed"]),
		"Types: {0}".format(workingmon.typing.names),
		"Abilities: {0}".format(workingmon.abilities),
		"Evolves? : %r" % workingmon.evolves,
		"Conditions: {0}".format(workingmon.evolution),
		"Experience Group: %s" % workingmon.expgroup,
		"Experience Drop: %d" % workingmon.expDrop,
		"Egg Group: %s" % workingmon.eggGroup,
		"Female Rate (-1 for genderless): %.3f" % workingmon.femaleRate,
		"Shiny Rate: 1 in %d" % int(workingmon.shinyRate ** -1),
		"Capture Rate: %d" % workingmon.captureRate,
		"Base Happiness: %d" % workingmon.baseHappiness,
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
		blitText(surface, "Editing %s: %s" % (EDITING, tempText), (int(width*1/5), 25), textSize=30)
	
	workingmon.typing.drawV(dex, (0,0), "Bar")
	workingmon.typing.drawH(dex, (120,50), "Sphere", 0.2)
	workingmon.typing.drawH(dex, (120,0), "Icon", 0.25)

	
	if EDITING == "EVO COND":
		Y = 35
		tSize = 12
		fullTexts = ["level,[LEVEL]", "levelwitem,[LEVEL],[ITEM]", "levelwhappiness,[HAPPINESS]", "levelwarea,[AREA]","needitem,[ITEM]","levelwgender,[LEVEL],[GENDER]", "levelwgender+item,[LEVEL],[GENDER],[ITEM]","levelwparty,[LEVEL],[PARTYMEMBER]","levelwopen,[LEVEL],[NEWPOKE]","levelwstatdiff,[LEVEL],[STAT1],[COND],[STAT2]","levelwtime,[TIME],{HAPPINESS}"]
		fullTexts = [f+",[EVOLVES-TO]" for f in fullTexts]
		mini = len(fullTexts)
		if len(tempText) > 1:
			for x in range(len(fullTexts)-1,-1,-1):
				f = fullTexts[x]
				if tempText.split(",")[0].lower() not in f.split(",")[0].lower():
					fullTexts.pop(x)
		tSize = (mini-len(fullTexts)) + tSize
		for f in fullTexts:
			blitText(surface,f,(int(width*1/5)+50, 25+Y), color = (0,0,255), textSize = tSize)
			Y += tSize+5
	elif EDITING in ["HP", "SPEED", "ATTACK", "DEFENSE", "S ATTACK", "S DEFENSE"]:
		blitText(surface, "STAT,[EV Yield]:[STAT MOD]", (int(width*1/5)+50, 60), color=(0,0,255))


	## Draw dex data

	## Draw the next / previous pokemon in the dex
	surface.blit(dex, (width - dw, height - bh))
	surface.blit(battle1, (0, height - bw))
	surface.blit(battle2, (width - bw, 120))
	return surface


if __name__ == "__main__":
	## Screen Settings
	size = width, height = 800, 800
	pygame.mixer.pre_init(44100, 16, 2, 4096)
	pygame.init()
	
	pygame.mixer.init()
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
	workingmon.name = getPokeByID(workingmon.id)
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