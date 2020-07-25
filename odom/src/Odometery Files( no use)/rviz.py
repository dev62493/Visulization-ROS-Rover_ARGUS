#!/usr/bin/env python
import rospy
import tf
from sensor_msgs.msg import JointState
from std_msgs.msg import Header,Int32
from geometry_msgs.msg import Twist,Point

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
	a=(msg.linear.z/100)
	b=(msg.linear.y/100)
	c=(msg.angular.z/100)
	d=(msg.angular.x/10)
	e=(msg.linear.x/10)
	hello_str.position = [a,b,c,d,e]
	hello_str.velocity = [0]
	hello_str.effort = [0]
	print hello_str
	pub.publish(hello_str)

if __name__ == '__main__':
	rospy.init_node('Aspire',anonymous=True)
	pub = rospy.Publisher('joint_states', JointState, queue_size=100)
	pub_2 = rospy.Publisher('battery_data', Point, queue_size=100) 	
	sub_2 = rospy.Subscriber('battery_data', Point, callback_2,pub_2)
	sub = rospy.Subscriber('manu_con', Twist, callback,pub)
	rospy.spin()

