import global_variables

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
