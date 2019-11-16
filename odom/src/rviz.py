#!/usr/bin/env python

import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import tf
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point

def callback_2(msg_2,pub_2):
	voltage = Point()
	f=msg_2.x
	g=msg_2.y
	h=msg_2.z
	pub_2.publish(voltage)

def callback(msg,pub):	
	hello_str = JointState()
	hello_str.header = Header()
        hello_str.header.stamp = rospy.Time.now()
	hello_str.header.frame_id = "odom"
	hello_str.name = ['prism1','prism2','rot1','rot2','cont']
	a=msg.linear.x
	b=msg.linear.y
	c=msg.linear.z
	d=msg.angular.x
	e=msg.angular.z
	hello_str.position = [a,b,c,d,e]
	hello_str.velocity = [0]
	hello_str.effort = [0]
	print hello_str
	pub.publish(hello_str)

if __name__ == '__main__':
	rospy.init_node('Aspire',anonymous=True)
	print "Node created"
	pub = rospy.Publisher('joint_states', JointState, queue_size=100)
	pub_2 = rospy.Publisher('battery_data', Point, queue_size=100)
	sub_2 = rospy.Subscriber('battery_data', Point, callback_2,pub_2)
	sub = rospy.Subscriber('encoder_data', Twist, callback,pub)   
	print "Subscriber and publisher Made"	
	rospy.spin()
