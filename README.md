# final_assignment
Second assignment of Research Track I course in Robotics Engineering Unige
 Research track 1: Assignment 2 2020/21
Ilenia D’Angelo 4404721
# •	How to run the code:

In order to run the code, follow those steps:
1.	Launch in the terminal the file simulation_mapping.launch with the command: 
```
roslaunch final_assignment simulation_gmapping.launch
```
2.	Using another terminal, launch the file move_base.launch with the command: 
```
roslaunch final_assignment move_base.launch
```
3.	Open a third terminal and launch the file final.launch with the command:
``` 
roslaunch final_assignment.launch
```
# •	Graph of the system:




# •	Description of the content of the package:

The package is composed of 4 nodes, 3 launch files and a folder “world” containing everything necessary to build the environment where our robot moves.
It uses the ros package slam_gmapping and move_base to have an accurate algorithm for localizing and for the path planning of the mobile robot in an unknown enviroment. 
The main node is called “main.py”. It publishes and subscribes to several topic and calls several useful services, in order to control the robot’s behaviour. It is a:
 # o	Publisher for:
move_base:  using the action MoveBaseActionGoal, in order to give a goal to the robot and, in case, cancel it before the end of the execution and hence stop the robot where it is;
cmd_vel: in order to control linear and angular velocity of the robot;
 # o	Subscriber for:
odom: it is used to know the current position of the robot;
 # o	Services:
user_selection: It is the user interface, through that the user can choose one of the four possible behaviours of the robot;
wall_follower_switch: this service allows the robot to follow the external walls of the map;
randsix_pos_server: it is used to extract a random number from 1 to 6, for selecting randomly one of the possible positions on the map

 # o	Parameters:
des_pos_x: A parameter to save the x coordinate of our goal;
des_pos_y: A parameter to save the y coordinate of our goal;
state: A parameter to save the state, the possible behaviour of the robot;

# •	The behaviour of the robot and how to make that
This package implements four possible behaviour of the robot, in a sort of state machine. Through the interface, the user can select:
1.	Give a random position to the robot to reach
2.	Choose one out the six positions proposed to reach
3.	Command the robot to follow external wall
4.	Stop the robot right where it is and restart from the choice menu
To implement the first point, we used the randsix_pos_server, a service to choose a random number, among 1 and 6, corresponding to one of the six saved position. When we extract a position, we save it in the param service, in this way the next node, can get them from it, then we published a goal in the topic move base, with the desired position x and y.
To implement the second point, we used the coordinates saved in the param server, using that the main program gets the desired x and y and publishes them to the move_base topic
To implement the third point, we used the service wall_follower_service, it thanks to the topic scan, can detect the walls and publishing to the cmd_vel can allow the robot to follow walls. During this step the user can choose in any time to stop robot and return to the menu
To implement the fourth point, we used the service user_selection to start a menu where the user can choose one of the four behaviour, we also published in the move_base/cancel topic to cancel the previous goal and publishing in the topic cmd_vel we stop the robot.

# •	System’s limitations and possible improvements
We used a threshold of 0.4 to recognize as reached the goal, our system is not so sharp to do it exactly, due to the odometry. A possible improvement can be using different systems to measure the position and the distance.
In the future we can implement one more status for the robot, changing the planning algorithm from dijkstra to the bug0
A choice for our robot was to not allow to stop the robot until it reaches the goal during behaviours 1 and 2, but a possible choice for the future can be to allow such kind of control, publishing on the move_base/cancel topic
Moreover, in the future a useful tool can be an implementation of a timeout to deal with unreachable targets using a lower threshold or implementing the bug0 planning algorithm.
About the position showed to the user whe the robot reaches the goal, we choose to round it to integer with the ceiling function.This is not the most accurate choice. A possible improvement can be finding a more accurate way to round the position showed, using a different algorithm.
