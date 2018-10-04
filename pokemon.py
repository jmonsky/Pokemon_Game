import random
from math import floor

from element import Element
from experience import checkLevel

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

class Pokemon(object):
	def __init__(self):
		## Identification pieces
		self.name = ""
		self.id = 0
		self.shiny = False
		self.gender = "Attack Helicopter"
		self.form = "Normal"
		self.forms = []

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
		self.happiness = 0

		## Personalization
		self.nickname = ""
		self.originalTrainer = ""
		self.trainer = None#Pointer to trainer
		self.item = ""#Item()

		## Battle Attributes
		self.moves = []#MoveSet()
		self.inflictions = []#Infliction()
		self.party = []#Party()

		## Encounter Statistics
		self.femaleRate = 0
		self.shinyRate = 1/4096
		self.captureRate = 0

		## Other Junk
		self.regular = True
		self.sprites = {
			"Front":None,#Sprite(),
			"Back":None,#Sprite(),
		}
		#self.overworldSprite = None#Sprite() UNSURE ABOUT FOR NOW
		self.introAnimation = None#Animation()
		self.deathAnimation = None#Animation()
		self.actionAnimation = None#Animation()
		self.reactionAnimation = None#Animation()

	def checkForLevelUps(self):
		totalDelta = baseStatDict(0)
		td = checkLevel(self)
		while td != None:
			totalDelta = addStatDicts(totalDelta, td)
			td = checkLevel(self)
		return totalDelta
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

	def construct(self, pokedexEntry, level=1):
		poke = pokedexEntry

		## Copy Identification pieces
		self.name = poke.name
		self.id = poke.id
		self.shiny = False
		if random.random() < poke.shinyRate:
			self.shiny = True
		genderRand = random.random()
		if genderRand < 1/8192:
			pass
		else:
			if genderRand < self.femaleRate:
				self.gender = "Female"
			else:
				self.gender = "Male"
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
		self.EVS = poke.EVS.copy()
		self.statMod = poke.statMod.copy()
		self._setStats()
		self.typing = poke.typing.copy()
		self.exp = poke.exp
		self.expgroup = poke.expgroup






test = Pokemon()
test.typing = Element("Ghost", "Dragon")
test.baseStats = {
			"HP":150,
			"Attack":{
				"Special":120,
				"Physical":120, },
			"Defense":{
				"Special":100,
				"Physical":100, },
			"Speed":90,
			}
test.construct(test, 1)
# for EXP in range(1, 5000, 100):
# 	test.exp = EXP
# 	print(EXP, test.level, test.checkForLevelUps(), test.stats)
test.exp = 6000000
print(test.stats)
print(test.checkForLevelUps())
print(test.level)
print(test.stats)
print(test.exp)