import subprocess, os
from os import listdir
from os.path import isfile, join
import shutil
from time import sleep

def clearDir(folder):
	for the_file in os.listdir(folder):
		file_path = os.path.join(folder, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
			#elif os.path.isdir(file_path): shutil.rmtree(file_path)
		except Exception as e:
			print(e)

def stichPNGS(refdir, inDir, outDir, filename):
	searchTerm = filename[:-4]
	print("Stitching %s" % searchTerm)
	os.system(".\\IM\\convert.exe "+inDir+"*.png +append "+outDir+searchTerm+"_SS.png")

def breakGifs(inDir, outDir, spriteSheetDir):
	onlyfiles = [f for f in listdir(inDir) if isfile(join(inDir, f))]
	gifs = []
	for file in onlyfiles:
		if ".gif" in file:
			gifs.append(file)
	for filename in gifs:
		print("Splitting %s" % filename)
		os.system(".\\IM\\convert.exe -coalesce "+inDir+filename+" "+outDir+filename[:-4]+".png")
		stichPNGS(inDir, outDir, spriteSheetDir, filename)
		print("Clearing directory %s" % outDir)
		clearDir(outDir)


breakGifs(".\\IN\\", ".\\OUT\\", ".\\SPRITESHEETS\\")
