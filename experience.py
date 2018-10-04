def _erratic(n):
	if n < 50:
		return (n**3 * (100-n))/50
	elif n >= 50 and n < 68:
		return (n**3 * (150-n))/100
	elif n >= 68 and n < 98:
		return (n**3 * ((1911 - 10 * n)/3))/500
	elif n >= 98 and n <= 100:
		return (n**3 * (160 - n))/100

def _fluct(n):
	if n < 15:
		return n**3 * (((n+1)/3 + 24)/50)
	elif n >= 15 and n < 36:
		return n**3 * ((n+14)/50)
	elif n >= 36 and n < 100:
		return n**3 * (((n/2)+32)/50)

EXP = {
	"Erratic":_erratic,
	"Fast":lambda n : (4*n**3)/5,
	"Medium Fast":lambda n : n**3,
	"Medium Slow":lambda n : (6/5)*n**3 - 15*n**2 + 100*n - 140,
	"Slow":lambda n : (5*n**3)/4,
	"Fluctuating":_fluct,
}

def checkLevel(poke):
	'''
		Check if the pokemon can level up, If it can call the _setStats() and level it up
	'''
	if poke.level == 100:
		## Do nothing if the pokemon is already level 100
		poke.exp = EXP[poke.expgroup](100)
		return None
	## If it can level up, increment its level by 1, update its stats, and return the stat deltas
	if poke.exp >= EXP[poke.expgroup](poke.level+1):
		poke.level += 1
		delta = poke._setStats()
		return delta
	else:
		return None



print(int(EXP["Fluctuating"](50)))