#!/usr/bin/env python  
import roslib
import rospy
import math
import tf
import time

from math import sin, cos, pi  
from std_msgs.msg import Float32MultiArray,MultiArrayDimension
f=Float32MultiArray()


if __name__ == '__main__':
	rospy.init_node('Gripper_End_point',anonymous=True)
	f.layout.data_offset = 0 
	f.layout.dim = [MultiArrayDimension()]
	f.layout.dim[0].label = "End_co-ordinates"
	f.layout.dim[0].size = 5
	f.layout.dim[0].stride = 5
	pub = rospy.Publisher('current_coordinates',Float32MultiArray,queue_size=100)        
	listener = tf.TransformListener()
	while not rospy.is_shutdown():
		try:       			
			(t,r)   = listener.lookupTransform('/base_link', '/odom', rospy.Time(0))
			base = tf.transformations.euler_from_quaternion(r)	
			yaw=base[2]
			[rotated_x,rotated_y,rotated_z]=t
			original_base_x = -1*(rotated_x*cos(yaw) + rotated_y*sin(yaw))
			original_base_y = rotated_x*sin(yaw) - rotated_y*cos(yaw)	
			original_base_z = rotated_z				
			global current			
			current=[original_base_x,original_base_y,original_base_z,yaw]
			print current						
		except:
			print "error"
			continue  
		f.data=current
		pub.publish(f)
           
