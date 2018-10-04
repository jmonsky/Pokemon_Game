from element import Element

class Pokemon(object):

	def __init__(self):
		## Identification pieces
		self.name = ""
		self.id = 0
		self.shiny = False
		self.gender = "Attack Helicopter"
		self.form = "Normal"

		## Statistics
		self.level = 0
		self.exp = 0
		self.beg = 0
		self.hp = 0
		self.stats = {
			"HP":1,

			"Attack":{
				"Special":1,
				"Physical":1, },

			"Defense":{
				"Special":1,
				"Physical":1, },

			"Speed":1,
			}
		self.statMult = self.stats.copy()
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
			"Front":None#Sprite(),
			"Back":None#Sprite(),
		}
		#self.overworldSprite = None#Sprite() UNSURE ABOUT FOR NOW
		self.introAnimation = None#Animation()
		self.deathAnimation = None#Animation()
		self.actionAnimation = None#Animation()
		self.reactionAnimation = None#Animation()


test = Pokemon()
test.stats["HP"] = 20
print(test.shinyRate)
