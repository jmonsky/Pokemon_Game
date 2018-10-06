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

class AnimatedSprite(object):
	def __init__(self, anim, lazyLoad=True):
		self.source = anim
		self.loaded = False
		self.index = 0
		self.ptime = 0
		self.runStep = 1
		self.running = True
		if not lazyLoad:
			self.load()

	def load(self):
		if not self.loaded:
			anim = self.source
			inDir = ".\\Assets\\Animations\\"+anim+"\\"
			self.sprite_sheet = [pygame.image.load(inDir+f) for f in listdir(inDir) if isfile(join(inDir, f))]
			self.fWidth = self.sprite_sheet[0].get_width()
			self.fHeight = self.sprite_sheet[0].get_height()
			self.path = anim
			self.frames = len(self.sprite_sheet)
			self.frameRate = self.frames/3
			self.runTime = self.frames / self.frameRate
			self.loaded = True

	def copy(self):
		new = AnimatedSprite(self.source)
		new.runStep = self.runStep
		new.frameRate = self.frameRate
		return new

	def get_image(self, frame):
		if self.loaded:
			image = pygame.Surface((self.fWidth, self.fHeight), SRCALPHA)
			image.blit(self.sprite_sheet[frame], (0, 0))


			return image


	def draw(self, surface, pos, scale = 1):
		if self.loaded:
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

	def setFrameRate(self, fr):
		self.frameRate = fr
		self.runTime = self.frames / self.frameRate
