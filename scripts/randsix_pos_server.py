#! /usr/bin/env python

# Ilenia D'Angelo 4404721 Assignment 2

#it is the server service used as generator of random integer number in the interval [1,6], each one corresponds to a pair of coordinates (x,y)
import rospy
import math
import random
from std_srvs.srv import *

#service callback
#This callback is of the type empty, it is just a sort of signal
# @param des_pos_x and des_pos_y are set in the parameter service depending on the value of the generated random number
def set_rand_pos (req):

	randpos = random.randint (1,6)
	print("The random position is = " + str(randpos))
	if randpos == 1:
		x = -4
		y =-3

	elif randpos == 2:
		x = -4
		y = 2

	elif randpos == 3:
		x = -4
		y = 7

	elif randpos == 4:
		x = 5
		y = -7

	elif randpos == 5:
		x = 5
		y = -3

	elif randpos == 6:
		x = 5
		y = 1

	rospy.set_param("des_pos_x", x)
	rospy.set_param("des_pos_y", y)
	print("Hi! We are reaching the random position: x = " + str(x) + ", y = " + str(y))
	return []

def main():
	#initialization of the node randsix_pos_server
	rospy.init_node ('randsix_pos_server')

	srv = rospy.Service('randsix_pos_server', Empty, set_rand_pos)
	rate = rospy.Rate(20)
	while not rospy.is_shutdown():
		rate.sleep()

if __name__ == '__main__':
	main()
