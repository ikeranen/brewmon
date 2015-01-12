from math import pi
# Paramaters for brewHW simulator

# For serial communication (com0com can be used to run client and sim)
serialport = 2

# Local echoing of recieved commands
cmdecho = True

# Local echoing of outgoing messages
locecho = True

# Time to sleep between ticks in seconds
interval = 1

# Thermal model parameters 
DEBUG = 0					# Debug mode
fit = 1.0					# Fit to experiment data (Stetson-Harrison constant)
vol = 0.015 				# Volume of water, m^3
rho = 998.2071				# Density of water @ 20C, kg/m^3
cp = 4181.3					# Specific heat capacity of water, J/(kgK)
Tamb = 20.0					# Ambient temperature, C
t = 1						# Timestep, s
Qin_nom = 2000.0			# Nominal heating power, W
r = 0.16					# Radius of kettle, m
delta = 0.002				# Thickness of kettle, m
lambda_rst = 16				# Thermal conductivity of stainless steel, W/(mK)
A = ((2*r*vol)/r**2)		# Area of kettle walls, m^2
m = rho*vol					# Mass of water, kg
h = vol/(pi*r**2)			# Height of kettle, m
w = 2*pi*r					# Width of kettle equivalent, m
nu = 1.9*10**-5				# Thermal diffusitivity of air, m^2/s
kappa = 1.57*10**-5			# Kinematic viscosity of air, m^2/s
prandtl = nu/kappa			# Prandtl number
lambda_air = 0.0257			# Thermal conductivity of air, W/(mK)
grav = 9.81					# Gravitational acceleration, m/s^2
beta = 1/(Tamb+273.15)
sigma = 5.6704*10**-8		# Stefan-Boltzmann constant, W/(m^2*K^4)
epsilon_water = 0.95		# Emissivity of water
epsilon_steel = 0.27		# Emissivity of steel
epsilon_white = 0.925		# Emissivity of white surface (radiation to)
r_plt = 0.185/2.0			# Radius of heating surface, m
t_plt = 0.02				# Thickness of heating surface, m
cp_iron = 450.0				# Specific heat capacity of iron, J/(kgK)
rho_iron = 7300.0			# Density of iron, kg/m^3
A_plt = pi*r_plt**2			# Surface area of heating surface, m^2
vol_plt = A_plt*t_plt		# Volume of heating surface, m^3
m_plt = vol_plt*rho_iron	# Mass of heating surface, kg