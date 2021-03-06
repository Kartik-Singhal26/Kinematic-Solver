# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 07:58:25 2020

@author: kartik

This file plots and animate the 3 link manipulator for trajectory tracking application.

"""

import numpy as np
from time import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from three_link_planar import ForwardKin, InvKinematics
from Reference_Trajectory import PointsInCircle, PointsInEight


# Link Length
L1 = int(input('Enter length of Link 1: '))
L2 = int(input('Enter Length of Link 2: '))
L3 = int(input('Enter Length of Link 3: '))
r = int(input('Enter Radius of Trajectory: '))
OffsetX = int(input('Center of Trajectory X axes: '))
OffsetY = int(input('Center of Trajectory Y axes: ')) 

n = 100 # Resolution of moment. High Reso -> More Computation Time

Coord = PointsInEight(r,n)
X = [c[0] + OffsetX for c in Coord]
Y = [c[1] + OffsetY for c in Coord]
i = len(X)

# Initialize Vector for storing Link Coordinates
X1 = []
Y1 = []
X2 = []
Y2 = []
X3 = []
Y3 = []
J1 = []
J2 = []
J3 = []

Errorlog = []

start_time = time()

for k in range(i):  
    
    print('Point number: ', k)
    Theta, Error = InvKinematics(L1, L2, L3, X[k], Y[k])
    Link_Pose = ForwardKin(L1, L2, L3, Theta[0], Theta[1], Theta[2])
    X1.append(Link_Pose['Link1'][0])
    Y1.append(Link_Pose['Link1'][1])
    X2.append(Link_Pose['Link2'][0])
    Y2.append(Link_Pose['Link2'][1])
    X3.append(Link_Pose['Link3'][0])
    Y3.append(Link_Pose['Link3'][1])
    J1.append(Theta[0])
    J2.append(Theta[1])
    J3.append(Theta[2])     
    
    Errorlog.append(Error)

print('Time Taken: %s seconds ' % (time() - start_time))    

# Animate the plot

# Setup Animation Environment
axlimit = L1 + L2 + L3 + 5
fig2 = plt.figure()
anim = fig2.add_subplot(111, aspect = 'equal', autoscale_on = False, xlim = (-axlimit, axlimit), ylim = (-axlimit, axlimit))
anim.grid(color = 'grey', linestyle = '-', linewidth = 0.5)  
plt.title('Kinematic Solver | Trajectory Tracking') 
link1, = anim.plot([], [], 'o-', lw = 4, mew = 5, label = "Link 1", color = 'Green')
link2, = anim.plot([], [], 'o-', lw = 4, mew = 5, label = "Link 2", color = 'Blue')
link3, = anim.plot([], [], 'o-', lw = 4, mew = 5, label = "Link 3", color = 'orange')


time_template = 'Time = %.1fs'
time_text = anim.text(0.02, 0.95, '', transform = anim.transAxes)
Joint1_template = 'Joint 1 Pose = %.1f radians'
Joint2_template = 'Joint 2 Pose = %.1f radians'
Joint3_template = 'Joint 3 Pose = %.1f radians'
Joint1_text = anim.text(0.02, 0.90, '', transform = anim.transAxes)
Joint2_text = anim.text(0.02, 0.85, '', transform = anim.transAxes)
Joint3_text = anim.text(0.02, 0.80, '', transform = anim.transAxes)

dt = 1./100

#plot workspace
plt.plot(X,Y)

def init():
    link1.set_data([], [])
    link2.set_data([], [])
    link3.set_data([], [])
    
    time_text.set_text('')
    Joint1_text.set_text('')
    Joint2_text.set_text('')
    Joint3_text.set_text('')
    return link1, link2, link3, Joint1_text, Joint2_text, Joint3_text, time_text

def animate(a):
    link1_x = X1[a] 
    link1_y = Y1[a]
    link2_x = X2[a] 
    link2_y = Y2[a]
    link3_x = X3[a] 
    link3_y = Y3[a]
    
    link1.set_data([0,link1_x],[0,link1_y])
    link2.set_data([link1_x,link2_x],[link1_y,link2_y])
    link3.set_data([link2_x,link3_x],[link2_y,link3_y])
    
    time_text.set_text(time_template % (a*dt))
    Joint1_text.set_text(Joint1_template % (J1[a]))
    Joint2_text.set_text(Joint2_template % (J2[a]))
    Joint3_text.set_text(Joint3_template % (J3[a]))
 
    return link1, link2, link3, Joint1_text, Joint2_text, Joint3_text, time_text

t0 = time()
animate(0)
t1 = time()
interval = 10000 * dt - (t1 - t0)

ani = animation.FuncAnimation(fig2, animate, np.arange(1, i), interval = interval, blit = True, init_func = init)

ani.save('Trajectory_Tracking.mp4', fps=10)
plt.show()

