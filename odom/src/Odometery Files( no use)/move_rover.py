#!/usr/bin/env python
import rospy
import tf
import time 
import math

from sensor_msgs.msg import JointState,Joy
from std_msgs.msg import Header,Int32
from math import sin, cos, pi
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3


[x,y,th,vx,vy,vth,p_a,p_b,p_b,p_c,p_d,p_e,k,last_time,current_time
]=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

c=0.001
d=300



def odom_cb(msg):
	
	global x,y,vx,vy,vth,last_time,current_time,p_vx,p_vth
	current_time = rospy.Time.now()	
	last_time = rospy.Time.now()	
	odom_broadcaster = tf.TransformBroadcaster()
	global th
	dt = (last_time-current_time).to_sec()	
	dt=dt/c
	if k==0:	
		vx = msg.linear.x/dt*c
		vth = msg.angular.z/dt
		p_vx=vx
		p_vth=vth
		dx = (vx * cos(th)) * dt #taking components
		dy = (vx * sin(th)) * dt
		dth = vth * (dt*d)
		odom = Odometry()
		odom.twist.twist = Twist(Vector3(vx, vy, 0), Vector3(0, 0, vth))	
	dx = (p_vx * cos(th)) * dt #taking components
	dy = (p_vx * sin(th)) * dt
	dth = p_vth * (dt*d)	
	x += dx
	y += dy
	th += dth
	odom_quat = tf.transformations.quaternion_from_euler(0, 0, th*0.01)		
	odom_broadcaster.sendTransform((x, y, 0.),odom_quat,current_time,"base_link","odom")
	odom = Odometry()
	odom.header.stamp = current_time
	odom.header.frame_id = "odom"	
	odom.pose.pose = Pose(Point(x, y, 0.), Quaternion(*odom_quat))
	odom.child_frame_id = "base_link"	
	odom.twist.twist = Twist(Vector3(p_vx, vy, 0), Vector3(0, 0, p_vth))
	#print odom			
	hello_str = JointState()	
	hello_str.header = Header()
        hello_str.header.stamp = rospy.Time.now()
	hello_str.header.frame_id = "base_link"
	hello_str.name = ['prism1','prism2','rot1','rot2','cont']
	hello_str.position = [p_a,p_b,p_c,p_d,p_e]	
	hello_str.velocity = [0]
	hello_str.effort = [0]
		
	manu_pub.publish(hello_str)	
	odom_pub.publish(odom)

def joy_cb(vari):
	global k
	if vari.buttons[6] & vari.buttons[7] != 1:
		k=0
	if vari.buttons[6] & vari.buttons[7] == 1:
		k=1

def callback(msg,manu_pub):
	global p_a,p_b,p_c,p_d,p_e	
	hello_str = JointState()
	hello_str.header = Header()
        hello_str.header.stamp = rospy.Time.now()
	hello_str.header.frame_id = "odom"
	hello_str.name = ['prism1','prism2','rot1','rot2','cont']
	if k==1:	
		a=(msg.linear.z/100)
		b=(msg.linear.y/100)
		c=(msg.angular.z/100)
		d=(msg.angular.x/10)
		e=(msg.linear.x/10)
		p_a=a
		p_b=b
		p_c=c
		p_d=d
		p_e=e
		hello_str.position = [a,b,c,d,e]
	hello_str.position = [p_a,p_b,p_c,p_d,p_e]	
	hello_str.velocity = [0]
	hello_str.effort = [0]
	manu_pub.publish(hello_str)


if __name__ == '__main__':
	rospy.init_node('Visulise',anonymous=True)
	joy_sub=rospy.Subscriber('joy',Joy,joy_cb)
	manu_pub = rospy.Publisher('joint_states', JointState, queue_size=100)
	manu_sub = rospy.Subscriber('manipulator', Twist, callback,manu_pub)	
	cmd_vel_sub = rospy.Subscriber("cmd_vel",Twist,odom_cb)	
	odom_pub = rospy.Publisher("odom", Odometry, queue_size=50)	
	rospy.spin()



