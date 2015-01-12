from math import pi
# Import user parameters
import g

class Tmodel():
	def __init__(self):
		self.T = g.Tamb
		self.Tplt = g.Tamb
		self.eta = 0.0
		return
	
	def calc_Qout(self):
		# Convection sides
		rayleigh = (g.grav*g.beta*(self.T-g.Tamb)*g.h**3)/(g.nu*g.kappa)
		f1 = (1+(0.492/g.prandtl)**(9/16.0))**(-16/9.0)
		nu_plt = (0.825+0.387*(rayleigh*f1)**(1/6.0))**2
		nusselt = nu_plt+0.97*(g.h/(2*g.r))
		alpha = (nusselt*g.lambda_air)/g.h
		Qout = alpha*g.A*(self.T-g.Tamb)
		# Convection top
		ra2 = (g.grav*g.beta*(self.T-g.Tamb)*(g.r/2)**3)/(g.nu*g.kappa)
		f2 = (1+(0.322/g.prandtl)**(11/20.0))**(-20/11.0)
		if ra2*f2 > 7*10**4:
			nu2 = 0.15*(ra2*f2)**(1/3.0)
		else:
			nu2 = 0.766*(ra2*f2)**(1/5.0)
		alpha2 = (nu2*g.lambda_air)/(g.r/2)
		Qout2 = alpha2*(pi*g.r**2)*(self.T-g.Tamb)
		# Radiation from sides
		Csid = g.sigma/((1/g.epsilon_steel)+(1/g.epsilon_white)-1)
		Takel = g.Tamb+273.15
		Tkel = self.T+273.15
		Qout3 = Csid*g.A*((Tkel**4)-(Takel**4))
		# Radiation from top
		Ctop = g.sigma/((1/g.epsilon_water)+(1/g.epsilon_white)-1)
		Qout4 = Ctop*(pi*g.r**2)*((Tkel**4)-(Takel**4))
		return g.fit*(Qout+Qout2+Qout3+Qout4)
		
	def calc_Qin(self,eta):
		# Calculate heating of the heating surface
		Qin_plt = g.Qin_nom*eta*g.t
		dT_plt_in = Qin_plt/(g.cp_iron*g.m_plt)
		self.Tplt += dT_plt_in
		# Calculate conduction to kettle
		Q_cond = g.lambda_rst*g.A_plt*((self.Tplt-self.T)/g.delta)
		dT_plt_out = Q_cond/(g.cp_iron*g.m_plt)
		self.Tplt -= dT_plt_out
		# Return conduction to kettle
		Qin = Q_cond
		return Qin
	
	def tick(self,eta):
		self.eta = eta
		Qout = self.calc_Qout()*g.t
		Qin = self.calc_Qin(eta)*g.t
		Q = Qin-Qout
		dT = Q/(g.cp*g.m)
		self.T += dT
		if g.DEBUG:
			print 'Qin: %.2f W - Qout: %.f W' % (Qin, Qout)
			self.print_state()
		return self.T
	
	def getT(self):
		return self.T
	
	def getTplt(self):
		return self.Tplt
	
	def get_eta(self):
		return self.eta
	
	def print_state(self):
		print 'Water: %.2f C - Heating surface: %.2f C' % (self.T, self.Tplt)
		return