#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
import tf
ps=PoseStamped()


def call_back():
	ps.header.stamp = rospy.Time.now()
	ps.header.frame_id = "odom"
	ps.pose.position = (3,3,0)
	euler[0] = 0
	euler[1] = 0
	euler[2] = 0
	quat=tf.transformations.quaternion_from_euler(euler[0],euler[1],euler[2])
	ps.pose.orientation = (quat[0],quat[1],quat[2],quat[3])
	pub.publish(ps)

if __name__=="__main__":
	rospy.init_node("Goal",anonymous=True)
	pub=rospy.Publisher("move_base_simple/goal",PoseStamped,queue_size=200)
	rospy.spin()
