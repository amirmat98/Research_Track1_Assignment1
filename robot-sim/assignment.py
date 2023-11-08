"""
Descriptions
"""

#import libraries
from __future__ import print_function # for print()
import time # for time.sleep()
from sr.robot import * # for robot object


# define global variables
my_robot = Robot() # robot object
my_time = 0.5 # turn and drive time
my_speed = 25 # turn and drive speed
angle_threshold = 2.0 # angle threshold
distance_threshold = 0.4 # distance threshold
#silver_token_list = [] # array to store the code of collected silver tokens
gold_token_list = [] # array to store the code of gold tokeens


# drive the robot forward/backwards
def drive(speed, seconds):
	my_robot.motors[0].m0.power = speed
	my_robot.motors[0].m1.power = speed
	time.sleep(seconds)
	my_robot.motors[0].m0.power = 0
	my_robot.motors[0].m1.power = 0
	
	
# turn the robot left/right
def turn(speed, seconds):
	my_robot.motors[0].m0.power = speed
	my_robot.motors[0].m1.power = -speed
	time.sleep(seconds)
	my_robot.motors[0].m0.power = 0
	my_robot.motors[0].m1.power = 0

#This Function to find the closest Golden Box with no elements in the list "gold_token_list"
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
	
		return -1 , -1 ,token_code
	
	else:
		return distance, rotation_y ,token_code
		

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
		

#This Function move towards the closet token nearby
def Gold_grab():

	token_flag = 1			
	while token_flag:
	
	    distance, rotation_y ,token_code = search_gold_token()  # we look for gold tokens
	    
	    if distance <= distance_threshold: # if the robot is close enough to the token the while loop is stopped so it can grab the token 
		print("Found a Gold one!")	 
		token_flag = 0
		
	    elif -angle_threshold<= rotation_y <= a_th: # if the robot is well aligned with the token but not close, we go forward to reach it
		print("Going forward!.")
		drive(10, 0.5)
		
	    elif rotation_y < -angle_threshold: # if the robot is not well aligned with the token, we move it on the left or on the right until it's aligned
		print("Left a bit...")
		turn(-2, 0.5)
		
	    elif rotation_y > angle_threshold:
		print("Right a bit...")
		turn(+2, 0.5)
		
		
while 1:
    pass
