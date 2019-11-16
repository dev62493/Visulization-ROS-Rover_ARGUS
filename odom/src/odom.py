#!/usr/bin/env python

import math
from math import sin, cos, pi

import rospy
import tf
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3

x=0
y=0
th=0
vx=0
vy=0
vth=0


def odom_cb(msg):
	global x,y,vx,vy,vth

	vx = msg.linear.x
	vth = msg.angular.z
	current_time = rospy.Time.now()
	last_time = rospy.Time.now()
	odom_broadcaster = tf.TransformBroadcaster()
	global th
	dt = (current_time - last_time).to_sec()
	dx = (vx * cos(th) - vy * sin(th)) * dt #taking components
	dy = (vx * sin(th) + vy * cos(th)) * dt
	dth = vth * dt

	x += dx
	y += dy
	th += dth
	
	odom_quat = tf.transformations.quaternion_from_euler(0, 0, th)
	odom_broadcaster.sendTransform((x, y, 0.),odom_quat,current_time,"base_link","odom")

	#publishing odometry to rviz 
	odom = Odometry()
	odom.header.stamp = current_time
	odom.header.frame_id = "odom"
	odom.pose.pose = Pose(Point(x, y, 0.), Quaternion(*odom_quat))
	odom.child_frame_id = "base_link"
	odom.twist.twist = Twist(Vector3(vx, vy, 0), Vector3(0, 0, vth))

	odom_pub.publish(odom)

	last_time = current_time


while not rospy.is_shutdown():

	rospy.init_node('odometry_publisher',anonymous=True)
	
	data_sub = rospy.Subscriber("cmd_vel",Twist,odom_cb)
	odom_pub = rospy.Publisher("odom", Odometry, queue_size=50)	
	rospy.spin()
