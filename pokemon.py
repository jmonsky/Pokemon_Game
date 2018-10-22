## pokemon.py
'''
	Houses the Pokemon and Pokedex classes

	Pokemon() -> Pokemon data structure, holds the all the information about a given pokemon
	Pokedex() -> Holds a series of pokemon and can be used to hold the baseline data for pokemon for construction later
'''

import random
from math import floor

import os

import pygame

from sprite import OverworldSprite, BattleSprite
from element import Element
from experience import checkLevel, expToLevel

def baseStatDict(n):
	return {
			"HP":n,

			"Attack":{
				"Special":n,
				"Physical":n, },

			"Defense":{
				"Special":n,
				"Physical":n, },

			"Speed":n,
			}

def addStatDicts(s1, s2):
	return {
		"HP":s1["HP"]+s2["HP"],

		"Attack":{
			"Special":s1["Attack"]["Special"]+s2["Attack"]["Special"],
			"Physical":s1["Attack"]["Physical"]+s2["Attack"]["Physical"], },

		"Defense":{
			"Special":s1["Defense"]["Special"]+s2["Defense"]["Special"],
			"Physical":s1["Defense"]["Physical"]+s2["Defense"]["Physical"], },

		"Speed":s1["Speed"]+s2["Speed"],
	}

class Pokedex(object):
	def __init__(self):
		self.pokes = {}

	def addPokemon(self, pokemon):
		self.pokes[pokemon.name] = pokemon.copy()

	def generateAPoke(self, id, level):
		for poke in self.pokes.keys():
			if poke.id == id:
				return construct(poke, level)

	def displayAPoke(self, surface, poke, scale = 1):
		if poke in self.pokes:
			self.pokes[poke].draw(surface, scale)

	def copy(self):
		new = Pokedex()
		for poke in self.pokes.keys():
			new.addPokemon(self.pokes[pokes])
		return new

	def readyToPickle():
		[self.pokes[poke].unloadSprites() for poke in self.pokes.keys()]



