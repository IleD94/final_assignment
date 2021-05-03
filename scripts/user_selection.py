#! /usr/bin/env python

# Ilenia D'Angelo 4404721 Assignment 2

#@package user_selection
#it is a service server used to interact with the user for the selection of the state of the robot, this state is stored in the parameter server. In the state==2 the user can choose the goal too
 
import rospy
from std_srvs.srv import *

#function used in the callback to allow the user to choose one of the six possible positions
def set_new_user_pos():
	print("Please, digit a number to choose one of the six possible positions (x,y) 1:(-4,-3) 2:(-4,2) 3:(-4,7) 4:(5,-7) 5:(5,-3) 6:(5,1)")
	#boolean variable to control that the user choose one of the possible combination and not anything else	
	posnotok = True
	while posnotok:
		userpos = int(raw_input('digit your choice:'))
		posnotok = False
		if userpos == 1:
			x = -4
			y = -3
		elif userpos == 2:
			x = -4
			y = 2
		elif userpos == 3:
			x = -4
			y = 7
		elif userpos == 4:
			x = 5
			y = -7
		elif userpos == 5:
			x = 5
			y = -3
		elif userpos == 6:
			x = 5
			y = 1
		else:
			print ("Your choice is not valid")
			posnotok = True
			
	#@param des_pos_x is set in the parameter server
	rospy.set_param("des_pos_x", x)
	#@param des_pos_y is set in the parameter server
	rospy.set_param("des_pos_y", y)
	print("Thanks! Let's reach the next position")
	return []

#service callback
#this callback is of type Empty, it does not have a return value, but print on the screen some messages to interact with the user and takes inputs from them
def set_option (req):
	#boolean variable to deal with possible unvalid status choice of the user
	allright = False
	while not allright:
		print("Please, choose an option. 1: Random target position, 2: user target position, 3: follow the external wall, 4: stop where you are")
		status = int(raw_input('your option:'))
		if status == 1 or status == 2 or status == 3 or status == 4:
			allright = True
		else:
			print ('Your choice is not valid. Please insert an int value from 1 to 4')
	#set in the parameter server the @param state
	rospy.set_param ("state", status)
	print("Your choice: "+ str(status))
	if status == 2:
		#call of the function set_new_user_pos to set a user's choice position
		set_new_user_pos()
		x = rospy.get_param("des_pos_x")
		y = rospy.get_param("des_pos_y")
		print("Hi! We are reaching the chosen position: x = " + str(x) + ", y = " + str(y))
	return []

def main():
	global status
	#initialization of the node user_selection
	rospy.init_node('user_selection')
	#initialization of the service user_selection of type empty
	srv = rospy.Service ('user_selection', Empty, set_option)
	
	rate = rospy.Rate(20)
	while not rospy.is_shutdown():
		rate.sleep()

if __name__ == '__main__':
	main()
