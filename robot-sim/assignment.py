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
		


while 1:
    pass
