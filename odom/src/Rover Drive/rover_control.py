#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Float32MultiArray,MultiArrayDimension

f=Float32MultiArray()

def data_transfer(msg):
	
	f.layout.data_offset = 0 
	f.layout.dim = [MultiArrayDimension()]
	f.layout.dim[0].label = "Joint_state_data"
	f.layout.dim[0].size = 8
	f.layout.dim[0].stride = 8
	
	if msg.buttons[4] and msg.buttons[5] == 1:
		a=msg.buttons[0]*msg.axes[5]
		b=msg.buttons[1]*msg.axes[5]
		c=msg.buttons[2]*msg.axes[5]
		d=msg.buttons[3]*msg.axes[5]
		e=msg.axes[2]*msg.axes[5]			
		f.data=[a,b,c,d,e,0,0,0.02]		

	else:
		v1=msg.axes[1]*255*-1
		v2=msg.axes[3]*255
		f.data=[0,0,0,0,0,v1,v2,0.00008]
	robot_state_pub.publish(f)

if __name__=='__main__':
	rospy.init_node('Rover_control',anonymous=True)
	joy_sub=rospy.Subscriber('joy',Joy,data_transfer)
	robot_state_pub=rospy.Publisher('joint_data',Float32MultiArray,queue_size=100)
	rospy.spin()
