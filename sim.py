# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 11:23:50 2017

@author: Rafael
"""

#import numpy as np
diffuswater = 0.143e-2

def D(i,j):
    #dist = dx*np.sqrt((center-i)**2 + (center-j)**2 +(center-k)**2)
    return diffuswater

#fig = plt.figure()
##plt.rc('text', usetex=True)
##plt.rc('font', family='serif')
#ax = fig.add_subplot(111, projection='3d')
#
#ax.set_xlabel('Radius')
#ax.set_ylabel('Time')
#ax.set_zlabel('Temperature')
#
#for t in range(20000):
#    T=compute(T)
#    #string1="Zeit: " + (t*dt) + "     Temperatur: " + (T[center][center][center])
#    if(t%500)==0:
#        print(t*dt)
#        print(T[center,center,center])
#        
#        for x in range(N):
#            ax.scatter(x*dx, t*dt, T[x,center,center],'r')
#        
#    if T[center,center,center] >= targettemp:
#        print(t*dt)
#        print(T[center,center,center])
#        break


def computefield(T):
    Ttemp=T
    global display_size
    global dt
    global dx
    
    N = display_size/10
    
    #boundary conditions fixed?
    for i in range(1,N-1):
        for j in range(1,N-1):
                T[i,j] = Ttemp[i,j] + (D(i,j)*dt/(dx**2))*(Ttemp[i+1,j] + Ttemp[i-1,j] + Ttemp[i,j+1] + Ttemp[i,j-1] + -4*Ttemp[i,j])
    return T