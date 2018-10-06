## pokemon.py
'''
	Houses the Pokemon and Pokedex classes

	Pokemon() -> Pokemon data structure, holds the all the information about a given pokemon
	Pokedex() -> Holds a series of pokemon and can be used to hold the baseline data for pokemon for construction later
'''

import random
from math import floor

from sprite import AnimatedSprite
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
		## Identification pieces
		self.name = ""
		self.id = 0
		self.shiny = False
		self.gender = "Attack Helicopter"
		self.form = ""
		self.forms = []
		self.forward = True
		self.eggGroup = ""

		## Statistics
		self.level = 0
		self.exp = 0
		self.expgroup = "Slow"
		self.hp = 0
		self.stats = baseStatDict(1)
		self.statMod = self.stats.copy()
		self.baseStats = self.stats.copy()
		self.IVS = self.stats.copy()
		self.EVS = self.stats.copy()
		self.typing = Element()
		self.nature = ""#Nature()
		self.abilities = ""#Ability()
		self.ability = ""
		self.happiness = 0
		self.evolution = None#EvolutionData()
		self.expDrop = 0

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
		self.regular = True
		self.loadedSprites = False
		self.formSprites = {}
		self.sprites = {
		"Normal":{
			"Front":None,
			"Back":None,
			},
		"Shiny":{
			"Front":None,
			"Back":None,
			},
		}
		self.spriteFPosition = (0,0)
		self.spriteBPosition = (0,0)
		self.spriteFScale = 1
		self.spriteBScale = 1
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
		self.sprites = {
		"Normal":{
			"Front":None,
			"Back":None,
			},
		"Shiny":{
			"Front":None,
			"Back":None,
			},
		}
		self.loadedSprites = False


	def loadSprites(self):
		self.loadedSprites = True
		def pad0(num):
			n = str(num)
			if len(n) == 1:
				n = "00"+n
			elif len(n) == 2:
				n = "0"+n
			return n
		if not self.regular:
			for i in self.forms:
				self.formSprites[i] = {
				"Normal":{
					"Front":AnimatedSprite(pad0(self.id)+"_"+i.upper()+"_NF"),
					"Back":AnimatedSprite(pad0(self.id)+"_"+i.upper()+"_NB"),
					},
				"Shiny":{
					"Front":AnimatedSprite(pad0(self.id)+"_"+i.upper()+"_SF"),
					"Back":AnimatedSprite(pad0(self.id)+"_"+i.upper()+"_SB"),
					},
				}
			try:
				self.formSprites["NORMAL"] = {
				"Normal":{
					"Front":AnimatedSprite(pad0(self.id)+"_NF", False),
					"Back":AnimatedSprite(pad0(self.id)+"_NB", False),
					},
				"Shiny":{
					"Front":AnimatedSprite(pad0(self.id)+"_SF", False),
					"Back":AnimatedSprite(pad0(self.id)+"_SB", False),
					},
				}
				self.form = "NORMAL"
				self.forms.append("NORMAL")
			except:
				pass
		else:
			self.sprites = {
			"Normal":{
				"Front":AnimatedSprite(pad0(self.id)+"_NF"),
				"Back":AnimatedSprite(pad0(self.id)+"_NB"),
				},
			"Shiny":{
				"Front":AnimatedSprite(pad0(self.id)+"_SF"),
				"Back":AnimatedSprite(pad0(self.id)+"_SB"),
				},
			}
		

	def draw(self, surface, off, scalar=1):
		if self.loadedSprites:
			if self.regular:
				if self.forward:
					pos = (self.spriteFPosition[0]+off[0], self.spriteFPosition[1]+off[1])
					if self.shiny:
						self.sprites["Shiny"]["Front"].draw(surface, pos, scalar*self.spriteFScale)
					else:
						self.sprites["Normal"]["Front"].draw(surface, pos, scalar*self.spriteFScale)
				else:
					pos = (self.spriteBPosition[0]+off[0], self.spriteBPosition[1]+off[1])
					if self.shiny:
						self.sprites["Shiny"]["Back"].draw(surface, pos, scalar*self.spriteBScale)
					else:
						self.sprites["Normal"]["Back"].draw(surface, pos, scalar*self.spriteBScale)
			else:
				if self.forward:
					pos = (self.spriteFPosition[0]+off[0], self.spriteFPosition[1]+off[1])
					if self.shiny:
						self.formSprites[self.form]["Shiny"]["Front"].draw(surface, pos, scalar*self.spriteFScale)
					else:
						self.formSprites[self.form]["Normal"]["Front"].draw(surface, pos, scalar*self.spriteFScale)
				else:
					pos = (self.spriteBPosition[0]+off[0], self.spriteBPosition[1]+off[1])
					if self.shiny:
						self.formSprites[self.form]["Shiny"]["Back"].draw(surface, pos, scalar*self.spriteBScale)
					else:
						self.formSprites[self.form]["Normal"]["Back"].draw(surface, pos, scalar*self.spriteBScale)
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
		if poke.regular:
			self.form = "Normal"
			self.forms = []
		else:
			self.form = poke.forms[0]
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
		self.typing = poke.typing.copy()
		self.exp = expToLevel(self, level)
		self.expgroup = poke.expgroup
		self.expDrop = poke.expDrop
		self.abilities = poke.abilities
		self.ability = random.choice(self.abilities).copy() ## Needs rewrite for hiddenabilites

		self.evolution = poke.evolution.copy()

		self.femaleRate = poke.femaleRate
		self.shinyRate = poke.shinyRate
		self.captureRate = poke.captureRate

		self.regular = poke.regular

		self.introAnimation = poke.introAnimation#.copy()
		self.deathAnimation = poke.deathAnimation#.copy()
		self.actionAnimation = poke.actionAnimation#.copy()
		self.reactionAnimation = poke.reactionAnimation#.copy()



