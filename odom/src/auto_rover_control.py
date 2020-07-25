#!/usr/bin/env python

import rospy,devlib
import numpy as np
from sensor_msgs.msg import Joy
from std_msgs.msg import Float32MultiArray,MultiArrayDimension,Float32

f=Float32MultiArray()
flt=Float32()
vx=0
omega=0
goal_x = 5.3
goal_y = -2.4
goal_z = 0
	
def pri_cb(variable):
	global v,omega,goal_x,goal_y,goal_z	
	kp=0.00990
	kpth=0.00005
	crit_x=0.1
	crit_y=0.1
	crit_theta = 0

	(current_x,current_y,current_z,c_yaw) = variable.data
	
	error_x = goal_x - current_x
	error_y = goal_y - current_y
	error_z = goal_z - current_z
	
	d = devlib.distance(goal_x,goal_y,current_x,current_y)
	goal_yaw = devlib.calc_yaw(error_x,error_y)
	goal_deg = devlib.cvt2deg(goal_yaw)		
	c_deg = devlib.cvt2deg_x2x(c_yaw)	
	
	r_theta = goal_deg - c_deg 	
	theta = devlib.pid(0.35,0,1.25,r_theta)
	
	if (abs(error_x) >= abs(crit_x)) and (abs(error_y) >= abs(crit_y)) and (abs(theta) == crit_theta) :
		v = -kp*d
		print "Aquiring Velocity"
		print goal_x,current_x,v
	elif theta > crit_theta or theta < -crit_theta:		
		v=0
		omega = r_theta*kpth
		print r_theta	
	else:
		print ("Goal Reached" + str(goal_x) +"::"+ str(goal_y))				
		goal_deg = c_deg
	
	f.layout.data_offset = 0 
	f.layout.dim = [MultiArrayDimension()]
	f.layout.dim[0].label = "Rover_state_data"
	f.layout.dim[0].size = 9
	f.layout.dim[0].stride = 9
	f.data=[0,0,0,0,0,v,omega,0.08]	
	if r_theta < 5 or r_theta > -5:	
		flt.data = r_theta
	else: 
		flt.data = 0
	angle_pub.publish(flt)
	robot_state_pub.publish(f)
	

if __name__=='__main__':
	rospy.init_node('Rover_control',anonymous=True)
	point_sub=rospy.Subscriber('current_coordinates',Float32MultiArray,pri_cb)
	robot_state_pub=rospy.Publisher('joint_data',Float32MultiArray,queue_size=100)
	angle_pub=rospy.Publisher('theta2',Float32,queue_size=100)
	rospy.spin()
