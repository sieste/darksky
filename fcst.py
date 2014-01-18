#!/usr/bin/env python2

import urllib2
import json
import time
import datetime
import ConfigParser
import sys
import os
import math

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

# plot height
if (config.has_option("Settings", "plotsize")):
	plotsize = int(config.get("Settings", "plotsize"))
else:
	plotsize = 2

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
	height = 5 + plotsize * 4
	
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
	
	labls = ['0.0  :', '0.25 :', '0.5  :', '0.75 :', '1.0  :']
	for i in xrange(5):
		plotmat[2 + i * (plotsize + 1)][0:6] = list(labls[i])
		plotmat[2 + i * (plotsize + 1)][67] = ':'
	
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
	
elif mode=="temp":
	plotheight = 17
	plotwidth = 49

	temp = []
	fcsttime = []
	for d in data["hourly"]["data"]:
		temp.append(d["temperature"])
		fcsttime.append(d["time"])
	
	
	# transform to celsius
	for i in xrange(len(temp)):
		temp[i] = (temp[i] - 32) * 5 / 9
		temp[i] = round(temp[i], 1)
	
	
	# y limits (min and max rounded to nearest multiple of `dy`)
	dy = 2.5
	ymin = math.floor(min(temp) / dy) * dy
	ymax = math.ceil(max(temp) / dy) * dy
	
	# y label every `dy` degrees
	nlabels = int((ymax - ymin) / dy) + 1
	labels = [ymin + dy * x for x in xrange(0, nlabels)]
	ilabels = [int(round(x * (plotheight-1) / (nlabels-1))) 
	           for x in xrange(0, nlabels)]
	labelstr = []
	for i in xrange(len(labels)):
		st = list(str(labels[i]))
		st = st + [' ' for i in range(6 - len(st))]
		labelstr.append(st)
	
	# x labels
	xlinevec = []
	xlabinds = []
	xlabs = []
	for i in xrange(len(fcsttime)):
		t = datetime.datetime.fromtimestamp(fcsttime[i] + time.timezone)
		h = int(t.strftime('%H'))
		day = t.strftime('%a')
		hh = t.strftime('%H:%M')
		if (h % 6 == 0):
			xlinevec.append(i)
		if (h == 0):
			xlabinds.append(i)
			xlabs.append(list(day))
		if (h == 12):
			xlabinds.append(i)
			xlabs.append(list(hh))
	
	t0 = datetime.datetime.fromtimestamp(fcsttime[0] 
	       + time.timezone).strftime('%H:%M')
	
	# plot it
	plotmat = [[" " for i in xrange(plotwidth)] for i in xrange(plotheight)]
	for i in xrange(plotwidth):
		#if i in xlinevec:
			#for j in xrange(plotheight):
				#plotmat[j][i] = "."
		#for j in ilabels[1:-1]:
			#plotmat[j][i] = "."
		plotmat[int((temp[i] - ymin) / (ymax - ymin) * (plotheight - 1))][i] = "*"
	
	# add line on top and bottom
	plotmat.insert(0, ["-" for i in xrange(len(plotmat[0]))])
	plotmat.append(["-" for i in xrange(len(plotmat[0]))])
	
	# add x axis ticks
	for i in xlabinds:
		plotmat[0][i] = "|"
	
	plotmat.insert(0, [" " for i in xrange(len(plotmat[0]))])
	
	# add 4 empty columns and label x axis
	for i in xrange(len(plotmat)):
		for j in xrange(4):
			plotmat[i].append(" ")
	for i in xrange(len(xlabinds)):
		ii = max(0, xlabinds[i]-1)
		plotmat[0][ii:(ii+4)] = xlabs[i]
	
	# add vertical lines
	plotmat[len(plotmat)-1].insert(0, " ")
	plotmat[1].insert(0," ")
	for i in xrange(2,len(plotmat)-1):
		plotmat[i].insert(0,"|")
		plotmat[i][plotwidth+1] = "|"
	
	# add y axis ticks and labels
	for i in xrange(len(plotmat)):
		for j in xrange(6):
			plotmat[i].insert(0," ")
	
	for i in xrange(len(ilabels)):
		ii = ilabels[i]+2
		st = list(str(labels[i]))
		plotmat[ii][0:(len(st))] = st
		plotmat[ii][6] = ":"
		plotmat[ii][56] = ":"
	
	# print
	print ""
	print "       Temperature forecast for Exeter, Devon, UK"
	print ""
	for i in reversed(xrange(len(plotmat))):
		print ''.join(plotmat[i])
	print ''.join([' ' for i in xrange(35)]) + '(src: www.forecast.io)'
	print ""

else:
	print "unknown mode: "+mode+" ... exiting"
	sys.exit()
	

	
