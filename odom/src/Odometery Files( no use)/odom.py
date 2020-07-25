#!/usr/bin/env python

import time 
import math
from math import sin, cos, pi

import rospy
import tf
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
from sensor_msgs.msg import Joy

x=0
y=0
th=0
vx=0
vy=0
vth=0
last_time=0
current_time=0
c=0.001
d=300
k=0

def odom_cb(msg):
		
	global x,y,vx,vy,vth,last_time,current_time
	current_time = rospy.Time.now()
	last_time = rospy.Time.now()		
	odom_broadcaster = tf.TransformBroadcaster()
	global th
	dt = (last_time-current_time).to_sec()	
	dt=dt/c
	vx = msg.linear.x/dt*c
	vth = msg.angular.z/dt
	dx = (vx * cos(th)) * dt #taking components
	dy = (vx * sin(th)) * dt
	dth = vth * (dt*d)
	x += dx
	y += dy
	th += dth
	odom_quat = tf.transformations.quaternion_from_euler(0, 0, th)	
	print x,y,odom_quat	
	odom_broadcaster.sendTransform((x, y, 0.),odom_quat,current_time,"base_link","odom")

	#publishing odometry to rviz 
	odom = Odometry()
	odom.header.stamp = current_time
	odom.header.frame_id = "odom"	
	odom.pose.pose = Pose(Point(x, y, 0.), Quaternion(*odom_quat))
	odom.child_frame_id = "base_link"	
	odom.twist.twist = Twist(Vector3(vx, vy, 0), Vector3(0, 0, vth))
	#print odom
	if k==0:			
		odom_pub.publish(odom)

def joy_cb(vari):
	global k
	if vari.buttons[6] & vari.buttons[7] != 1:
		k=0
	if vari.buttons[6] & vari.buttons[7] == 1:
		k=1

while not rospy.is_shutdown():

	rospy.init_node('odometry_publisher',anonymous=True)	
	rospy.Subscriber('joy',Joy,joy_cb)	
	data_sub = rospy.Subscriber("cmd_vel",Twist,odom_cb)
	odom_pub = rospy.Publisher("odom", Odometry, queue_size=50)	
	rospy.spin()

