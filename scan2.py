import matplotlib.pyplot as plt
import pylab
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import random
import math
import serial
import syslog
import time
import re


port = '/dev/ttyACM0'
frequency = '9600'

ser = serial.Serial(port,frequency)

xs = []
ys = []
zs = []
d = []

points = []
output = []

for i in range(0,200):
	points.append(ser.readline().split(' ')[:3])

def removeBuffer(rawPoints):
	beginning = 0
	for j in range(0,len(rawPoints)):
		for k in range(0, len(rawPoints[j])):
			if rawPoints[j][0] == '-30':			# Wherever pan is starting
				if rawPoints[j][1] == '100':		# Wherever tilt is starting
					beginning = j
	rawPoints = rawPoints[beginning:]

	return rawPoints

points = removeBuffer(points)
#print points

for a in points:
	xs.append(float(a[0]))
	ys.append(float(a[1]))
	d.append(re.findall("\d+.\d+", a[2]))

d = [y for x in d for y in x]

for b in range(0,len(d)):
	d[b] = float(d[b])

print xs
print ys
print d

for c in range(0,len(xs)):

	zs[c] = d[c] * math.cos(math.radians(xs[c]))

	xs[c] = d[c] * math.sin(math.radians(xs[c]))

	ys[c] = d[c] * math.sin(math.radians(ys[c]))


fig = pylab.figure()
ax = Axes3D(fig)

ax.set_xlabel('X Sweep Position')
ax.set_ylabel('Y Sweep Position')
ax.set_zlabel('Distance')

ax.scatter(xs,ys,zs)
pyplot.show()