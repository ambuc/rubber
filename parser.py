# using data from https://data.cityofnewyork.us/Transportation/Subway-Stations/arq3-7z49

from fastkml import kml #kml parses kml
import xml.etree.ElementTree as ET #ET parses inside xml
with open ("data.kml", "r") as myfile:
    doc = myfile.read().replace('\n', '')

k = kml.KML() # new kml object
k.from_string(doc) # read file to kml object
features = list(k.features()) # list object
placemarks = list(features[0].features()) # list object of Placemarks
stations = [] # array of stations

for elem in placemarks: 
	local = {} # local dictionary
	root = ET.fromstring("<desc>" + elem.description + "</desc>")
	local['name'] = root[1][0][1].text
	local['stats'] = root[1][2][1].text
	local['coor'] = elem.geometry._coordinates
	stations.append(local)

xvals = [];  yvals = []

for elem in stations:
	xvals.append(elem['coor'][0])
	yvals.append(elem['coor'][1])

import matplotlib.pyplot as plt

plt.plot(xvals, yvals, 'ko', mew=0, ms=1.5)

plt.axes().set_aspect('equal', 'datalim')
plt.show()
