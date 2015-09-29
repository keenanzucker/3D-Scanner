import serial
from math import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

ser= serial.Serial('/dev/ttyACM0') #collect data from Arduino

fig = plt.figure()	#initialize 3d figure
ax = fig.add_subplot(111, projection='3d')

X = []	#empty arrays to gather data
Y = []
Z = []

now = time.time() #set time limit for scan
future = now + 140

plt.ion()	#enable interactive plotting for real-time plotting
plt.show()
ax.set_xlabel('X axis') #create axes labels
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')

while True:
	if time.time() > future: #end after 140s
		break

	line = ser.readline() #collect Arduino data and parse
	line = line[:-3]
	dis= line.split(',')

	theta = ((float(dis[0])+20)*pi)/180.0 #convert to floats and radians
	phi = -((float(dis[1])-92)*pi)/180.0
	r = float(dis[2])

	x = r*cos(theta)*cos(phi) #convert spherical coordinates to rectangular
	y = r*sin(theta)*cos(phi)
	z = r*sin(phi)
	# print [x,y,z]

	if r > 15.0 and r < 50: #remove uncalibrated and irrelevant data
		X.append(x)		#store data for permanent plot
		Y.append(y)
		Z.append(z)
		ax.scatter(x, y, z)	#plot point
		ax.set_zlim([-10, 20]) #set axes limits
		ax.set_xlim([-30,30])
		ax.set_ylim([-30,30])
		plt.draw()
	else:
		pass

plt.ioff()	#create a permanent plot from collected data
ax.set_xlabel('X axis') #create axes labels
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.scatter(X, Y, Z)	#plot points
plt.show()
