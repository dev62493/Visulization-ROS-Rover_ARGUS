import devlib
from devlib import getkey as gk

global forward,reverse,left,right

def scandir():
	[forward,reverse,left,right] = [0,0,0,0]
	button = gk(0.3)
	if button == "w":
		forward = 1
	elif button == "s":
		reverse = 1
	elif button == "a":
		left = 1
	elif button == "d":
		right = 1
	else:
		[forward,reverse,left,right] = [0,0,0,0]
	command = [forward,reverse,left,right]
	return command

if __name__=="__main__":
	pressed = gk(0.1)
	while (pressed != "c"):
		dirarray = scandir()
		print dirarray
		pressed = gk(0.1)
