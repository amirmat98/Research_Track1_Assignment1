import os # for clearing the screen

# interface function
# this function prints the robot's interface
# it takes a command as input and prints the corresponding message
def interface(command):
	os.system('clear')
	print('###################################################################')
	print("##                         Robot's interface                     ##")
	print('###################################################################\n\n')

	if command is "start":
		print('Lets put sliver tokens next to the gold tokens')
		time.sleep(2)

	if command is "notoken":
		print('Ops there is no token in my range!!!')

	elif command is "goldtoken":
		print('I found a gold token')

	elif command is "nogoldtoken":
		print('ther is no gold token in my range!!!')

	elif command is "deliver":
		print('I am delivering the silver token next to the gold token')

	elif command is "silvertoken":
		print('I found a silver token')

	elif command is "nosilvertoken":
		print('Ops there is no silver token in my range!!!')

	elif command is "grab":
		print('I grabbed the silver token \nLets deliver it to a gold token')

	elif command is "release":
		print('Yes.. I put the silver token next to the gold token')

	elif command is "problem":
		print('Ops there is a problem, I cannot grab the token!!!')

	elif command is "left":
		print("I am turning left a bit")

	elif command is "right":
		print("I am turning right a bit")

	elif command is "finish":
		print("I delivered silver all tokens successfully!!!")



