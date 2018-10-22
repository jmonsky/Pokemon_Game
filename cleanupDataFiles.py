from pokeName import *
import json
for ID in range(1,803):
	baseInfo = None
	with open(".\\Data\\Pokemon\\"+getPokeFile(ID)+".json", "r") as FILE:
		try:
			baseInfo = eval(FILE.read())
		except:
			print("Error Cleaning up %s's file" % getPokeByID(ID))
		else:
			with open(".\\Data\\Pokemon\\"+getPokeFile(ID)+".json", "w+") as FILE:
				if baseInfo != None:
					json.dump(baseInfo, FILE, indent = 4)