import matplotlib.pyplot as plt
import pylab
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import serial
import re
import numpy as np

port = '/dev/ttyACM0'									# Arduino Port Number
frequency = '9600'

ser = serial.Serial(port,frequency)  					# Setup Serial port to connect to Arduino


def getData():
	"""Reads the serial port from the Arduino and returns the 
		list of three element lists """
	rawData = []
	for i in range(0,200): 								# Number of samples to take
		rawData.append(ser.readline().split(' ')[:3])

	return rawData

def removeBuffer(rawPoints):
	""" Removes the serial buffer from the raw data by searching for the 
		elements that we want to see first. Returns the clean points"""
	beginning = 0
	points = []
	for j in range(0,len(rawPoints)):
		for k in range(0, len(rawPoints[j])):
			if rawPoints[j][0] == '-30':				# Wherever pan is starting
				if rawPoints[j][1] == '100':			# Wherever tilt is starting
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
		distance[j] = float(distance[j])

	return [theta, phi, distance]

def translateCoordinates(points):
	""" Turns the points from spherical coordinates to 
		Cartesian coordinates to be able to plot"""
	
	theta = np.radians(np.subtract(180, points[0]))
	phi = np.radians(points[1])

	x = np.multiply(points[2], np.multiply(np.sin(theta), np.cos(phi)))
	y = np.multiply(points[2], np.multiply(np.sin(theta), np.sin(phi)))
	z = np.multiply(points[2], np.cos(theta))

	print [x,y,z]
	return [x,y,z]

def createPlot(points):
	""" Generates the 3D scatter plot of the scan"""
	fig = pylab.figure()
	ax = Axes3D(fig)

	ax.set_xlabel('X Sweep Position')
	ax.set_ylabel('Y Sweep Position')
	ax.set_zlabel('Distance')

	ax.scatter(points[0], points[1], points[2])
	pyplot.show()


if __name__ == '__main__':
	""" Runs the whole thang!"""
	data = []

	data = getData()
	data = removeBuffer(data)

	createPlot(translateCoordinates(createCoordinates(data)))
