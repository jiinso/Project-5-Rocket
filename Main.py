# Midterm Project: Modeling a Rocket Launch with Gravity and Air Resistance
# IP4CS: Intro to Programming for Computational Sciences
# author: Jiin So, Sumin Kyoung
# date: 10/28/2014


# import needed modules of python
import numpy as np
import pylab as pl

# assign constant variables with their respective values
# units are in S.I. units.
# burn rate is kg/s
height_ISS = 355000.0
mass_empty = 10000.0
mass_maxfuel = 10000.0
v_exhaust = 7000.0
burn_rate = 100.0
area_reference = 10.0
drag_coefficient = 0.5
m_0 = mass_empty + mass_maxfuel


#----------------------------- Part 1: Rocket Thrust-----------------------------------------------------------------------------------------------------------------------------------------------------------
# First define the acceleration function that is dependent on time t.
# We know this equation because we know force = mass * acceleration = burn_rate * v_exhaust
# Note that the mass is not the initial mass, but it is changing (lost burn_rate * t kg of mass for time t)
def acc(t):
    return burn_rate * v_exhaust /(m_0 - burn_rate*t)


# set initial conditions
a = 0.0							# starting time point
b = 140.0							# ending time point
N = 10000						# number of steps
h = (b-a)/float(N)					# width of each step interval of time
t_points= np.arange(a, b, h)			# create array of t_points
height = 0.0						# initial height, velocity, and time = 0
velocity = 0.0
t_i= 0.0
velocity = velocity - 0.5*h*acc(t_i)		# set the velocity half step back for the leap frog method
velocity_points = []				# set up empty lists for velocity points and height points
height_points = []

for t in t_points:								# for each time point in t_points
    if t <= 100.0:								# if t is smaller than 100 s (if the fuel is not used up), use the leap frog method to find the next points of velocity and height
        height_points.append(height)	
        velocity_sync = velocity + 0.5*h*acc(t)			# velocity is half-step off, so to plot the correct velocity for the correct times we need to append the synced velocity
        velocity_points.append(velocity_sync)
        velocity += h*acc(t)
        height += h*velocity
    else:										# if t is greater than 100s, the fuel is used up; velocity does not change.
        height_points.append(height)
        velocity_points.append(velocity)				# append the final velocity at 100s for each of the continuing points
        height += h*velocity						# use the constant velocity to calculate the new height for 100 more seconds.	


# plot graph of height vs. time
pl.figure(1)
pl.plot(t_points, height_points, label = 'height')
pl.legend(loc=2)
pl.show()

# plot graph of velocity vs. time
pl.figure(2)
pl.plot(t_points, velocity_points, label = 'velocity')
pl.legend(loc=2)
pl.show()





#----------------------------- Part 2: Gravity -----------------------------------------------------------------------------------------------------------------------------------------------------------
# The acceleration we acquired above did not take gravity into account.
# But we know that F_total = F_thrust + F_gravity = mass * acceleration - mass * gravity
# = burn_rate * v_exhaust - burn_rate * t * g_s / (1 + height/R_earth)^2
# Note that the mass is not the initial mass, but it is changing (losing burn_rate * t kg of mass as time t changes)

R_earth = 6.37 * 10 ** 6                                # in meters
Grav_Const = 6.674 * 10 ** -11                          # in N*m^2/kg^2
M_earth = 5.9722 * 10 ** 24                             # in kilograms
Grav_earth = 9.81

def acc_g(t):
    return (burn_rate * v_exhaust - burn_rate * t * Grav_earth / (1 + height/R_earth) ** 2) / (m_0 - burn_rate*t)

# set initial conditions again for including Gravity
a = 0.0							# starting time point
b = 200.0				                # ending time point
N = 10000						# number of steps
h = (b-a)/float(N)					# width of each step interval of time
t_points= np.arange(a, b, h)			        # create array of t_points
height = 0.0						# initial height, velocity, and time = 0
velocity = 0.0
t_i= 0.0
velocity = velocity - 0.5*h*acc(t_i)		        # set the velocity half step back for the leap frog method
velocity_points = []				        # set up empty lists for velocity points and height points
height_points = []

