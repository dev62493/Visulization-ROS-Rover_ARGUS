#!/usr/bin/env python
import rospy,tf,time,math,devlib
import math as m 
import numpy as np
from devlib 		import add,setlimit
from std_msgs.msg 	import Float32MultiArray
from sensor_msgs.msg 	import JointState

j=JointState()
odom_broadcaster = tf.TransformBroadcaster()
var=[0,0,0,0,0]
[x,y,th]=[0,0,0]
arr = np.array([[0.2,-0.2],[0.02,-0.2],[3.14,-3.14],[0,-3.14],[0,6.28]])
flag = 0
def data_cb(msg):
	global var,x,y,th,arr
	flag = 1
	bit = msg.data
	for i in range (0,4):
		var[i] = add(var[i],bit[i],bit[7])
		var[i] = setlimit(var[i],arr[i,0],arr[i,1])
	j.header.stamp = rospy.Time.now()
	j.header.frame_id = "odom"
	j.name = ['prism1','prism2','rot1','rot2','cont']
	j.position = var
	j.velocity = [bit[0],bit[1],bit[2],bit[3],bit[4]]
	j.effort = [0]
	th = add(th , bit[6] , bit[7])
	if th < 0:
		th = 2*m.pi + th
	if th >= 2*m.pi:
		th = th - 2*m.pi
	x  = add(x , bit[5] * m.cos(th) , bit[7])
	y  = add(y , bit[5] * m.sin(th) , bit[7])	
	odom_quat = tf.transformations.quaternion_from_euler(0, 0, th)		
	odom_broadcaster.sendTransform((x, y, 0.),odom_quat,rospy.Time.now(),"base_link","odom")
	joint_state_pub.publish(j)

if __name__=='__main__':
	rospy.init_node('odometry_1',anonymous=True)
	joint_state_pub =rospy.Publisher('joint_states',JointState,queue_size=100)
	joint_sub=rospy.Subscriber('joint_data',Float32MultiArray,data_cb)
	rospy.spin()
