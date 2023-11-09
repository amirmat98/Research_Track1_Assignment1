import global_variables

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
		
