#!/usr/bin/env python

import rospy,devlib
import numpy as np
from sensor_msgs.msg import Joy
from std_msgs.msg import Float32MultiArray,MultiArrayDimension,Float32

f=Float32MultiArray()
flt=Float32()

vx=0
omega=0
x=input("Enter goal co-ordinates: ")
goal_x = x[0]
goal_y = x[1]
goal_z = 0
kv=0.003
kp=0.1
kd = 0.001
kth=0.001	

	
def pri_cb(variable):
	global v,omega,goal_x,goal_y,goal_z,kp,kth,kv,kd	
	(current_x,current_y,current_z,c_yaw) = variable.data
	
	error_x = goal_x - current_x
	error_y = goal_y - current_y
	error_z = goal_z - current_z
	
	d = devlib.distance(goal_x,goal_y,current_x,current_y)
	goal_yaw = devlib.calc_yaw(error_x,error_y)
	goal_deg = devlib.cvt2deg(goal_yaw)		
	c_deg = devlib.cvt2deg_x2x(c_yaw)	
	r_theta = goal_deg - c_deg 	
	r_theta = devlib.pid(kp,kd,0,r_theta)
	if (abs(d)>=0.3 and abs(r_theta) < 1) :
		omega=0		
		v = -kv*d
		print ("Speed: ",v)
	elif abs(r_theta) >= 1:		
		v=0
		omega = r_theta*kth
		print ("Angle error: ",r_theta)	
	else :
		print ("Goal Reached at " + str(goal_x) +","+ str(goal_y))				
		goal_deg = c_deg
		v,omega=0,0
	
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

rospy.init_node('Rover_control',anonymous=True)
rate = rospy.Rate(0.00125)	

while not rospy.is_shutdown():
	print "Starting Autonomous localisation"
	point_sub=rospy.Subscriber('current_coordinates',Float32MultiArray,pri_cb)
	robot_state_pub=rospy.Publisher('joint_data',Float32MultiArray,queue_size=100)
	angle_pub=rospy.Publisher('theta2',Float32,queue_size=100)
	rate.sleep()	
