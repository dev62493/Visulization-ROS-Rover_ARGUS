#!/usr/bin/env python 
import rospy 
from visualization_msgs.msg import Marker
import time
import tf
import numpy.matlib 
import numpy as np 

#def take_inputs(num):
#	global data,count
#	data = np.matlib.zeros((num,1))
#	count=0
#	while count!=num :
#		print(" data "+str(count+1)+" :")
#		data[count]=input(" -> ")
#		count+=1
#	return data

if __name__=="__main__":
	rospy.init_node('Markers',anonymous=True)
	marker_pub=rospy.Publisher('goal',Marker,queue_size=100)	
	while(1):
		m=Marker()
		m.header.frame_id = "/odom"
		m.header.stamp = rospy.Time.now()
		m.ns="my_IK_goal"
		m.id=2021
		m.type=m.CUBE
		m.action=m.ADD
		m.pose.position = (3.3,3.3,0)			#Pose
		euler = (0,0,0,)					#Euler_orientation
		q=tf.transformations.quaternion_from_euler(euler[0],euler[1],euler[2])
		m.pose.orientation = q
		m.scale = (0.5,0.5,0.5)				#scale_size
		m.color = (0,1,1,1)				#Color
		m.lifetime = rospy.Duration()
		m.text = "GOAL"
		marker_pub.publish(m)
