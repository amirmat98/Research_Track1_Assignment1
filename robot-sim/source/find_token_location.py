import global_variables

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
