#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

t=Twist()
count=0
pwm1=0
pwm2=0

def keys_cb(msg,twist_pub):
	global count,pwm1,pwm2
	if msg.buttons[4] and msg.buttons[5] ==1:
		if msg.axes[1]!=0:		
			pwm1=pwm1+msg.axes[1]*count*0.05
			if pwm1>=255:
				pwm1=255
			elif pwm1<=-255:
				pwm1=-255
			else:
				pwm1=pwm1		
			t.linear.x=pwm1
			t.angular.z=0
			if count>200:
				print "Counter reset"
				count=0		
		
		elif msg.axes[3]!=0:	
			pwm2=pwm2+msg.axes[3]*count*0.006
			if pwm2>=6.28:
				pwm2=6.28
			elif pwm2<=-6.28:
				pwm2=-6.28
			else:
				pwm2=pwm2		
			t.linear.x=0			
			t.angular.z=pwm2
			if count>200:
				print "Counter reset"
				count=0
		else:
			print "Nothing is commanded"
		count=count+1
	
	else:
		t.linear.x=msg.axes[1]*255
		t.angular.z=msg.axes[3]*6.28 
		count=0
		pwm1=0
		pwm2=0	
	twist_pub.publish(t)

if __name__ == '__main__':
	rospy.init_node('time_control',anonymous=True)
	twist_pub = rospy.Publisher('cmd_vel', Twist, queue_size=50)		
	rospy.Subscriber('joy',Joy,keys_cb,twist_pub)
	rospy.spin()
