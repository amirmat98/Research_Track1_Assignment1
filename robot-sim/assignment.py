"""
Descriptions
"""

#--------------------------------------------------------------------------

#import libraries
from __future__ import print_function # for print()
import os # for clearing the screen
import time # for time.sleep()
from sr.robot import * # for robot object

#--------------------------------------------------------------------------

# define global variables
my_robot = Robot()
my_time = 0.5 # turn and drive time
my_speed = 25 # turn and drive speed
angle_threshold = 2.0 # angle threshold
distance_threshold = 0.4 # distance threshold
gold_token_list = [] # array to store the code of gold tokeens

#--------------------------------------------------------------------------

# drive the robot forward/backwards
def drive(speed, seconds):
	my_robot.motors[0].m0.power = speed
	my_robot.motors[0].m1.power = speed
	time.sleep(seconds)
	my_robot.motors[0].m0.power = 0
	my_robot.motors[0].m1.power = 0

#--------------------------------------------------------------------------

# turn the robot left/right
def turn(speed, seconds):
	my_robot.motors[0].m0.power = speed
	my_robot.motors[0].m1.power = -speed
	time.sleep(seconds)
	my_robot.motors[0].m0.power = 0
	my_robot.motors[0].m1.power = 0

#--------------------------------------------------------------------------

#This Function find the closest token nearby (among the tokens that were previously grabbed and put next to each other)
def find_token_location():
	distance = 100
	rotation_y = 0
	token_code = -1
	
	for token in my_robot.see():
		if token.dist<distance and token.info.marker_type == MARKER_TOKEN_GOLD and token.info.code in gold_token_list:
			distance = token.dist
			rotation_y = token.rot_y
			token_code = token.info.code
			
	if distance == 100:
	
		return -1 , -1 ,-1
	
	else:
		return distance, rotation_y ,token_code



#--------------------------------------------------------------------------

#This Function move towards the closet token nearby
def gold_grab():

	token_flag = 1			
	while token_flag:
	
	    distance, rotation_y ,token_code = search_gold_token()  # we look for gold tokens
	    
	    if distance <= distance_threshold: # if the robot is close enough to the token the while loop is stopped so it can grab the token 
		print("Found a Gold one!")	 
		token_flag = 0
		
	    elif -angle_threshold<= rotation_y <= angle_threshold: # if the robot is well aligned with the token but not close, we go forward to reach it
		print("Going forward!.")
		drive(10, 0.5)
		
	    elif rotation_y < -angle_threshold: # if the robot is not well aligned with the token, we move it on the left or on the right until it's aligned
		print("Left a bit...")
		turn(-2, 0.5)
		
	    elif rotation_y > angle_threshold:
		print("Right a bit...")
		turn(+2, 0.5)


#--------------------------------------------------------------------------

#This function to move towards the closest drop location ( The closest token which was previously moved and relocated)	
def release_golden_token():

	flag = 1			
	while flag:
	    distance , rotation_y , token_code = find_token_location()  # we look for closest gold token which was droped previously
	    
	    if distance < distance_threshold + 0.2:  # if the robot is close enough to the drop location the while loop is stopped so the robot can release the box
	    # The value 0.2 is defined so that the robot releases the box it holds a small distance away from the target box
		print("Found a drop location!")	 
		flag = 0
	    elif -angle_threshold <= rotation_y <= angle_threshold: # if the robot is well aligned with the drop location, we go forward
		print("Going forward!.")
		drive(10, 0.5)
	    elif rotation_y < -angle_threshold: # if the robot is not well aligned with the drop location, we move it on the left or on the right
		print("Left a bit...")
		turn(-2, 0.5)
	    elif rotation_y > angle_threshold:
		print("Right a bit...")
		turn(+2, 0.5)	



#--------------------------------------------------------------------------

#This Function to find the closest Golden token with no elements in the list "gold_token_list"
# return: distance, angle and code of the nearest token
def search_gold_token():
	distance = 100
	rotation_y = 0
	token_code = -1
	
	for token in my_robot.see():
		# if the token is unmarked and in the range of the robot, update the distance, angle and code of token
		if token.dist<distance and token.info.marker_type == MARKER_TOKEN_GOLD and token.info.code not in gold_token_list:   
			distance = token.dist
			token_code = token.info.code
			rotation_y = token.rot_y
		
			
	if distance >= 100:
	
		return -1 , -1 , -1
	
	else:
		return distance, rotation_y ,token_code
		
#--------------------------------------------------------------------------

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


#--------------------------------------------------------------------------


def main():

	distance , rotation_y , token_code = search_gold_token() # The robot tries to find the closest golden token
	while distance == -1:  # In case the robot can not find a golden token, it keeps turning and surching until it finds one 
		print("I have to search more for a gold box!!")
		turn(5,2)
		distance , rotation_y , token_code = search_gold_token()
	
	# The robot moves toward the closest golden token and grabs it
	gold_grab()  
	my_robot.grab()
	print("Just grabbed it")
	
	# The robot turns and moves forward to a random drop location and releases the token
	turn(-10,1.1)
	drive(10 , 19)
	my_robot.release()
	print("Package Delivered")
	
	# The robot moves backward a little to avoid hitting the token it dropped and turns 360 degrees to start looking for a new token
	drive(-10 , 2)
	turn(30,2)
	
	#The code of the token that was just dropped is added to the list so that the robot looks for other tokens in the next steps

	gold_token_list.append(token_code)
	
	# The robot starts a search, grab, drop algorithm and keeps doing it until all tokens are next to each other (gold_token_list has the code of all tokens and its
	# length is 6)
	while len(gold_token_list)< 6:
		
		# The robot moves toward the closest golden token and grabs it
		distance , rotation_y , token_code = search_gold_token()
		while distance == -1:
			print("I have to search more for a gold box!!")
			turn(5,2)
			distance , rotation_y , token_code = search_gold_token()
		gold_grab()
		my_robot.grab()
		print("Just grabbed it")
		
		# The robot finds a drop location for the token it's holding
		new_distance , new_rotation_y , new_token_code = find_token_location()
		
		# The robot keeps turning until it finds the group of tokens that were put together before and bribgs the token there
		# for the first round of the loop it brings the box to the reference box which was initially moved
		while new_distance == -1:
			print("I have to search more for a destination!!")
			turn(5,2)
			new_distance , new_rotation_y , new_token_code = find_token_location()
			
		release_golden_token()
		my_robot.release()
		print("Package Delivered")
		drive(-10,2)
		turn(30,2)
		
		# The code of the dropped box is added to the List before starting a new search and grap 
		gold_token_list.append(token_code)
		
#--------------------------------------------------------------------------

main()

