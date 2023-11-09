#import libraries
from __future__ import print_function # for print()
import time # for time.sleep()
from sr.robot import * # for robot object

from source import drive
from source import find_token_location
from source import global_variables
from source import gold_grab
from source import interface
from source import release_golden_token
from source import search_golden_token
from source import turn
#from source import * # for all functions

my_robot = Robot() # robot object

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
		
