# Midterm Project: Modeling a Rocket Launch with Gravity and Air Resistance
# IP4CS: Intro to Programming for Computational Sciences
# author: Jiin So (intro, Part 1, Part 4) Sumin Kyoung (Part 2, Part 3)
# date: 10/28/2014


# import needed modules of python
import numpy as np
import pylab as pl
import visual as vis


# assign constant variables with their respective values
# units are in S.I. units.
height_ISS = 355000.0									# height of the International Space Station
mass_empty = 10000.0									# mass of the empty rocket
mass_fuel = 10000.0										# mass of fuel (maximum amount = 10000)
mass_payload = 4474.51590745							# maximum payload (with max. fuel)
m_0 = mass_empty + mass_fuel+ mass_payload				# initial mass before launch
m_1 = mass_empty +mass_payload
v_exhaust = 7000.0									# exhaust velocity
burn_rate = 100.0										# burn rate of the fuel (kg/s)
radius_earth = 6.37 * 10 ** 6								# radius of earth in meters
gravity_earth = 9.81									# gravity near earth (m/s**2)
area_reference = 10.0									# reference area of rocket (m**2)
drag_coefficient = 0.5
temp_lapse = 0.0065									# temperature lapse rate; (Kelvin per meter)
temp_sea = 288.0										# in Kelvin
press_sea = 1.01 * 10 ** 5								# air pressure at sea level (Pa)
molar_mass = 0.02896									# molar mass of air (kg/mole)
ideal_gas = 8.314										# ideal gas constant (Joules/(Kelvin*mole))



# set initial conditions
a = 0.0								# starting time point
b = 350.0								# ending time point; change to appropriate time as fit
N = 10000							# number of steps
h = (b-a)/float(N)						# width of each step interval of time
t_points= np.arange(a, b, h)				# create array of t_points


#----------------------------- Part 3: Air Resistance-----------------------------------------------------------------------------------------------------------------------------------------------------------
# Now taking air resistance into account, remodel the trajectory path of the rocket.
# F_total = F_thrust + F_gravity + F_air, where
# F_thrust = burn_rate * v_exhaust
# F_gravity = mass * gravity = (m_0 - burn_rate*t)*(gravity_earth / (1 + height/radius_earth)**2)
# F_air = (0.5 * pressure * molar_mass * area_reference * drag_coefficient * (velocity ** 2.0) / (ideal_Gas * temperature))
# Adding F_Air Resistance is more complicated than adding F_gravity because there are two dynamic variables that depends on each other.
# Again, note that the mass is not the initial mass, but it is changing (lost burn_rate * t kg of mass for time t), but only while there is fuel to burn.

# Define functions (Temp, Grav, Press, and Air_Resistance) to use in calculating air resistance.
def Temp(height):                                       		# Temperature changes based on the height
    if temp_sea - (temp_lapse * height) > 0:		# Temperature cannot be negative	
        return temp_sea - (temp_lapse * height)
    else:
    	return 0

def Grav(height):                                      		 # Gravity also changes based on the height as mentioned in previous part
    return gravity_earth / (1.0 + height/radius_earth) ** 2.0
    
def Press(temp,g):                                         		# Pressure changes based the temperature and gravity
    if temp > 0:								# Pressure = 0 if temperature =0
        return press_sea * (temp / temp_sea) ** (g * molar_mass/(ideal_gas * temp_lapse))
    else:
        return 0
    
def Air_Resistance(press, temp): 				# Air Resistance changes based on pressure and temperature
    if temp > 0:								# Air_Resistance is only defined if temp is larger than 0. Or else there is no air resistance.
        return -0.5 * press * molar_mass * area_reference * drag_coefficient * (velocity ** 2.0) / (ideal_gas * temp)
    else:
    	return 0


# Define functions of acceleration.
# Like in Part 2, we need two acceleration functions to represent the acceleration when the fuel is burning and when there is no more fuel to burn.
def Acc_A1(t):
    return (burn_rate * v_exhaust - (m_0 - burn_rate * t) * gravity_earth / (1.0 + height/radius_earth) ** 2.0 + air_resis) / (m_0 - burn_rate*t)

def Acc_A2 (t):
    return -(gravity_earth / ((1 + height/radius_earth) ** 2)) + (air_resis)/(m_1)


# set initial conditions (things that need to be set to 0 or empty again)
height = 0.0										# initial height, velocity, and time = 0
velocity = 0.0
t_i= 0.0
temp = Temp(height)
g = Grav(height)
press = Press(temp, g)
air_resis = Air_Resistance(press, temp)
velocity = velocity - 0.5*h*Acc_A1(t_i)		        			# set the velocity half step back for the leap frog method
velocity_points = []				     				# set up empty lists for velocity points and height points
height_points = []



for t in t_points:							# for each time point in t_points
    if t <= 100.0:								# if t is smaller than 100 s (if the fuel is not used up), use the leap frog method to find the next points of velocity and height
        height_points.append(height)
        velocity_sync = velocity + 0.5*h*Acc_A1(t)	# velocity is half-step off, so to plot the correct velocity for the correct times we need to append the synced velocity
        velocity_points.append(velocity_sync)
        velocity += h*Acc_A1(t)
        height += h*velocity
        temp = Temp(height)
        g = Grav(height)
        press = Press(temp,g)
        air_resis = Air_Resistance(press, temp)
    else:									# if t is greater than 100s, the fuel is used up; velocity does not change.
        height_points.append(height)
        velocity_sync = velocity + 0.5*h*Acc_A2(t)	# velocity is half-step off, so to plot the correct velocity for the correct times we need to append the synced velocity
        velocity_points.append(velocity_sync)
        velocity += h*Acc_A2(t)
        height += h*velocity
        temp = Temp(height)
        g = Grav(height)
        press = Press(temp,g)
        air_resis = Air_Resistance(press, temp)

#----------------------------- Part 4: VPython -----------------------------------------------------------------------------------------------------------------------------------------------------------
# Create an animation for the launched rocket reaching the ISS 
scene1 = vis.display (title = 'Animation of Launched Rocket to the ISS: Max Payload')

# create three objects: Earth, the International Space Station, and the rocket.
Earth = vis.sphere(pos=[0,-250,0], radius = 50, color=vis.color.green)
ISS = vis.sphere(pos = [0, 160, 0], radius = 5, color=vis.color.magenta)
rocket = vis.cone(pos=[0, -200, 0], axis = (0, 10, 0), radius = 2, color=vis.color.cyan)

# define the rate of the animation and the height of the rocket using the data from the previous parts (heigh_points)
for item in height_points:
    vis.rate (500)
    rocket.pos.y = (item/1000) - 200
