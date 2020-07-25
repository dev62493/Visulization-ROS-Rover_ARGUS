import math as m
import numpy as np

def setlimit(joint,upper,lower):
	if joint>upper: 
		joint=upper
	elif joint<lower:
		joint=lower
	else:
		joint=joint
	return joint

def add(parameter,addfactor,time):
	parameter+=addfactor*time
	return parameter

def calc_yaw(distx,disty):
	mag_x=abs(distx)
	mag_y=abs(disty)
	if mag_x == 0:
		raw_yaw = m.pi/4
	else:
		raw_yaw = m.atan(mag_y/mag_x)
	if distx > 0 and disty > 0:
		yaw = raw_yaw
	elif distx < 0 and disty < 0:
		yaw = raw_yaw + m.pi
	elif distx > 0 and disty < 0:
		yaw = 2*m.pi - raw_yaw 
	else:
		yaw = m.pi - raw_yaw
	return yaw
	
def cvt2deg_x2x(rad):
	net = m.pi - rad
	deg = 180*(net/m.pi)
	return deg

def cvt2deg(rad):
	net = rad*180/m.pi
	return net

def distance(x1,y1,x2,y2):
	t1 = (x2-x1)*(x2-x1)
	t2 = (y2-y1)*(y2-y1)
	dist = m.sqrt(t1+t2)
	return dist

def solve_linear_log(x):
	d1=[]
	for i in range (0,4):
		inp=(raw_input())
		d1.append(inp)
	print d1		
	m1 = np.array(d1).reshape(2, 2)
	m00 = m.log(float(m1[0][0]),10)
	m01 = m.log(float(m1[0][1]),10)
	m10 = m.log(float(m1[1][0]),10)
	m11 = m.log(float(m1[1][1]),10)
	c= ((m00*m11)-(m01*m10))/ (m11- m10)
	slope = (m01 - m00)/ (m11 - m10)
	out = slope*x+c
	print slope ,c,x
	return out	

p_error=0

def pid(kp,kd,ki,error):
	global p_error
	integral = error + p_error
	diff	 = error - p_error
	net_error = kp*error + kd*diff + ki*integral
	p_error = error
	return net_error

