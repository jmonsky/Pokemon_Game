## sprite.py
'''
	Houses the sprite and animated sprite class

	Sprite() -> Just an image basically
	AnimatedSprite() -> An animation that loads all the images in a directory into an array and plays through them
'''

import pygame
from pygame.locals import *

from os import listdir
from os.path import isfile, join
from time import time

class Sprite(object):
	def __init__(self, sprite, lazyLoad=True):
		self.source = sprite
		self.loaded = False
		if not lazyLoad:
			self.load()

	def unload(self):
		self.image = None
		self.loaded = False

	def load(self):
		if not self.loaded:
			img = self.source
			path = ".\\Assets\\Sprites\\"+img+".png"
			self.image = pygame.image.load(path)
			self.width = self.image.get_width()
			self.height = self.image.get_height()
			self.loaded = True

	def copy(self):
		new = Sprite(self.source)
		return new

	def draw(self, surface, pos, scale = 1):
		if self.loaded:
			img = pygame.Surface((self.width, self.height), SRCALPHA)
			img.blit(self.image, (0,0))
			if scale != 1:
				img = pygame.transform.scale(img, (int(self.width * scale), int(self.height * scale)))
			surface.blit(img, pos)
		else:
			self.load()

class BattleSprite(object):
	def __init__(self, sprite, lazyLoad=True):
		self.source = sprite
		self.loaded = False
		self.dir = "Front"
		self.shiny = False
		if not lazyLoad:
			self.load()

	def unload(self):
		self.image = None
		self.loaded = False

	def load(self):
		if not self.loaded:
			img = self.source
			path = ".\\Assets\\Pokemon\\Battle\\"
		
			self.images = {}
			try:
				self.images["Shiny Front"] = pygame.image.load(path+img+"s.png")
			except:
				pass
			try:
				self.images["Shiny Back"] = pygame.image.load(path+img+"sb.png")
			except:
				pass
			try:
				self.images["Regular Front"] = pygame.image.load(path+img+".png")
			except:
				pass
			try:
				self.images["Regular Back"] = pygame.image.load(path+img+"b.png")
			except:
				pass
			try:
				self.width = self.images["Regular Front"].get_width()
				self.height = self.images["Regular Front"].get_height()
			except:
				self.loaded = False
			self.loaded = True

	def copy(self):
		new = Sprite(self.source)
		return new

	def draw(self, surface, pos, scale = 1):
		if self.loaded:
			IMAGE = {"Front":{True:"Shiny Front", False:"Regular Front"}, "Back":{True:"Shiny Back", False:"Regular Back"}}[self.dir][self.shiny]
			img = pygame.Surface((self.width, self.height), SRCALPHA)
			try:
				img.blit(self.images[IMAGE], (0,0))
			except:
				return None
			if scale != 1:
				img = pygame.transform.scale(img, (int(self.width * scale), int(self.height * scale)))
			surface.blit(img, pos)
		else:
			self.load()


class OverworldSprite(object):
	def __init__(self, anim, lazyLoad=True):
		self.source = anim
		self.loaded = False
		self.index = 0
		self.ptime = 0
		self.runStep = 1
		self.running = True
		self.dir = "up"
		self.exists = True
		self.TYPE = "Regular"
		if not lazyLoad:
			self.load()

	def unload(self):
		self.sprite_sheet = None
		self.loaded = False

	def load(self):
		if not self.loaded:
			anim = self.source
			inDir = ".\\Assets\\Pokemon\\Overworld\\"+anim
			self.sprite_sheets = {}
			try:
				self.sprite_sheets["Regular"] = pygame.image.load(inDir+".png")
			except:
				pass
			try:
				self.sprite_sheets["Shiny"] = pygame.image.load(inDir+"s.png")
			except:
				pass
			try:
				self.sprite_sheets["Female"] = pygame.image.load(inDir+"f.png")
			except:
				pass
			try:
				self.sprite_sheets["FemaleShiny"] = pygame.image.load(inDir+"fs.png")
			except:
				pass
			try:
				self.fWidth = self.sprite_sheets["Regular"].get_width()/4
				self.fHeight = self.sprite_sheets["Regular"].get_height()/4
			except:
				self.exists = False
				self.fWidth = 1
				self.fHeight = 1
			self.frames = 4
			self.frameRate = self.frames / 0.5
			self.runTime = self.frames / self.frameRate
			self.loaded = True

	def copy(self):
		new = AnimatedSprite(self.source)
		new.runStep = self.runStep
		new.frameRate = self.frameRate
		return new

	def get_image(self, frame):
		if self.loaded and self.exists:
			image = pygame.Surface((self.fWidth, self.fHeight), SRCALPHA)

			positions = {
				"up":3,
				"down":0,
				"right":2,
				"left":1,
			}

			image.blit(self.sprite_sheets[self.TYPE], (-self.fWidth*frame, -positions[self.dir]*self.fHeight))
			return image

	def draw(self, surface, pos, scale = 1):
		if self.loaded and self.exists:
			img = self.get_image(self.index)
			if scale != 1:
				img = pygame.transform.scale(img, (int(self.fWidth * scale), int(self.fHeight * scale)))
			surface.blit(img, pos)
			if self.running:
				if time()-self.ptime > 1/self.frameRate:
					self.ptime = time()
					self.index += self.runStep
					if self.index >= self.frames:
						self.index = 0
					if self.index < 0:
						self.index = self.frames-1
		else:
			self.load()

	def pause(self):
		self.running = False

	def play(self):
		self.running = True

	def reverse(self):
		self.runStep = -abs(self.runStep)

	def forward(self):
		self.runStep = abs(self.runStep)

	def switchDir(self):
		self.runStep *= -1

	def setFrameSkip(self, framesToSkip):
		self.runStep = 1*((self.runStep)/(abs(self.runStep))) + framesToSkip

	def setFrameRate(self, fr):
		self.frameRate = fr
		self.runTime = self.frames / self.frameRate
