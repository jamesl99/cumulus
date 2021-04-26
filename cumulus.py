import numpy
import numpy.matlib
import math
import time



class twowedge(object):
	"""This class holds slope characterstics"""
	def __init__(self, h_s, beta, z, phi_mob, gamma, c, r_u=0, alpha = 0.7):
		super(twowedge, self).__init__()
		self.h_s = float(h_s)
		self.alpha = float(alpha)
		self.beta = numpy.deg2rad(float(beta))
		self.z = float(z)
		self.phi_mob = numpy.deg2rad(float(phi_mob))
		self.gamma = float(gamma)
		self.l_s= (self.h_s)/(math.tan(self.beta))
		self.r_u = float(r_u)
		self.c=float(c)

		#default pore water pressure at 0 kN/m2

		#Defines positions of points

		self.toe = [0,0]

		self.one_a = []

		one_a_x = self.alpha*self.l_s
		one_a_y = self.alpha*self.h_s
		self.one_a.append(one_a_x)
		self.one_a.append(one_a_y)


		self.two = [self.l_s,self.h_s]



		#Passive

		self.one_b=[self.alpha*self.l_s,(self.alpha*self.h_s)-self.z]

		self.theta_p = math.atan(self.one_b[1]/self.one_b[0])
		#in radians




	def passive(self):
		"""Returns l_p, area, weight, U, c'l, N, T, H_p"""
		passive_data=[]
		theta_p=self.theta_p

		l_p= math.sqrt(self.one_b[0]**2+self.one_b[1]**2)
		passive_data.append(l_p)

		area = self.z*self.one_a[0]*0.5
		passive_data.append(area)

		weight = area*self.gamma
		passive_data.append(weight)

		u = (self.r_u*weight)/(math.cos(theta_p))
		passive_data.append(u)

		cl=l_p*self.c
		passive_data.append(cl)

		N_top = weight - (cl*math.sin(self.theta_p)) + (u*math.sin(self.theta_p)*math.tan(self.phi_mob))

		N_bottom = (math.tan(self.phi_mob)*math.sin(self.theta_p)) + math.cos(theta_p)

		N=N_top/N_bottom
		passive_data.append(N)

		T= ((N-u)*math.tan(self.phi_mob))+cl
		passive_data.append(T)

		H_p= -(N*math.sin(theta_p))+(T*math.cos(theta_p))
		self=H_p=H_p
		passive_data.append(H_p)

		return passive_data

	def active(self, theta_a_lower=5, theta_a_upper=90, step = 5):
		"""Returns Maximum Value of H_a"""

		theta_a_deg=numpy.arange(float(theta_a_lower), float(theta_a_upper), float(step)).tolist()
		theta_a_rad=[]

		for x in theta_a_deg:
			theta_a_rad.append(numpy.deg2rad(x))

		phi=self.phi_mob

		self.arr_active=numpy.array([])
		A_Azero = ((self.two[0]-self.one_a[0])*(self.two[1]-self.one_a[1])*0.5)

		count = int(0)
		h_a_row = []
		theta_row=[]

		while count <= (len(theta_a_rad)):
			x = int(x)

			rad = theta_a_rad[count]

			l_a = (self.two[1]-self.one_b[1])/(math.tan(theta_a_rad[count]))

			A_a=((self.two[1]-self.one_b[1])*l_a*0.5)-A_Azero

			l_b=(l_a/(math.cos(rad)))

			W_a=self.gamma*A_a

			cl_a=self.c*l_b

			U_a=(self.r_u*W_a)/(math.cos(rad))

			N_a_top=W_a-(cl_a*math.sin(rad))+(U_a*math.tan(self.phi_mob)*math.sin(rad))
			N_a_bottom=math.cos(rad)+(math.tan(self.phi_mob)*math.sin(rad))
			N_a=N_a_top/N_a_bottom


			T_a=((N_a-U_a)*(math.tan(self.phi_mob)))+cl_a

			H_a=((N_a*math.sin(rad))-(T_a*math.cos(rad)))
			h_a_row.append(H_a)

			if count == len(theta_a_rad)-1:
				break

			count+=1

		return max(h_a_row)

	def active_array(self, theta_a_lower=5, theta_a_upper=90, step = 5):
		"""Set upper and lower limit values for active angle. Default Values taken as"""
		theta_a_deg=numpy.arange(float(theta_a_lower), float(theta_a_upper), float(step)).tolist()

		theta_a_rad=[]
		#key used to search list of values

		for x in theta_a_deg:
			theta_a_rad.append(numpy.deg2rad(x))

		self.arr_active=numpy.array([])
		"""Array order theta, l_a, A_a, l_b, W_a, c'l_a, U_a, N_a , T_a , H_a (width=10, height = len(theta_a_rad))"""

		A_Azero = ((self.two[0]-self.one_a[0])*(self.two[1]-self.one_a[1])*0.5)


		count = int(0)
		while count <= (len(theta_a_rad)):
			row = []
			x = int(x)

			rad = theta_a_rad[count]

			row.append(theta_a_deg[count])

			l_a = (self.two[1]-self.one_b[1])/(math.tan(theta_a_rad[count]))
			row.append(l_a)

			A_a=((self.two[1]-self.one_b[1])*l_a*0.5)-A_Azero
			row.append(A_a)

			l_b=(l_a/(math.cos(rad)))
			row.append (l_b)

			W_a=self.gamma*A_a
			row.append (W_a)

			cl_a=self.c*l_b
			row.append (cl_a)

			U_a=(self.r_u*W_a)/(math.cos(rad))
			row.append(U_a)

			N_a_top=W_a-(cl_a*math.sin(rad))+(U_a*math.tan(self.phi_mob)*math.sin(rad))
			N_a_bottom=math.cos(rad)+(math.tan(self.phi_mob)*math.sin(rad))
			N_a=N_a_top/N_a_bottom
			row.append (N_a)

			T_a=((N_a-U_a)*(math.tan(self.phi_mob)))+cl_a
			row.append(T_a)

			H_a=((N_a*math.sin(rad))-(T_a*math.cos(rad)))
			row.append(H_a)

			self.arr_active=numpy.append(self.arr_active,row)

			if count == len(theta_a_rad)-1:
				break

			count+=1

		self.arr_active = self.arr_active.reshape(len(theta_a_rad),10)
		return self.arr_active

