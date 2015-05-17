import csv

data = []
lineslist = []

class Point:
	def __init__(self, division, line, station_name, station_latitude, station_longitude):
		self.division = division
		self.line = line
		self.station_name = station_name
		self.station_latitude = station_latitude
		self.station_longitude = station_longitude
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
		return hash(('lat', self.station_latitude, 'long', self.station_longitude))

with open('StationEntrances.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	spamreader.next()
	for row in spamreader:
		p = Point(row[0], row[1], row[2], row[3], row[4])
		for i in range(5, 15):
			if row[i]:
				p.addToRoutes(row[i])
				if row[i] not in lineslist:
					lineslist.append(row[i])
		data.append(p)

data = set(data)
lineslist = sorted(lineslist)
byline = {}
for line in lineslist:
	byline[line] = []
for point in data:
	for route in point.getRoutes():
		byline[route].append(point)

for point in byline['1']:
	print point.getStationName()

# print lineslist
# print data
# print len(data)
# for item in data:
	# print item.getLine(), item.getStationName(), item.getLocation(), item.getRoutes()
