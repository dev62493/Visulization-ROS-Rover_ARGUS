#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
import time 
t = Twist()
key=0
curr=0
curr1=0
p=0.1
#current_time=rospy.Time.now()
def show_time():
	if key==0:
		last_time = rospy.get_time()
		diff=float(int(last_time-current_time))
		return diff
	else:
		return 0

def keys_cb(msg,twist_pub):
	global key,curr,curr1,p
	global current_time
	if msg.buttons[4] & msg.buttons[5]==1:
		key=1
		curr=0
		curr1=0
		current_time = rospy.get_time()	
	else:
		key=0
			
	if msg.axes[1]>0.09 or msg.axes[1]<-0.09:
		curr=curr+show_time()*msg.axes[1]*p
		t.linear.x=curr
		print "Stuck"
	
	if msg.axes[3]>0.09 or msg.axes[3]<-0.09:
		curr1=curr1+show_time()*msg.axes[3]*p*-1
		t.linear.y=curr1
		print "stuck"
	
	twist_pub.publish(t)


if __name__ == '__main__':
	rospy.init_node('joystick',anonymous=True)
	twist_pub = rospy.Publisher('cmd_vel', Twist, queue_size=50)	
	current_time=rospy.get_time()	
	rospy.Subscriber('joy',Joy,keys_cb,twist_pub)
	rospy.spin()

