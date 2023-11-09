import global_variables

# drive the robot forward/backwards
def drive(speed, seconds):
	my_robot.motors[0].m0.power = speed
	my_robot.motors[0].m1.power = speed
	time.sleep(seconds)
	my_robot.motors[0].m0.power = 0
	my_robot.motors[0].m1.power = 0

