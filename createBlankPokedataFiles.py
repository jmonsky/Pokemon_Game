from pokeName import *
import json
for ID in range(1,803):
	with open(".\\Data\\Pokemon\\"+getPokeFile(ID)+".json", "w+") as FILE:
		with open("base.json", "r") as file:
			baseInfo = json.loads(file.read())
		baseInfo["ID"] = ID
		baseInfo["Name"] = getPokeByID(ID)
		json.dump(baseInfo, FILE, indent = 4)