class Pokemon(object):
	def __init__(self):
		self.version = 3
		## Identification pieces
		self.name = ""
		self.id = 0
		self.shiny = False
		self.gender = "Attack Helicopter"
		self.forms = {}
		self.forward = True
		self.overworldDir = "down"
		self.diffFemale = False
		self.eggGroup = []

		## Statistics
		self.level = 0
		self.exp = 0
		self.expgroup = "Slow"
		self.hp = 0
		self.stats = baseStatDict(1)
		self.statMod = baseStatDict(1)
		self.baseStats = baseStatDict(0)
		self.IVS = baseStatDict(0)
		self.EVS = baseStatDict(0)
		self.EV_yield = baseStatDict(0)
		self.typing = Element()
		self.nature = ""#Nature()
		self.abilities = ""#Ability()
		self.ability = ""
		self.happiness = 0
		self.evolution = None#EvolutionData()
		self.expDrop = 0
		self.baseHappiness = 0

		## Personalization
		self.nickname = ""
		self.originalTrainer = ""
		self.trainer = None#Pointer to trainer
		self.item = ""#Item()

		## Battle Attributes
		self.moves = []#MoveSet()
		self.inflictions = []#Infliction()
		self.party = []#Party()
		self.evolution = []
		self.evolves = False

		## Encounter Statistics
		self.femaleRate = 0.5
		self.shinyRate = 1/4096
		self.captureRate = 0

		## Other Junk
		self.loadedSprites = False
		self.battleSprite = None
		self.overworldSprite = None
		self.spriteFPosition = (0,0)
		self.spriteBPosition = (0,0)
		self.spriteFScale = 1
		self.spriteBScale = 1
		self.spriteOScale = 1
		#self.overworldSprite = None#Sprite() UNSURE ABOUT FOR NOW
		self.introAnimation = None#Animation()
		self.deathAnimation = None#Animation()
		self.actionAnimation = None#Animation()
		self.reactionAnimation = None#Animation()

	def copy(self):
		new = Pokemon()
		new.construct(self, self.level)
		new.exp = self.exp
		return new


	def _setStats(self):
		'''
			Function will set the stats based on the current level, also returns the stat delta
		'''
		OLDSTATS = self.stats.copy()
		Nmod = 1 ## Change later when natures get added in
		self.stats = {
			"HP": int(((self.baseStats["HP"] * 2 + self.IVS["HP"]*(self.level/100.0) + (self.EVS["HP"]/4) ) * (self.level / 100) + 10 + self.level) ** self.statMod["HP"]),
			"Attack":{
				"Special":int(((self.baseStats["Attack"]["Special"] * 2 + self.IVS["Attack"]["Special"]*(self.level/100.0) + (self.EVS["Attack"]["Special"]/4) ) * (self.level / 100) + 5) * Nmod ** self.statMod["Attack"]["Special"]),
				"Physical":int(((self.baseStats["Attack"]["Physical"] * 2 + self.IVS["Attack"]["Physical"]*(self.level/100.0) + (self.EVS["Attack"]["Physical"]/4) ) * (self.level / 100) + 5) * Nmod ** self.statMod["Attack"]["Physical"]),
			},
			"Defense":{
				"Special":int(((self.baseStats["Defense"]["Special"] * 2 + self.IVS["Defense"]["Special"]*(self.level/100.0) + (self.EVS["Defense"]["Special"]/4) ) * (self.level / 100) + 5) * Nmod ** self.statMod["Defense"]["Special"]),
				"Physical":int(((self.baseStats["Defense"]["Physical"] * 2 + self.IVS["Defense"]["Physical"]*(self.level/100.0) + (self.EVS["Defense"]["Physical"]/4) ) * (self.level / 100) + 5) * Nmod ** self.statMod["Defense"]["Physical"]),
			},
			"Speed":int(((self.baseStats["Speed"] * 2 + self.IVS["Speed"]*(self.level/100.0) + (self.EVS["Speed"]/4) ) * (self.level / 100) + 5) * Nmod ** self.statMod["Speed"]),
		}
		STATDELTA = {
			"HP":self.stats["HP"]-OLDSTATS["HP"],
			"Attack":{
				"Special":self.stats["Attack"]["Special"]-OLDSTATS["Attack"]["Special"],
				"Physical":self.stats["Attack"]["Physical"]-OLDSTATS["Attack"]["Physical"],
			},
			"Defense":{
				"Special":self.stats["Defense"]["Special"]-OLDSTATS["Defense"]["Special"],
				"Physical":self.stats["Defense"]["Physical"]-OLDSTATS["Defense"]["Physical"],
			},
			"Speed":self.stats["Speed"]-OLDSTATS["Speed"],
		}

		return STATDELTA

	def unloadSprites(self):
		self.battleSprite = None
		self.overworldSprite = None
		self.typing.unloadSprites()
		self.loadedSprites = False


	def loadSprites(self):
		self.loadedSprites = True
		self.typing.loadSprites()
		self.overworldSprite = OverworldSprite(str(self.id), False)
		self.battleSprite = BattleSprite(str(self.id), False)
		

	def drawBattle(self, surface, off, targetHeight=100):
		if self.loadedSprites:
			scaling = (targetHeight/self.battleSprite.height)
			X = 0
			Y = 0
			if self.forward:
				scaling *= self.spriteFScale
				X -= self.spriteFPosition[0]
				Y -= self.spriteFPosition[1]
			else:
				scaling *= self.spriteBScale
				X -= self.spriteBPosition[0]
				Y -= self.spriteBPosition[1]
			X += (scaling * self.battleSprite.width)/2
			Y += (scaling * self.battleSprite.height)/2
			if self.forward:
				self.battleSprite.dir = "Front"
			else:
				self.battleSprite.dir = "Back"
			self.battleSprite.shiny = self.shiny
			self.battleSprite.draw(surface, (off[0]-X, off[1]-Y), scaling)
		else:
			self.loadSprites()

	def drawOverworld(self, surface, off, targetSize=64):
		if self.loadedSprites:
			scaling = (targetSize/self.overworldSprite.fHeight)
			X = 0
			Y = 0
			scaling *= self.spriteOScale
			X += (scaling * self.overworldSprite.fWidth)/2
			Y += (scaling * self.overworldSprite.fHeight)/2
			self.overworldSprite.dir = self.overworldDir
			if self.shiny:
				self.overworldSprite.TYPE = "Shiny"
			else:
				self.overworldSprite.TYPE = "Regular"
			self.overworldSprite.draw(surface, (off[0]-X, off[1]-Y), scaling)
		else:
			self.loadSprites()

	def checkLevelUp(self):
		return checkLevel(self)

	def construct(self, pokedexEntry, level=1):
		poke = pokedexEntry

		## Copy Identification pieces
		self.name = poke.name
		self.id = poke.id
		self.shiny = False
		self.eggGroup = poke.eggGroup
		if random.random() < poke.shinyRate:
			self.shiny = True
		genderRand = random.random()
		if self.femaleRate == -1:
			if genderRand < 1/8192:
				pass
			else:
				if genderRand < self.femaleRate:
					self.gender = "Female"
				else:
					self.gender = "Male"
			self.gender = "Genderless"
		self.forms = poke.forms.copy()

		## Copy & Create Statistics
		self.level = level
		self.baseStats = poke.baseStats.copy()
		self.IVS = {
			"HP":random.randint(0,31),
			"Attack":{
				"Special":random.randint(0,31),
				"Physical":random.randint(0,31), },
			"Defense":{
				"Special":random.randint(0,31),
				"Physical":random.randint(0,31), },
			"Speed":random.randint(0,31),
			}
		self.EVS = baseStatDict(0)
		self.statMod = poke.statMod.copy()
		self._setStats()
		self.baseHappiness = poke.baseHappiness
		self.typing = poke.typing.copy()
		self.exp = expToLevel(self, level)
		self.expgroup = poke.expgroup
		self.EV_yield = poke.EV_yield.copy()
		self.expDrop = poke.expDrop
		self.abilities = poke.abilities
		self.ability = random.choice(self.abilities).copy() ## Needs rewrite for hiddenabilites

		self.evolution = poke.evolution.copy()

		self.diffFemale = poke.diffFemale

		self.spriteOScale = poke.spriteOScale
		self.spriteBScale = poke.spriteBScale
		self.spriteFScale = poke.spriteFScale

		self.spriteFPosition = poke.spriteFPosition
		self.spriteBPosition = poke.spriteBPosition

		self.femaleRate = poke.femaleRate
		self.shinyRate = poke.shinyRate
		self.captureRate = poke.captureRate

		self.introAnimation = poke.introAnimation#.copy()
		self.deathAnimation = poke.deathAnimation#.copy()
		self.actionAnimation = poke.actionAnimation#.copy()
		self.reactionAnimation = poke.reactionAnimation#.copy()



