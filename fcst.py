#!/usr/bin/env python2

import urllib2
import json
import time
import datetime
import ConfigParser
import sys
import os

if len(sys.argv) < 2:
	mode = "rain"
else:
	mode = sys.argv[1]



# initialize config file parser
conffile = os.path.expanduser("~/.pyfcio.conf")
config = ConfigParser.ConfigParser()

# load config file
if os.path.isfile(conffile):
	config.read(conffile)
else:
	print "No config file " + conffile + " found. Please create one first ... exiting" 
	sys.exit()

# get forecast.io api key
if config.has_option("Settings", "forecastioApiKey"):
	forecastioApiKey = config.get("Settings", "forecastioApiKey")
else:
	print "Please provide variable `forecastioApiKey` under section [Settings] in file " + conffile + " ... exiting"
	sys.exit()

# get latitude and longitude
if (config.has_option("Settings", "lat") & 
    config.has_option("Settings", "lon")):
	lat = config.get("Settings", "lat")
	lon = config.get("Settings", "lon")
else:
	print "Please provide variables `lat` and `lon` under section [Settings] in file " + conffile + " ... exiting"
	sys.exit()

# get downloadIfOlder option
if (config.has_option("Settings", "downloadIfOlder")):
	downloadIfOlder = float(config.get("Settings", "downloadIfOlder"))
else:
	downloadIfOlder = 120

# set json filename
if (config.has_option("Settings", "jsonFile")):
	jsonfilename = config.get("Settings", "jsonFile")
else:
	jsonfilename = "/tmp/forecastio.json"

# download json file if file doesn't exist or if file is more 
# than `downloadIfOlder` seconds old
downloadnew = False
if not(os.path.isfile(jsonfilename)):
	downloadnew = True
elif (time.time() - os.path.getmtime(jsonfilename) > downloadIfOlder):
	downloadnew = True

if downloadnew:
	url = ('https://api.forecast.io/forecast/' + forecastioApiKey
	       + '/' + str(lat) + ',' + str(lon))
	response = urllib2.urlopen(url)
	fcstData = response.read()
	with open(jsonfilename, 'wb') as jsonFile:
		jsonFile.write(fcstData)

# open json file
with open(jsonfilename, 'r') as jsonFile:
	data = json.load(jsonFile)


if mode == "rain":
	# get precip data from json file
	precipProb = []
	precipIntensity = []
	fcsttime = []
	for d in data["minutely"]["data"]:
		precipProb.append(d["precipProbability"])
		precipIntensity.append(d["precipIntensity"])
		fcsttime.append(d["time"])
	
	# create plot matrix
	width = 61
	height = 17
	
	plotmat = [[" " for i in xrange(width)] for i in xrange(height)]
	for i in xrange(width):
		ppr = precipProb[i]
		plotmat[int(round(ppr * (height-1)))][i] = "*"
	
	# add line above and below plot
	plotmat.insert(0, ["-" for i in xrange(len(plotmat[0]))])
	plotmat.append(["-" for i in xrange(len(plotmat[0]))])
	
	# add x axis ticks
	for i in [0, 15, 30, 45]:
		plotmat[0][i] = "|"
	
	# add x axis labels
	t0 = datetime.datetime.fromtimestamp(fcsttime[0] 
	     + time.timezone).strftime('%H:%M')
	plotmat.insert(0, [" " for i in xrange(len(plotmat[0]))])
	plotmat[0][0:6] = list(t0)
	plotmat[0][16:(16+8)] = list('+15min')
	plotmat[0][31:(31+8)] = list('+30min')
	plotmat[0][46:(46+8)] = list('+45min')
	
	# add left and right border
	plotmat[len(plotmat)-1].insert(0, " ")
	plotmat[1].insert(0," ")
	for i in xrange(2,len(plotmat)-1):
		plotmat[i].insert(0,"|")
		plotmat[i].append("|")
	
	# add y axis ticks and labels
	for i in xrange(len(plotmat)):
		for j in xrange(5):
			plotmat[i].insert(0," ")
	
	plotmat[2][0:6] = list('0.0  :')
	plotmat[6][0:6] = list('0.25 :')
	plotmat[10][0:6] = list('0.5  :')
	plotmat[14][0:6] = list('0.75 :')
	plotmat[18][0:6] = list('1.0  :')
	
	plotmat[2][67] = ':'
	plotmat[6][67] = ':'
	plotmat[10][67] = ':'
	plotmat[14][67] = ':'
	plotmat[18][67] = ':'
	
	
	# print the result
	print ""
	if config.has_option("Settings", "rainheader"):
		rainheader = config.get("Settings", "rainheader")
		print '      ' + rainheader
	print ""
	
	for i in reversed(xrange(len(plotmat))):
		print ''.join(plotmat[i])
	
	print ''.join([' ' for i in xrange(46)]) + '(src: www.forecast.io)'
	print ""
	
else:
	print "unknown mode: "+mode+" ... exiting"
	sys.exit()
	
	
