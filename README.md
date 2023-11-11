# Description
[Università degli studi di Genova](https://unige.it/en/ "University of Genova")

Professor: [Carmine Recchiuto](https://github.com/CarmineD8 "Carmine Recchiuto")

Student: [AmirMahdi Matin](https://github.com/amirmat98 "AmirMahdi Matin")  - 5884715 - Robotics Engineering 

First assignment of Research Track 1 course
-----------------------------------------------------------------------------------------

# Table of Contents
- [Aims of the Research_Track1_First_Assignment](#Aims of the Research_Track1_First_Assignment)
- [Installing and running](#Installing&running)
- [Troubleshooting](#Troubleshooting)
- [Robot_API](#Robot_API)
	- [Motors](##Motors)
	- [Grabber](##Grabber)
	- [Vision](##Vision)
- [How it works](#How it works)
	- [drive](##drive)
	- [turn](##turn)
	- [Gold_find](##Gold_find)
	- [Release_Loc_Find](##Release_Loc_Find)
	- [Gold_grab](##Gold_grab)
	- [Release_Grabbed_Gold](##Release_Grabbed_Gold)
	- [main](##main)
- [Possible improvements](#possible_improvements)



## Aims of the Research_Track1_First_Assignment 

[Student Robotics](https://studentrobotics.org) has designed a straightforward and portable robot simulator. 
Arena has undergone modifications for the first assignment of the Research Track I course. 
The objective of this task is to collect all the golden 'tokens' and place them in close proximity to one another.   The environment, as well as the initial and final arrangement and formation of the 'tokens', are depicted in Figure 1 and Figure 2, respectively. 

<p align="center">
  <img src="https://github.com/PeymanPP5530/research-track-1-assignment1/blob/main/README%20images/initial.png?raw=true" />
</p>


![](sr/First_Config.png)
> Figure1) First configuration of the robot and environment

![](sr/Final_Config.png)
> Figure2)Final configuration of the robot and environment

<p align="center">
  <img src="https://raw.githubusercontent.com/amirmat98/Research_Track1_Assignment1/main/robot-sim/sr/Drawing1.jpg" />
</p>
> Figure3) Flowchart of the algorithm



##Installing&running


The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

**Open a shell and execute the following command:**
```shell
sudo apt-get udpate
sudo apt-get install git
sudo apt-get install python-dev python-pip python-pygame
sudo pip install pypybox2d
```
Now, you should [download](https://github.com/amirmat98/Research_Track1_Assignment1.git "download") a simple robotic simulator with the solution:
```shell
cd
git clone https://github.com/amirmat98/Research_Track1_Assignment1.git
```
Then, move to the simulator folder:
```shell
cd ~/Research_tTrack1_Assignment1/robot-sim
```
Now, run the simulation:
```shell
python2 run.py assignment.py
```
The following simulation will be shown:

<p align="center">
  <img src="https://github.com/PeymanPP5530/research-track-1-assignment1/blob/main/README%20images/initial.png?raw=true" />
</p>



## Troubleshooting

When running `python run.py <file>`, you may be presented with an error: `ImportError: No module named 'robot'`. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:
* Find the location of srtools: `pip show sr.tools`
* Get the location. In my case this was `/usr/local/lib/python2.7/dist-packages`
* Create symlink: `ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/`

When utilizing Docker in lieu of Ubuntu, the simulator will function without encountering any errors. 

##Robot_API

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to that of the [SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```
##How it works

The objective of this task is for the robot to arrange all the golden 'tokens' in close proximity to one another.   To enhance the code's fluidity and comprehensibility, certain functions are defined. 
The initial two parameters are defined as thresholds.   The variables `angle_thresholds` and `distance_threshold` represent the threshold values for angles and distances, respectively.   These factors enable the robot to determine its proximity to the target, allowing it to seize the target when it reaches a suitable distance. 
A list called `gold_token_list` is created with no elements.   The code associated with the relocated token is appended to this list to facilitate the robot's comprehension of which tokens have been relocated, allowing it to disregard them during the search for new tokens to grasp. 

The defined functions for this assignment are as follows:

- drive
- turn
- search_gold_token
- find_token_location
- gold_grab
- release_golden_token
- interface
- main

Each function is described here and then the main code which uses all the functions for the goal is presented and described.

### drive ###

The purpose of the drive(speed, seconds) function is to enable the robot to move in a straight line.   The function receives two inputs: `speed` and `seconds`.   The object will undergo motion at a velocity of `speed` for a period of `seconds`.   The object can move in the forward direction by assigning a positive value to the `speed` parameter, or it can move in the reverse direction by assigning a negative value to the `speed` parameter. 
- 'speed': the desired magnitude of the robot's linear velocity.
- 'second' represents the desired duration of the driving time, measured in seconds. 


```python
def drive(speed, seconds):
	my_robot.motors[0].m0.power = speed
	my_robot.motors[0].m1.power = speed
	time.sleep(seconds)
	my_robot.motors[0].m0.power = 0
	my_robot.motors[0].m1.power = 0
	
```

### turn ###

The turn(speed, seconds) operations provide the robot with the capability to rotate in place.   The task is accomplished by setting the speeds of the right and left motors to be equal, but with opposite signs.   The function receives two inputs: `speed` and `seconds`.   The object will undergo linear motion at a velocity of `speed` for a period of `seconds`. 


```python
def turn(speed, seconds):
	my_robot.motors[0].m0.power = speed
	my_robot.motors[0].m1.power = -speed
	time.sleep(seconds)
	my_robot.motors[0].m0.power = 0
	my_robot.motors[0].m1.power = 0
```
### search_gold_token ###

The `search_gold_token()` function is designed to locate the nearest golden 'token' and provide its distance (`distance`), angle (`rotation_y`), and code (`token_code`) as output, relative to the robot.   Within this function, the robot searches for golden tokens that have not been previously grabed (i.e., their code is absent from the `gold_token_list` collection).   If the function fails to discover a golden 'token', it will return `-1` as the output for all three parameters.   The code is presented below: 


```python
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
```

### find_token_location ###

This function determines the nearest drop point for the acquired golden 'token'.   The drop location refers to the specific position where a 'token' was previously moved and placed adjacent to other golden tokens.   The function yields three outputs: the distance (`distance`), the angle (`rotation_y`), and the code (`token_code`) representing the drop location relative to the robot.   To determine the drop location, the function attempts to locate the code of the nearest golden 'token' that is also present in the `gold_token_list`.   The code for this function is presented below: 


```python
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

```

### gold_grab ###

This function enables the robot to navigate towards the nearest golden 'token' and halts once it reaches a proximity close enough to the target 'token'.    The `angle_threshold` and `distance_threshold` parameters are utilized to determine the conditions under which the robot achieves its target.   If the robot is inside the specified distance threshold from the destination (`distance <= distance_threshold`), the function terminates and remains in a state of readiness for additional instructions from the user.   If the distance exceeds the `distance_threshold` and the rotation_y value falls within the range of `-angle_threshold` to `angle_threshold`.   The robot advances in order to reach the 'token'.   If the scenario does not fall into any of these two categories, the robot should turn right or left in order to minimize the angle difference with the target, and then proceed to move towards it.


```python
def gold_grab():

	token_flag = 1			
	while token_flag:
	
	    distance, rotation_y ,token_code = search_gold_token()  # we look for gold tokens
	    
	    if distance <= distance_threshold: # if the robot is close enough to the token the while loop is stopped so it can grab the token 
		interface("goldtoken") 
		token_flag = 0
		
	    elif -angle_threshold<= rotation_y <= angle_threshold: # if the robot is well aligned with the token but not close, we go forward to reach it
		interface("forward") 
		drive(my_speed, my_time)
		
	    elif rotation_y < -angle_threshold: # if the robot is not well aligned with the token, we move it on the left or on the right until it's aligned
		interface("left") 
		turn(-2, 0.5)
		
	    elif rotation_y > angle_threshold:
		interface("right") 
		turn(+2, 0.5)

```

### release_golden_token ###

The `release_golden_token()` method facilitates the robot's movement towards the designated drop spot for the 'token' it has acquired.   Upon reaching the designated place, the function terminates and remains in a state of readiness for the user's commands.   The technique and rationale behind this function are identical to that of `gold_grab`.   The sole distinction is in the utilization of the function `find_token_location()` to determine the drop location.   The robot releases the 'token' after it reaches a distance that is slightly greater than the distance threshold.   The purpose of adding this number to `distance_threshold` is to prevent the robot and the grabbed 'token' from colliding with the 'token' that is already at the target position. 


```python
def release_golden_token():

	flag = 1			
	while flag:
	    distance , rotation_y , token_code = find_token_location()  # we look for closest gold token which was droped previously
	    
	    if distance < distance_threshold + 0.2:  # if the robot is close enough to the drop location the while loop is stopped so the robot can release the box
	    # The value 0.2 is defined so that the robot releases the box it holds a small distance away from the target box
		interface("find_location") 	 
		flag = 0
	    elif -angle_threshold <= rotation_y <= angle_threshold: # if the robot is well aligned with the drop location, we go forward
		interface("forward")
		drive(my_speed, 0.5)
	    elif rotation_y < -angle_threshold: # if the robot is not well aligned with the drop location, we move it on the left or on the right
		interface("left") 
		turn(-2, 0.5)
	    elif rotation_y > angle_threshold:
		interface("right")
		turn(+2, 0.5)
```
### main ###

With the functions outlined in the preceding part, we can now explain the primary code responsible for the robot's ability to grasp and move all the golden tokens, ultimately gathering them in a single spot.
Initially, the nearest golden 'token' is located.   This 'token' will be regarded as the initial reference 'token'.   As a result, the next 'token' will be discarded at the same location as this reference 'token' is discarded.   However, the reference position may not apply to all subsequent tokens, since the robot endeavors to locate the nearest drop-off point. 
In certain instances, the robot may encounter a situation where it is unable to detect a golden 'token' within its vicinity (distance = -1).   In this scenario, the robot continuously rotates and scans its surroundings until it locates a valuable 'token' made of gold.   The code for this part is explained in the following manner: 


```python

	distance , rotation_y , token_code = search_gold_token() # The robot tries to find the closest golden token
	while distance == -1:  # In case the robot can not find a golden token, it keeps turning and surching until it finds one 
		interface("no_gold_token")
		turn(5,2)
		distance , rotation_y , token_code = search_gold_token()
```
Once the 'token' is detected, the robot proceeds towards it using the `gold_grab()` function and seizes the 'token' by employing the `my_robot.grab()` method.   The 'token' is deposited in a randomly selected location.   Once the 'token' is discarded, its code is appended to the `gold_token_list`.   The robot retreats and maneuvers to evade collision with the fallen 'token': 


```python
	# The robot moves toward the closest golden token and grabs it
	gold_grab()  
	my_robot.grab()
	interface("grab")
	
	# The robot turns and moves forward to a random drop location and releases the token
	turn(-10,1.1)
	interface("deliver")
	drive(10 , 19)
	my_robot.release()
	interface("release")
	
	# The robot moves backward a little to avoid hitting the token it dropped and turns 360 degrees to start looking for a new token
	drive(-my_speed , 2)
	turn(30,2)
	
	#The code of the token that was just dropped is added to the list so that the robot looks for other tokens in the next steps

	gold_token_list.append(token_code)

```
Subsequently, a while loop is established to ensure the robot reaches all the remaining tokens and consolidates them in close proximity.   Following the dropping of each 'token', its code is appended to the `gold_token_list` and a new search commences. 

```python

	# The robot starts a search, grab, drop algorithm and keeps doing it until all tokens are next to each other (gold_token_list has the code of all tokens and its
	# length is 6)
	while len(gold_token_list)< 6:
		
		# The robot moves toward the closest golden token and grabs it
		distance , rotation_y , token_code = search_gold_token()
		while distance == -1:
			interface("no_gold_token")
			turn(5,2)
			distance , rotation_y , token_code = search_gold_token()
		gold_grab()
		my_robot.grab()
		interface("grab")
		
		# The robot finds a drop location for the token it's holding
		new_distance , new_rotation_y , new_token_code = find_token_location()
		
		# The robot keeps turning until it finds the group of tokens that were put together before and bribgs the token there
		# for the first round of the loop it brings the box to the reference box which was initially moved
		while new_distance == -1:
			interface("find_destination")
			turn(5,2)
			new_distance , new_rotation_y , new_token_code = find_token_location()
			
		release_golden_token()
		my_robot.release()
		interface("release")
		drive(-my_speed,2)
		turn(30,2)
		
		# The code of the dropped box is added to the List before starting a new search and grap 
		gold_token_list.append(token_code)

```
[sr-api]: https://studentrobotics.org/docs/programming/sr/

## Possible improvements

