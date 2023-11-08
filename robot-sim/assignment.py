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


while 1:
    pass
