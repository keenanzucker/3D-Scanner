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

points = []
output = []

for i in range(0,200):
	points.append(ser.readline().split(' ')[:3])

def removeBuffer(rawPoints):
	for j in range(0,len(rawPoints)):
		for k in range(0, len(rawPoints[j])):
			if rawPoints[j][0] == '0':
				if rawPoints[j][1] == '60':
					beginning = j
	rawPoints = rawPoints[beginning:]

	return rawPoints

points = removeBuffer(points)

for a in points:
	xs.append(float(a[0]))
	ys.append(float(a[1]))
	zs.append(re.findall("\d+.\d+", a[2]))

zs = [y for x in zs for y in x]

for b in range(0,len(zs)):
	zs[b] = float(zs[b])

# for h in points:

# 	xcord = float(h[2]) * math.sin(math.radians(float(h[0])))

# 	ycord = float(h[2]) * math.sin(math.radians(float(h[1])))

# 	xs.append(float(xcord))
# 	ys.append(float(ycord))
# 	zs.append(float(h[2]))

print xs
print ys
print zs

fig = pylab.figure()
ax = Axes3D(fig)

ax.set_xlabel('X Sweep Position')
ax.set_ylabel('Y Sweep Position')
ax.set_zlabel('Distance')

ax.scatter(xs,ys,zs)
pyplot.show()