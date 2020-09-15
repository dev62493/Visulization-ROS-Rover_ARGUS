#!/usr/bin/env python
import rospy

from nav_msgs.msg import Path
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped

path = Path()
[x,y]=[0,0]

def odom_cb(data):
	global path,x,y
	path.header = data.header
	pose = PoseStamped()
	pose.header = data.header
	pose.pose = data.pose.pose
	path.poses.append(pose)
	x=pose.pose.position.x
	y=pose.pose.position.y
	print x,y
	path_pub.publish(path)



if __name__ == '__main__':
	rospy.init_node('path_node',anonymous=True)
	odom_sub = rospy.Subscriber('/odom', Odometry, odom_cb)
	path_pub = rospy.Publisher('/path', Path, queue_size=10)
	rospy.spin()
