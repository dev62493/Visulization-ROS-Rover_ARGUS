#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

t = Twist()

def keys_cb(msg,twist_pub):
	t.linear.x +=msg.axes[2]
	t.linear.y +=-1*msg.axes[5]
	t.linear.z +=msg.axes[6]
	t.angular.x +=msg.axes[0] 
	t.angular.z +=msg.buttons[0]
	print t	
	if msg.buttons[6] & msg.buttons[7]==1:	
		twist_pub.publish(t)
	
if __name__ == '__main__':
	rospy.init_node('manipulator',anonymous=True)
	twist_pub = rospy.Publisher('manu_con', Twist, queue_size=50)
	rospy.Subscriber('joy',Joy,keys_cb,twist_pub)
	rospy.spin()

