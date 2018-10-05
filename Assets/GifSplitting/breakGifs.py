import subprocess, os
from os import listdir
from os.path import isfile, join
import shutil

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
	onlyfiles = [f for f in listdir(inDir) if isfile(join(inDir, f))]
	frames = str(len(onlyfiles))
	searchTerm = filename[:-4]
	
	with open(outDir+searchTerm+".frames", "w+") as FILE:
		FILE.write(frames)
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
		new_outDir = outDir+filename[:-4]
		os.mkdir(new_outDir)
		os.system(".\\IM\\convert.exe -coalesce "+inDir+filename+" "+new_outDir+"\\"+filename[:-4]+".png")
		#stichPNGS(inDir, new_outDir, spriteSheetDir, filename)
		#print("Clearing directory %s" % outDir)
		#clearDir(outDir)


breakGifs(".\\IN\\", ".\\OUT\\", ".\\SPRITESHEETS\\")
