#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

t = Twist()

def keys_cb(msg,twist_pub):
	if msg.buttons[4] == 1:
		t.linear.x=msg.axes[1]*270
		t.angular.z=0
	elif msg.buttons[5] == 1:
		t.linear.x=0
		t.angular.z=msg.axes[3]*270	
	else:
		t.linear.x=msg.axes[1]*135
		t.angular.z=msg.axes[3]*135
	

	
	twist_pub.publish(t)

if __name__ == '__main__':
	rospy.init_node('joystick')
	twist_pub = rospy.Publisher('cmd_vel', Twist, queue_size=50)
	rospy.Subscriber('joy',Joy,keys_cb,twist_pub)
	rospy.spin()

