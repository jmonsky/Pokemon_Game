## element.py
'''
	Houses pokemon and move typing data
'''

from sprite import Sprite

element_Advantages = {
	"Typeless":{
		"SE":[],
		"NE":[],
		"RA":[],
		"WA":[],
		"IM":[],
		"IE":[],
	},
	"Bug":{
		"SE":["Dark", "Grass", "Psychic"], ## Super Effective
		"NE":["Fighting", "Fire", "Flying", "Ghost", "Rock", "Steel", "Fairy", "Poison"], ## Not very Effective
		"RA":["Fighting", "Grass", "Ground"], ## Resistant Against
		"WA":["Fire", "Flying", "Rock"], ## Weak Against
		"IM":[], ## Immune To
		"IE":[], ## Ineffective Against (They are immune)
	},
	"Dark":{
		"SE":["Ghost", "Psychic"],
		"NE":["Dark", "Fighting", "Fairy"],
		"RA":["Dark", "Ghost"],
		"WA":["Bug", "Fighting", "Fairy"],
		"IM":["Psychic"],
		"IE":[],
	},
	"Dragon":{
		"SE":["Dragon"],
		"NE":["Steel"],
		"RA":["Electric", "Fire", "Grass", "Water"],
		"WA":["Ice", "Dragon", "Fairy"],
		"IM":[],
		"IE":["Fairy"],
	},
	"Electric":{
		"SE":["Flying", "Water"],
		"NE":["Electric", "Dragon", "Grass"],
		"RA":["Flying", "Steel", "Electric"],
		"WA":["Ground"],
		"IM":[],
		"IE":["Ground"],
	},
	"Fairy":{
		"SE":["Dragon", "Dark", "Fighting"],
		"NE":["Fire", "Poison", "Steel"],
		"RA":["Bug", "Dark", "Fighting"],
		"WA":["Steel", "Poison"],
		"IM":["Dragon"],
		"IE":[],
	},
	"Fighting":{
		"SE":["Normal", "Steel", "Rock", "Ice", "Dark"],
		"NE":["Fairy", "Psychic", "Flying", "Bug", "Poison"],
		"RA":["Bug", "Dark", "Rock"],
		"WA":["Fairy", "Flying", "Psychic"],
		"IM":[],
		"IE":["Ghost"],
	},
	"Fire":{
		"SE":["Grass", "Bug", "Steel", "Ice"],
		"NE":["Rock", "Water", "Fire", "Dragon"],
		"RA":["Bug", "Fairy", "Fire", "Grass", "Ice", "Steel"],
		"WA":["Ground", "Rock", "Water"],
		"IM":[],
		"IE":[],
	},
	"Flying":{
		"SE":["Grass", "Bug", "Fighting"],
		"NE":["Electric", "Rock", "Steel"],
		"RA":["Bug", "Fighting", "Grass"],
		"WA":["Electric", "Ice", "Rock"],
		"IM":["Ground"],
		"IE":[],
	},
	"Ghost":{
		"SE":["Ghost", "Psychic"],
		"NE":["Dark"],
		"RA":["Bug", "Poison"],
		"WA":["Ghost", "Dark"],
		"IM":["Normal", "Fighting"],
		"IE":["Normal"],
	},
	"Grass":{
		"SE":["Water", "Rock", "Water"],
		"NE":["Bug", "Dragon", "Fire", "Flying", "Grass", "Poison", "Steel"],
		"RA":["Electric", "Grass", "Ground", "Water"],
		"WA":["Bug", "Fire", "Flying", "Ice", "Poison"],
		"IM":[],
		"IE":[],
	},
	"Ground":{
		"SE":["Electric", "Fire", "Poison", "Rock", "Steel"],
		"NE":["Bug", "Grass"],
		"RA":["Poison", "Rock"],
		"WA":["Grass", "Ice", "Water"],
		"IM":["Electric"],
		"IE":["Flying"],
	},
	"Ice":{
		"SE":["Dragon", "Flying", "Grass", "Ground"],
		"NE":["Ice", "Fire", "Steel", "Water"],
		"RA":["Ice"],
		"WA":["Fighting", "Fire", "Rock", "Steel"],
		"IM":[],
		"IE":[],
	},
	"Normal":{
		"SE":[],
		"NE":["Steel", "Rock"],
		"RA":[],
		"WA":["Fighting"],
		"IM":["Ghost"],
		"IE":["Ghost"],
	},
	"Poison":{
		"SE":["Grass", "Fairy"],
		"NE":["Ghost", "Ground", "Poison", "Rock"],
		"RA":["Bug", "Fairy", "Fighting", "Grass", "Poison"],
		"WA":["Ground", "Psychic"],
		"IM":[],
		"IE":["Steel"],
	},
	"Psychic":{
		"SE":["Fighting", "Poison"],
		"NE":["Psychic", "Steel"],
		"RA":["Fighting",  "Psychic"],
		"WA":["Dark", "Bug", "Ghost"],
		"IM":[],
		"IE":["Dark"],
	},
	"Rock":{
		"SE":["Flying", "Fire", "Ice", "Bug"],
		"NE":["Ground", "Steel", "Fighting"],
		"RA":["Fire", "Flying", "Normal", "Poison"],
		"WA":["Fighting", "Grass", "Ground", "Steel", "Water"],
		"IM":[],
		"IE":[],
	},
	"Steel":{
		"SE":["Fairy", "Ice", "Rock"],
		"NE":["Electric", "Fire", "Steel", "Water"],
		"RA":["Bug", "Dragon", "Fairy", "Flying", "Grass", "Ice", "Normal", "Psychic", "Rock", "Steel"],
		"WA":["Fire", "Fighting", "Ground"],
		"IM":["Poison"],
		"IE":[],
	},
	"Water":{
		"SE":["Fire", "Ground", "Rock"],
		"NE":["Dragon", "Grass", "Water"],
		"RA":["Fire", "Ice", "Steel", "Water"],
		"WA":["Electric", "Grass"],
		"IM":[],
		"IE":[],
	},
}



