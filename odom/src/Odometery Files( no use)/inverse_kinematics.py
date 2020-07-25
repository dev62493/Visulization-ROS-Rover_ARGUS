#!/usr/bin/env python
import rospy
import tf
import time 
import math

from std_msgs.msg import Float32MultiArray,Header,Int32
from sensor_msgs.msg import JointState
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Vector3
from visualization_msgs.msg import Marker

j=JointState()
odom=Odometry()
odom_broadcaster = tf.TransformBroadcaster()

px=1
py=1
pth=1

def calc_yaw(distx,disty):
	mag_x=abs(distx)
	mag_y=abs(disty)
	raw_yaw = math.atan(mag_x/mag_y)
	if distx > 0 and disty > 0:
		yaw = raw_yaw
	elif distx < 0 and disty < 0:
		yaw = raw_yaw + math.pi
	elif distx > 0 and disty < 0:
		yaw = math.pi - raw_yaw 
	else:
		yaw = 2*math.pi - raw_yaw
	return yaw


def pri_cb(msg):
	global c_x,c_y,c_z,px,py,pth
	crit_x=1
	crit_y=1	
	(c_x,c_y,c_z) = msg.data
	e_x=g_x-c_x
	e_y=g_y-c_y
	e_z=g_z-c_z
	theta = calc_yaw(e_x,e_y)
	omega = theta*pth	
	if e_x >= crit_x:
		vx = px*abs(e_x)
	elif e_y >= crit_y:
		vy = py*abs(e_y)
	else:
		print "Manipulator"	
	j.header = Header()
        j.header.stamp = rospy.Time.now()
	j.header.frame_id = "odom"
	j.name = ['prism1','prism2','rot1','rot2','cont']
	j.position = [0,0,0,0,0]
	j.velocity = [0,0,0,0,0]
	j.effort = [0,0,0,0,0]
	
	odom_quat = tf.transformations.quaternion_from_euler(0, 0, theta)		
	odom_broadcaster.sendTransform((c_x, c_y, 0.),odom_quat,rospy.Time.now(),"base_link","odom")
	odom.header.stamp = rospy.Time.now()
	odom.header.frame_id = "odom"
	odom.pose.pose = Pose(Point(c_x, c_y, 0.), Quaternion(*odom_quat))
	odom.child_frame_id = "base_link"	
	odom.twist.twist.linear.x=vx 
	odom.twist.twist.linear.y=vy
	odom.twist.twist.linear.z=0
	odom.twist.twist.angular.x=0
	odom.twist.twist.angular.y=0
	odom.twist.twist.angular.z=omega
	joint_state_pub.publish(j)
	odometry_pub.publish(odom)
	
def sec_cb(goal):
	global g_x,g_y,g_z
	g_x = goal.pose.position.x
	g_y = goal.pose.position.y
	g_z = goal.scale.z

if __name__=='__main__':
	rospy.init_node('odometry',anonymous=True)
	goal_sub=rospy.Subscriber('goal',Marker,sec_cb)
	point_sub=rospy.Subscriber('current_coordinates',Float32MultiArray,pri_cb)	
	odometry_pub=rospy.Publisher('odom',Odometry,queue_size=100)
	joint_state_pub =rospy.Publisher('joint_states',JointState,queue_size=100)
	rospy.spin()
