import matplotlib.pyplot as plt
import pylab
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import serial
import re
import numpy as np
from matplotlib import cm

port = '/dev/ttyACM0'									# Arduino Port Number
frequency = '9600'

ser = serial.Serial(port,frequency)  					# Setup Serial port to connect to Arduino


def getData():
	"""Reads the serial port from the Arduino and returns the 
		list of three element lists """
	rawData = []
	for i in range(0,2400): 								# Number of samples to take
		rawData.append(ser.readline().split(' ')[:3])

	return rawData

def removeBuffer(rawPoints):
	""" Removes the serial buffer from the raw data by searching for the 
		elements that we want to see first. Returns the clean points"""
	beginning = 0
	points = []
	for j in range(0,len(rawPoints)):
		for k in range(0, len(rawPoints[j])):
			if rawPoints[j][0] == '0':				# Wherever pan is starting
				if rawPoints[j][1] == '90':			# Wherever tilt is starting
					beginning = j
	points = rawPoints[beginning:]

	return points

def createCoordinates(points):
	"""Turns the list within list into floats rather than strings
		and get rid of escape characters. Returns three arrays: theta -- which 
		is x angle, phi -- which is y angle, and distance """

	theta = []
	phi = []
	distance = []

	for i in points:
		theta.append(float(i[0]))
		phi.append(float(i[1]))
		distance.append(re.findall("\d+.\d+", i[2]))	# Removes escape characters using regular expression 

	distance = [y for x in distance for y in x]

	for j in range(0,len(distance)):
		#if (distance[j] < 100):
		distance[j] = float(distance[j])

	return [theta, phi, distance]


def translateCoordinates(points):
	""" Turns the points from spherical coordinates to 
		Cartesian coordinates to be able to plot"""

	#theta = np.radians(np.absolute(np.subtract(points[0], 30)))
	#phi = np.radians(np.absolute(np.subtract(points[1], 120)))

	theta = np.radians(points[0])
	phi = np.radians(points[1])

	x = np.multiply(points[2], np.multiply(np.sin(theta), np.cos(phi)))
	y = np.multiply(points[2], np.multiply(np.sin(theta), np.sin(phi)))
	z = np.multiply(points[2], np.cos(theta))

	# x = np.multiply(points[2], np.multiply(np.cos(theta), np.cos(phi)))
	# y = np.multiply(points[2], np.multiply(np.sin(theta), np.cos(phi)))
	# z = np.multiply(points[2], np.sin(phi))

	print [x,y,z]
	return [x,y,z]

def colorcode(scans):
		"""Color codes points, sets blue if y distance is greater than threshold"""
		colors = []
		for scan in scans:
			if scan > 30:
				colors.append('r')
			else:
				colors.append('b')
		return colors

def size(scans):
	"""sizes points"""
	sizes = []
	for scan in scans:
		if scan > 30:
			sizes.append(20)
		else:
			sizes.append(40)
	return sizes

def createPlot(points):
	""" Generates the 3D scatter plot of the scan"""

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	ax.set_xlabel('X (cm)')
	ax.set_ylabel('Y (cm)')
	ax.set_zlabel('Z (cm)')
	color = colorcode(points[2])
	sizes = size(points[2])
	ax.scatter(points[0], points[1], points[2], c=color, s = sizes)
	fig.canvas.draw()
	plt.show()


if __name__ == '__main__':
	""" Runs the whole thang!"""
	data = []

	data = getData()
	data = removeBuffer(data)

	#createPlot(translateCoordinates(createCoordinates(data)))
	createPlot(createCoordinates(data))
