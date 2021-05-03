#! /usr/bin/env python
#Ilenia D'Angelo 4404721
#@package main
#The main node, it starts all the other services to have different robot's behaviours
import rospy
import time
# import ros message
from geometry_msgs.msg import Point
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from tf import transformations
# import ros service
from std_srvs.srv import *
from geometry_msgs.msg import Twist
from move_base_msgs.msg import MoveBaseActionGoal
from actionlib_msgs.msg import GoalID
import actionlib
import math

#global variables
pub = None
setgoal_pub = None
cancel_pub = None

srv_client_wall_follower_ = None
srv_client_user_interface_ = None
srv_client_randsix_pos_server = None

position_ = Point()
desired_position_ = Point()
desired_position_.x = None
desired_position_.y = None
desired_position_.z = 0

#Several states for the robots
state_desc_ = ['Go to a random point', 'Go to a chosen point', 'wall following', 'target reached']

# callback funtion for the subscription to odom with the aim to receive the position of the robot
# @var position_ is used to store the current position of the robot
def clbk_odom(msg):
	global position_

    	# position
	position_ = msg.pose.pose.position

# functions

#the funtion set_goal sets a new goal for the robot, it changes the values of des_pos_x and des_pos_y in the parameter server
def set_goal ():
	
	global setgoal_pub
	actiongoal = MoveBaseActionGoal ()
	actiongoal.goal.target_pose.header.frame_id = "map"
	actiongoal.goal.target_pose.pose.orientation.w = 1
	actiongoal.goal.target_pose.pose.position.x = rospy.get_param("des_pos_x")
	actiongoal.goal.target_pose.pose.position.y = rospy.get_param("des_pos_y")
	setgoal_pub.publish(actiongoal)
	return []

#change_state function implements a state machine,each state corresponds to a differet robot's behaviour
# @param state_ get the current state of the machine stored in the parameter server
def change_state():
	global state_, state_desc_, position_
	global srv_client_wall_follower_, srv_client_randsix_pos_server, set_goal,cancel_pub
	state_= rospy.get_param('state')
	log = "state changed: %s" % state_desc_[state_-1] 
	rospy.loginfo(log)
    	if state_ == 4: #stop and restart from the user interface
		time.sleep(1)
		#cancel the previous goal and stop
		cancel_msg = GoalID()
		cancel_pub.publish (cancel_msg)
		resp = srv_client_wall_follower_(False)
		twist_msg = Twist()
		twist_msg.linear.x = 0
		twist_msg.linear.y = 0
		twist_msg.angular.z = 0
		pub.publish(twist_msg)
		#round to the ceiling the actual position of the robot
		intposx = int(math.ceil(position_.x))
		intposy = int(math.ceil(position_.y))
		print 'Your current position is (x,y):(',intposx,',',intposy,')' 
		resp= srv_client_user_interface_()
		state_= rospy.get_param('state')

	if state_ == 1: #random goal
		resp = srv_client_randsix_pos_server ()
		resp = srv_client_wall_follower_(False)
		resp = set_goal ()
	if state_ == 2: #user goal
		resp = srv_client_wall_follower_(False)
   		resp = set_goal ()
	if state_ == 3: #wall follow	
		resp = srv_client_wall_follower_(True)
		

	
def main():
	time.sleep(2)
	global  position_, desired_position_, state_
	global srv_client_wall_follower_, srv_client_user_interface_, pub, setgoal_pub, srv_client_randsix_pos_server,cancel_pub
	
	#initialization of the main node
	rospy.init_node('main')
	#initialization of the subscriber to the topic odom to receive the positon
	sub_odom = rospy.Subscriber('odom', Odometry, clbk_odom)
	#initialization of the publisher to the topic cmd_vel to set the velocity
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
	#initialization of the publisher to the topic move_base/goal, it is an action to set the goal
	setgoal_pub = rospy.Publisher('move_base/goal', MoveBaseActionGoal, queue_size=1)
	#initialization of the publisher to the topic move_base/cancel, it is an action to cancel the goal
	cancel_pub = rospy.Publisher ("/move_base/cancel", GoalID, queue_size=1)
	#initialization of the service wall_follower_switch
	srv_client_wall_follower_ = rospy.ServiceProxy('/wall_follower_switch', SetBool)
	#initialization of the service user selection, it is the user interface where there is the menu
	srv_client_user_interface_ = rospy.ServiceProxy('/user_selection', Empty)
	#initialization of the service randsix_pos_server to have a random position 
	srv_client_randsix_pos_server = rospy.ServiceProxy ('/randsix_pos_server', Empty)
	
	
	change_state()
	rate = rospy.Rate(20)
	while not rospy.is_shutdown():
		state_ = rospy.get_param ("state")
		desired_position_.x = rospy.get_param('des_pos_x')
		desired_position_.y = rospy.get_param('des_pos_y')
		if state_ == 1 or state_ == 2:
			# err_pos is the error in reaching the goal, so the distance from the goal
			err_pos = math.sqrt(pow(desired_position_.y - position_.y, 2) + pow(desired_position_.x - position_.x, 2))
			print ("We are almost there! Our distance from the goal is:")			
			print err_pos
			if(err_pos < 0.4): #threshold under which we have reached the goal
				print ('You reach your goal!')
				rospy.set_param ("state", 4)
				#return to the state 4
				change_state()
		if state_ == 3:
			# stopBotton is a input from the user to stop the robot in state 3 and return in state 4
			stopBotton = raw_input ('Please, when you want to stop the wall following behaviour of the robot press s: ')
			if stopBotton == "s":
				rospy.set_param ("state", 4)
				change_state()
		if state_ == 4: 
			change_state()

		rate.sleep()

if __name__ == "__main__":
    main()
