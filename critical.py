import numpy
import numpy.matlib
import math
import time
import importlib
import cumulus

def drained(h,b,zed,gam,c_,r):
	phi=numpy.arange(float(1), float(50), float(0.01)).tolist()
	phi_mob=[]

	for x in phi:
		s=cumulus.twowedge(h,b,zed,x,gam,c_,r)
		p=s.passive()
		a=s.active(step=1)
		diff=a-(p[-1])
		if -0.01 <= diff <= 0.01:
			phi_mob.append(x)

	return max(phi_mob)

def undrained(h,b,zed,gam,r=0):
	c=numpy.arange(float(1), float(80), float(0.01)).tolist()
	c_mob= []

	for x in c:
		s=cumulus.twowedge(h,b,zed,0,gam,x,r)
		p=s.passive()
		a=s.active(step=1)
		diff = a-(p[-1])
		if -0.1 <= diff <= 0.1:
			c_mob.append(x)

	return max(c_mob)