for t in t_points:					# for each time point in t_points
    if t <= 100.0:					# if t is smaller than 100 s (if the fuel is not used up), use the leap frog method to find the next points of velocity and height
        height_points.append(height)	
        velocity_sync = velocity + 0.5*h*acc_g(t)	# velocity is half-step off, so to plot the correct velocity for the correct times we need to append the synced velocity
        velocity_points.append(velocity_sync)
        velocity += h*acc_g(t)
        height += h*velocity
    else:						# if t is greater than 100s, the fuel is used up; velocity does not change.
        height_points.append(height)
        velocity_points.append(velocity)		# append the final velocity at 100s for each of the continuing points
        height += h*velocity				# use the constant velocity to calculate the new height for 100 more seconds.	
        

# plot graph of height vs. time
pl.figure(3)
pl.plot(t_points, height_points, label = 'height')
pl.legend(loc=2)
pl.show()

# plot graph of velocity vs. time
pl.figure(4)
pl.plot(t_points, velocity_points, label = 'velocity')
pl.legend(loc=2)
pl.show()

#----------------------------- Part 3: Air Resistance-----------------------------------------------------------------------------------------------------------------------------------------------------------
# The acceleration we acquired above did not take Air Resistance into account.
# But we know that F_total = F_thrust + F_gravity + F_Air Resistance
# = mass * acceleration - mass * gravity - 0.5 * Pressure * Molar_mass * area_reference * drag_coefficient * (velocity ** 2.0) / (Ideal_Gas * Temperature)
# Adding F_Air Resistance is more complicated than adding F_gravity because there are two dynamin variables that one depends on the other.
# More explanation is written as the code proceeds
# Note that the mass is not the initial mass, but it is changing (losing burn_rate * t kg of mass as time t changes)

Temp_Lapse = 0.0065
Press_Sea = 1.01 * 10 ** 5
Molar_mass = 0.02896
Ideal_Gas = 8.314
height = 0.0
velocity = 0.0

# set initial conditions
a = 0.0							# starting time point
b = 200.0				                # ending time point
N = 10000						# number of steps
h = (b-a)/float(N)					# width of each step interval of time
t_points= np.arange(a, b, h)			        # create array of t_points
height = 0.0						# initial height, velocity, and time = 0
velocity = 0.0
t_i= 0.0
velocity = velocity - 0.5*h*acc(t_i)		        # set the velocity half step back for the leap frog method
velocity_points = []				        # set up empty lists for velocity points and height points
height_points = []

def Temp(height):                                       # Temperature changes based on the height
    return 288.0 - Temp_Lapse * height
    
def grav(height):                                       # Gravity also changes based on the height as mentioned in previous part
    return Grav_earth / (1.0 + height/R_earth) ** 2.0
    
def Press(T,g):                                         # Pressure changes based the temperature and gravity
    return Press_Sea * (T / 288.0) ** (g * Molar_mass/(Ideal_Gas * Temp_Lapse))
    
def Air_Resistance(P,T):                                # Air Resistance changes based on Pressure and Temperature
    if T>=0:
        return -0.5 * P * Molar_mass * area_reference * drag_coefficient * (velocity ** 2.0) / (Ideal_Gas * T)
    else:
        return 0
    
def acc_a(t,AR):
    return (burn_rate * v_exhaust - burn_rate * t * Grav_earth / (1.0 + height/R_earth) ** 2.0 + AR) / (m_0 - burn_rate*t)

for t in t_points:					# for each time point in t_points
    if t <= 100.0:					# if t is smaller than 100 s (if the fuel is not used up), use the leap frog method to find the next points of velocity and height
        height_points.append(height)
        T = Temp(height)                                # The reason why I defined T,g,P,AR as a constant is because when Python calls a function into
        g = grav(height)                                # another function, it gets very complicated and often produces error.
        P = Press(T,g)
        AR = Air_Resistance(P,T)
        velocity_sync = velocity + 0.5*h*acc_a(t,AR)	# velocity is half-step off, so to plot the correct velocity for the correct times we need to append the synced velocity
        velocity_points.append(velocity_sync)
        velocity += h*acc_a(t,AR)
        height += h*velocity
    else:						# if t is greater than 100s, the fuel is used up; velocity does not change.
        height_points.append(height)
        velocity_points.append(velocity)		# append the final velocity at 100s for each of the continuing points
        height += h*velocity
        

# plot graph of height vs. time
pl.figure(5)
pl.plot(t_points, height_points, label = 'height')
pl.legend(loc=2)
pl.show()

# plot graph of velocity vs. time
pl.figure(6)
pl.plot(t_points, velocity_points, label = 'velocity')
pl.legend(loc=2)
pl.show()
