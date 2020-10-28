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
			(t1,r1) = listener.lookupTransform('/mainlead', '/base_link', rospy.Time(0))
			(t2,r2) = listener.lookupTransform('/horilead', '/mainlead', rospy.Time(0))
			(t3,r3) = listener.lookupTransform('/rotational1', '/horilead', rospy.Time(0))
			(t4,r4) = listener.lookupTransform('/rotational2', '/rotational1', rospy.Time(0))

			base = tf.transformations.euler_from_quaternion(r)
			rot1 = tf.transformations.euler_from_quaternion(r3)			
			yaw=base[2]
			rot_yaw	=rot1[2]
			leadscrew_length = -t1[2]
			[rotated_x,rotated_y,rotated_z]=t
			
			unchanged_base_x = -1*(rotated_x*cos(yaw) + rotated_y*sin(yaw))
			unchanged_base_y = rotated_x*sin(yaw) - rotated_y*cos(yaw)			
			unchanged_base_z = rotated_z		

			#Due to roataional matrices hardcoded values are used instead of t3[0] and t4[0]

			rot1_x = unchanged_base_x - ( t2[0] + 0.30136 ) * cos(yaw)  	
			rot1_y = unchanged_base_y + ( t2[0] + 0.30136 ) * sin(yaw) 
			rot1_z = unchanged_base_z + leadscrew_length - t2[2] - t3[2] 			
			
			curr_x = rot1_x + 0.223839193 * cos(rot_yaw)
			curr_y = rot1_y - 0.223839193 * sin(rot_yaw)
			curr_z = rot1_z - 0.1549 
			global curr_co			
			curr_co=[unchanged_base_x,unchanged_base_y,unchanged_base_z,yaw]
			print curr_co						
		except:
			continue  
		f.data=curr_co
		pub.publish(f)
           
