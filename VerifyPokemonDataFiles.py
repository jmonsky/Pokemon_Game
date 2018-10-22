from pokeName import *
import json
for ID in range(1,807):
	baseInfo = None
	try:
		with open(".\\Data\\Pokemon\\"+getPokeFile(ID)+".json", "r") as FILE:
			try:
				baseInfo = eval(FILE.read())
				spec = baseInfo["Species"]
				if "Pokemon" not in spec:
					spec = spec + " Pokemon"
				if spec == " Pokemon":
					spec = ""
				baseInfo["Species"] = spec
			except:
				print("Error Cleaning up %s's file" % getPokeByID(ID))
			else:
				with open(".\\Data\\Pokemon\\"+getPokeFile(ID)+".json", "w+") as FILE:
					if baseInfo != None:
						json.dump(baseInfo, FILE, indent = 4)
	except:
		print("Couldnt find %s's data file so creating a baseline file" % getPokeByID(ID))
		with open("base.json") as baseFile:
			baseInfo = eval(baseFile.read())
		baseInfo["Name"] = getPokeByID(ID)
		baseInfo["ID"] = ID
		with open(".\\Data\\Pokemon\\"+getPokeFile(ID)+".json", "w+") as file:
			json.dump(baseInfo, file, indent = 4)
input("Press Enter To Exit... ")