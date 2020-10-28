#!usr/bin/env/python

import math as m
import devlib as d

def calc_cap(volt):
	ans = raw_input("l for linear capacitance n for Non linear Capacitance: ")
	print ""
	if ans == "l":
		print "Enter the data for Crss in format C1 C2 V1 V2 with space of a line: "
		raw_crss = d.solve_linear_log(m.log(volt,10))
		crss = m.pow(10,raw_crss)

		print "Enter the data for Ciss in format C1 C2 V1 V2 as above "
		raw_ciss = d.solve_linear_log(m.log(volt,10))
		ciss = m.pow(10,raw_ciss)
		
		print "Enter the data for Coss in format C1 C2 V1 V2 with space of a line: "
		raw_coss = d.solve_linear_log(m.log(volt,10))
		coss = m.pow(10,raw_coss)
		
	else:
		print "Cant solve for Non Linear scale enter manually"
		crss = input("Enter the Crss: ")
		ciss = input("Enter the Ciss: ")
		coss = input("Enter the Coss: ")
	gd = crss
	gs = ciss - crss
	ds = coss - crss
	cap = (gs,gd,ds)
	print ("gate source: "+str(gs)+"gate drain: "+str(gd)+"drain source: "+str(ds))	
	return cap

if __name__=="__main__":
	global flag,count
	[flag,count] = [0,0]
	vdd = float(input("Enter VDD : "))
	vgs = float(input("Enter VGS : "))
	vth = float(input("Enter Vth(min) : "))
	while(1-flag):
		ans = raw_input("Do you want to enter capacitance value ? ")
		print ""
		if ans == "yes" or count == 0:
			vgd  = vdd
			arr_cap = calc_cap(vdd)
			cgs = arr_cap[0]
			cgd = arr_cap[1]
			count =1
		else:
			cgs = cgs
			cgd = cgd
			vgd = vdd
			print cgs,cgd,vgd

		q = cgs*vgs + cgd*vgs + cgd*vgd
		print("charge is "+str(q))
		change = input("1 for manually rounding charge else press 2:")
		if change == 1:
			q=input("Enter the charge value: ")
		prio = raw_input("Set priority to on or off ? ")
		print ""
		if prio == "on":
			ton = input("Enter the Ton : ")
			i   = q/ton
			rg  = vgs/i
			ceq = cgs + cgd
			T = rg*ceq
			off_time = T*m.log(vgs/vth,m.exp(1))
			print ""
			print ("Calculated off time is: " + str(off_time) + " with rg = " + str(rg) + " ohms and current of "+ str(i))
		elif prio == "off":
			toff= input("Enter the Toff: ")
			ceq = cgs + cgd
			tau = toff/(m.log(vgs/vth,m.exp(1)))
			gate_resistor = tau/ceq
			curr = vgs/gate_resistor
			turn_on = q/curr
			print ""
			print ("Calculated on time is: " + str(turn_on) + " with rg = " + str(gate_resistor) + " ohms and current of " + str(curr))
		else:
			print "Wrong input setting default priority to ON Time"
			ton = input("Enter the Ton : ")
			i   = q/ton
			rg  = vgs/i
			ceq = cgs + cgd
			T = rg*ceq
			off_time = T*m.log(vgs/vth,m.exp(1))
			print ""
			print ("Calculated off time is: " + str(off_time) + " with rg = " + str(rg) + " ohms and current of "+str(i))