class Element(object):
	def __init__(self,  *types):
		self.types = len(types)
		self.names = []
		self.dictionaries = {}
		self.sprite = {
			"Sphere":[],
			"Icon":[],
			"Bar":[],
			"Egg":[],
		}
		self.spritesLoaded = False
		for T in types:
				T = T[0].upper()+T[1:].lower()
				self.names.append(T)
				self.dictionaries[T] = element_Advantages[T]

	def __gt__(self, otherType):
		multiplier = 1
		for myType in self.names:
			for opType in otherType.names:
				if opType in self.dictionaries[myType]["SE"]:
					multiplier *= 2
				elif opType in self.dictionaries[myType]["IE"]:
					multiplier *= 0
				elif opType in self.dictionaries[myType]["NE"]:
					multiplier *= 0.5
		return multiplier

	def draw(self, surface, pos, drawType, scale=1):
		if self.spritesLoaded:
			self.sprite[drawType][0].draw(surface, pos, scale)
		else:
			self.loadSprites()


	def drawV(self, surface, pos, drawType, scale=1):
		if self.spritesLoaded:
			Y = 0
			for s in self.sprite[drawType]:
				s.draw(surface, (pos[0], pos[1]+Y), scale)
				Y += s.height*scale
		else:
			self.loadSprites()

	def drawH(self, surface, pos, drawType, scale=1):
		if self.spritesLoaded:
			X = 0
			for s in self.sprite[drawType]:
				s.draw(surface, (pos[0]+X, pos[1]), scale)
				X += s.width*scale
		else:
			self.loadSprites()

	def loadSprites(self):
		if not self.spritesLoaded:
			for T in self.names:
				t = T.lower()
				self.sprite["Sphere"].append(Sprite("sphere2_"+t))
				self.sprite["Icon"].append(Sprite("sphere1_"+t))
				self.sprite["Egg"].append(Sprite("sphere3_"+t))
				self.sprite["Bar"].append(Sprite("type_"+t))

		self.spritesLoaded = True

	def unloadSprites(self):
		self.sprite = {
			"Sphere":[],
			"Icon":[],
			"Bar":[],
			"Egg":[],
		}
		self.spritesLoaded = False

	def copy(self):
		copy = Element()
		copy.types = self.types + 0
		copy.names = self.names.copy()
		copy.dictionaries = self.dictionaries.copy()

		return copy

	def __add__(self, newType):
		baby = self.copy()
		if newType not in baby:
			for NAME in newType.names:
				baby.types += 1
				baby.names.append(NAME)
				baby.dictionaries[NAME] = newType.dictionaries[NAME]
		return baby

	def __lt__(self, otherType):
		multiplier = 1
		for myType in self.names:
			for opType in otherType.names:
				if myType in otherType.dictionaries[opType]["WA"]:
					multiplier *= 2
				elif myType in otherType.dictionaries[opType]["IM"]:
					multiplier *= 0
				elif myType in otherType.dictionaries[opType]["RA"]:
					multiplier *= 0.5
		return multiplier

	def __eq__(self, other):
		count = 0
		if self.types != other.types:
			return False
		for i in other.names:
			if i in self.names:
				count += 1
		if count != self.types:
			return False
		else:
			return True

	def __contains__(self, value):
		cv = []
		for i in value.names:
			if i in self.names:
				cv.append(1)
		if sum(cv) == value.types:
			return True
		else:
			return False

	def __ne__(self, other):
		return not self.__eq__(other)

	def __len__(self):
		return len(self.names)

	def __str__(self):
		s = "Element("
		for i in self.names:
			s += "'" + i + "', "
		s += ")"
		return s

if __name__ == "__main__":
	types = list(element_Advantages.keys())
	elements = []
	for i in types:
		elements.append(Element(i))
	supertype = elements[0]
	for i in range(1,len(elements)):
		supertype += elements[i]
	print(supertype)
	for i in elements:
		print(i.names[0], i > supertype)