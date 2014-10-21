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