import csv, math
from collections import OrderedDict

a = 0 # bullshit variable for no reason, sorry

# the point class. 
# each point is a station with routes that pass through it.
class Point:
	def __init__(self, division, line, station_name, station_latitude,\
	 station_longitude):
		self.division = division
		self.line = line
		self.station_name = station_name
		self.station_latitude = float(station_latitude)
		self.station_longitude = float(station_longitude)
		self.routes = []
	def getLocation(self):
		return [self.station_latitude, self.station_longitude]
	def addToRoutes(self, x):
		self.routes.append(x)
	def getRoutes(self):
		return self.routes
	def getDivision(self):
		return self.division
	def getLine(self):
		return self.line
	def getStationName(self):
		return self.station_name
	def __eq__(self, other):
		return self.station_latitude==other.station_latitude\
			and self.station_longitude==other.station_longitude
	def __hash__(self):
		return hash(\
			('lat', self.station_latitude, 'long', self.station_longitude)\
		)

# the line class. 
# each line is a letter and has a number of points it goes through
class Line:
	def __init__(self, name, firstStation):
		self.name = name
		self.firstStation = firstStation
		self.points = []
	def add(self, point):
		self.points.append(point)
	def printLine(self):
		for point in self.points:
			print point.getStationName()

# find the distance between two points.
# expects locations of the form [latitude, longitude]
def calcDist(a, b):
	# a = [x1, y1], b = [x2, y2]
	return math.hypot(b[0] - a[0], b[1] - a[1]) # p y t h a g o r a s

# create data and linesList.
data = [] # data contains all points
linesList = [] # linesList contains text strings with the names of all lines

with open('StationEntrances.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	spamreader.next()
	for row in spamreader:
		p = Point(row[0], row[1], row[2], row[3], row[4]) # manual assignment
		for i in range(5, 15): # add all possible routes through a station
			if row[i]:
				p.addToRoutes(row[i])
				if row[i] not in linesList: # add to line to linesList 
					linesList.append(row[i])
		data.append(p) # add point to data


data = set(data) # eliminate duplicates
linesList = sorted(linesList) # alphabetize linesList, idk why

# create byLines array, which contains many arrays of points
# each in the nominal line but in no set order
byLine = {}
for line in linesList:
	byLine[line] = []
for point in data: # the completists' approach to assembling lineslist.
	for route in point.getRoutes():
		byLine[route].append(point)
# for point in byLine['7']:
# 	print point.getStationName()

def makeLinkedLine(name, firstStation):
	currentLine = Line(name, firstStation)
	toVisit = []
	for point in byLine[name]:
		if point.getStationName() == firstStation:
			currentLine.add(point)
		else :
			toVisit.append(point)
	print 'currently assembling the ' + name + ' line, starting at '\
	 + currentLine.points[0].getStationName()

	# try to find the next closest point to the starting point
	# predicated on there being no switchbacks, possibly an unsafe assumption
	atPoint = currentLine.points[0]
	while len(toVisit) > 0:
		trials = {}
		bestDist = 2
		for point in toVisit:
			trialDist = calcDist(point.getLocation(), atPoint.getLocation())
			trialPoint = point
			if trialDist < bestDist:
				bestPoint = trialPoint
				bestDist = trialDist
		currentLine.add(bestPoint)
		toVisit.remove(bestPoint)
		atPoint = currentLine.points[-1]
	return currentLine


allLines = {}
startingPoints = {
	  '1' : 'South Ferry'
	, '2' : 'Flatbush Av-Brooklyn College'
	, '3' : 'New Lots Av'
	, '4' : 'Utica Av'
	, '5' : 'Flatbush Av-Brooklyn College'
	, '6' : 'Brooklyn Bridge-City Hall'
	, '7' : '42nd St'
	, 'A' : 'Lefferts Blvd'
	, 'AS': 'Far Rockaway-Mott Av'
	, 'B' : 'Brighton Beach'
	, 'C' : 'Euclid Av'
	, 'D' : 'Stillwell Av'
	, 'E' : 'World Trade Center'
	, 'F' : 'Jamaica-179th St'
	, 'FS': 'Prospect Park'
	, 'G' : 'Long Island City-Court Square'
	, 'GS' : 'Grand Central-42nd St'
	, 'H' : 'Rockaway Park-Beach 116th'
	, 'J' : 'Broad St'
	# , 'L' : '14 St' # HERE IS THE PROBLEM. STATION NAMES ARE NOT UNIQUE.
	# IT IS PROBABLE THAT STATION NAMES /and/ LINE NAMES ARE
	# USE THAT TO MATCH FROM NOW ON
	# IT MAY ALSO ELIMINATE YOUR DUPLICATES
}

for line in linesList:
	if line in startingPoints:
		allLines[line] = makeLinkedLine(line, startingPoints[line])
	else:
		# line = line
		print line



# for point in allLines['J'].points:
	# print point.getStationName()
	# print point.getStationName() , '\t' , point.getLocation()[0], '\t', point.getLocation()[1], '\t'

