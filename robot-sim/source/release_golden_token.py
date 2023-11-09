import global_variables

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
