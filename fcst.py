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





#######################################################
# get options from config file
#######################################################

conffile = os.path.expanduser("~/.pyfcio.conf")
config = ConfigParser.ConfigParser()
if os.path.isfile(conffile):
	config.read(conffile)
else:
	print "No config file " + conffile + " found. Please create one first ... exiting" 
	sys.exit()
# forecast.io api key
if config.has_option("Settings", "forecastioApiKey"):
	forecastioApiKey = config.get("Settings", "forecastioApiKey")
else:
	print "Please provide variable `forecastioApiKey` under section [Settings] in file " + conffile + " ... exiting"
	sys.exit()
# latitude and longitude
if (config.has_option("Settings", "lat") & 
    config.has_option("Settings", "lon")):
	lat = config.get("Settings", "lat")
	lon = config.get("Settings", "lon")
else:
	print "Please provide variables `lat` and `lon` under section [Settings] in file " + conffile + " ... exiting"
	sys.exit()
# downloadIfOlder option
if (config.has_option("Settings", "downloadIfOlder")):
	downloadIfOlder = float(config.get("Settings", "downloadIfOlder"))
else:
	downloadIfOlder = 120
# plot height
if (config.has_option("Settings", "plotsize")):
	plotsize = int(config.get("Settings", "plotsize"))
else:
	plotsize = 2
# json filename
if (config.has_option("Settings", "jsonFile")):
	jsonfilename = config.get("Settings", "jsonFile")
else:
	jsonfilename = "/tmp/forecastio.json"



#######################################################
# txtplot function
#######################################################

def txtplot(data, ylim, nyticks=2, yspacer=3, xticksat=[], pch="*"):
	n = len(data)
	m = nyticks + (nyticks - 1) * yspacer 
	plotmat = [[" " for i in xrange(n)] for i in xrange(m)]
	ymin = min(ylim)
	ymax = max(ylim)
	if len(pch) != n:
		pch = [pch[0] for i in xrange(n)]
	# plot the data
	for i in xrange(n):
		j = (float(data[i]) - ymin) / (ymax - ymin) * (m - 1)
		j = int(round(j))
		if (j >= 0 and j < m):
			plotmat[j][i] = pch[i]
	# decorate the plot
	# horizontal lines
	plotmat.insert(0, ["-" for i in xrange(len(plotmat[0]))])
	plotmat.append(["-" for i in xrange(len(plotmat[0]))])
	# x ticks
	for i in xticksat:
		if i >=0 and i < len(plotmat[0]):
			plotmat[0][i] = "|"
	# vertical lines with ticks
	vline = ["|" for i in xrange(m)]
	yticksat = [i for i in xrange(0, m, yspacer+1)]
	for i in yticksat:
		vline[i] = ":"
	vline.insert(0, " ")
	vline.append(" ")
	for i in xrange(len(vline)):
		plotmat[i].insert(0, vline[i])
		plotmat[i].append(vline[i])
	# y tick labels
	dy = float((ymax - ymin)) / (nyticks - 1)
	ytickvals = [float(ymin + i * dy) for i in xrange(nyticks)]
	yticklabels = []
	yticklabellen = []
	for i in xrange(len(ytickvals)):
		s = list(str(round(ytickvals[i], 2)))
		yticklabels.append(s)
		yticklabellen.append(len(s))
	for i in xrange(len(plotmat)):
		for j in xrange(max(yticklabellen)+1):
			plotmat[i].insert(0, " ")
	for i in xrange(len(yticksat)):
		itick = yticksat[i] + 1
		plotmat[itick][0:len(yticklabels[i])] = yticklabels[i]
	# return 
	return plotmat




#######################################################
# download and open json file 
#######################################################

# if file doesn't exist or if file is more 
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
with open(jsonfilename, 'r') as jsonFile:
	data = json.load(jsonFile)






#######################################################
# 60 minutes precipitation forecast
#######################################################

if mode == "rain":
	# get precip data from json file
	precipProb = []
	precipIntensity = []
	fcsttime = []
	pch = []
	for d in data["minutely"]["data"]:
		precipProb.append(d["precipProbability"])
		pri = d["precipIntensity"] * 25.4
		if pri < 1:
			pch.append(".")
		elif pri < 2:
			pch.append("o")
		elif pri < 5:
			pch.append("X")
		else:
			pch.append("#")
		fcsttime.append(d["time"])

	# plot
	plotmat = txtplot(data=precipProb, ylim=[0,1], 
	                  nyticks=5, yspacer=plotsize, 
	                  xticksat=[0, 15, 30, 45], pch=pch)
	
	# add x axis labels
	t0 = datetime.datetime.fromtimestamp(fcsttime[0] 
	     + time.timezone).strftime('%H:%M')
	plotmat.insert(0, [" " for i in xrange(len(plotmat[0]))])
	plotmat[0][6:12] = list(t0)
	plotmat[0][21:(21+6)] = list('+15min')
	plotmat[0][36:(36+6)] = list('+30min')
	plotmat[0][51:(51+6)] = list('+45min')
	



#######################################################
# 48 hours temperature forecast
#######################################################
	
elif mode=="temp":
	
	temp = []
	fcsttime = []
	fcstday = []
	for d in data["hourly"]["data"]:
		tmp = (d["temperature"] - 32.0) * 5.0 / 9.0
		tmp = round(tmp, 1)
		temp.append(tmp)
		tim = d["time"] + time.timezone
		tim = datetime.datetime.fromtimestamp(tim)
		fcsttime.append(tim.strftime("%H:%M"))
		fcstday.append(tim.strftime("%a"))

	ymin = math.floor(min(temp) / 2.5) * 2.5
	ymax = math.ceil(max(temp) / 2.5) * 2.5
	nytix = int((ymax - ymin) / 2.5) + 1

	xtixat = []
	xtix = []
	for i,t in enumerate(fcsttime):
		if t == "00:00":
			xtixat.append(i)
			xtix.append(fcstday[i])
		if t == "12:00":
			xtixat.append(i)
			xtix.append(t)
	
	plotmat = txtplot(data=temp, ylim=[ymin,ymax], 
	                  nyticks=nytix, yspacer=plotsize, 
	                  xticksat=xtixat)

	plotmat.insert(0, [" " for i in xrange(len(plotmat[0])+2)])
	for i in xrange(len(xtixat)):
		tic = list(xtix[i])
		itic = xtixat[i] + 5
		plotmat[0][itic:(itic + len(tic))] = tic





#######################################################
# 48 hours rain forecast
#######################################################
	
elif mode=="rain2":
	
	rain = []
	fcsttime = []
	fcstday = []
	pch = []
	for d in data["hourly"]["data"]:
		pr = d["precipProbability"] 
		rain.append(pr)
		tim = d["time"] + time.timezone
		tim = datetime.datetime.fromtimestamp(tim)
		fcsttime.append(tim.strftime("%H:%M"))
		fcstday.append(tim.strftime("%a"))
		pri = d["precipIntensity"] * 25.4
		if pri < 1:
			pch.append(".")
		elif pri < 2:
			pch.append("o")
		elif pri < 5:
			pch.append("X")
		else:
			pch.append("#")

	xtixat = []
	xtix = []
	for i,t in enumerate(fcsttime):
		if t == "00:00":
			xtixat.append(i)
			xtix.append(fcstday[i])
		if t == "12:00":
			xtixat.append(i)
			xtix.append(t)
	
	plotmat = txtplot(data=rain, ylim=[0,1], 
	                  nyticks=5, yspacer=plotsize, 
	                  xticksat=xtixat, pch=pch)

	plotmat.insert(0, [" " for i in xrange(len(plotmat[0])+2)])
	for i in xrange(len(xtixat)):
		tic = list(xtix[i])
		itic = xtixat[i] + 5
		plotmat[0][itic:(itic + len(tic))] = tic





#######################################################
# print current conditions
#######################################################

elif mode == 'now':
	d = data['currently']
	if not 'summary' in d: summary = ''
	else: summary = d['summary']
	if not 'temperature' in d: temperature = ''
	else: temperature = str(round((d['temperature'] - 32.0) 
	                             * 5.0 / 9.0, 1)) + ' C'
	if 'apparentTemperature' in d: 
		apptemp = round((d['apparentTemperature'] - 32.0) * 5.0 / 9.0, 1)
		temperature = temperature + ' (feels like ' + str(apptemp) + ' C)'
	if not 'precipType' in d: d['precipType'] = 'rain'
	if not 'precipIntensity' in d: d['precipIntensity'] = 0
	if d['precipIntensity'] <= 0: precip = 'none'
	else: precip = d['precipType'] + ' ' + str(round(d['precipIntensity'] * 25.4, 2)) + ' mm/h'
	if not 'windSpeed' in d: windSpeed = '? km/h'
	else: windSpeed = str(int(d['windSpeed'] * 1.6093)) + ' km/h '
	if not 'windBearing' in d: windBearing = ''
	else: 
		windBearing = ['N','NE','E','SE','S','SW', 
	                     'W', 'NW', 'N'][int(d["windBearing"] / 45.0)]
	wind = windSpeed + windBearing
	if not 'humidity' in d: humidity = ''
	else: humidity = str(int(d['humidity'] * 100.0)) + ' %'
	
	out = [
	('  Summary:', summary),
	('  Temperature:', temperature),
	('  Precipitation:', precip),
	('  Humidity:', humidity),
	('  Wind: ', wind)]
	
	tnow = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M')
	print ""
	print 'Current weather conditions at ' + tnow
	print ""
	out2 = [[s.ljust(max(len(i) for i in column)) for s in column] for column in zip(*out)]
	for p in ["  ".join(row) for row in zip(*out2)]: print p
	print ""


else:
	print "unknown mode: "+mode+" ... exiting"
	sys.exit()
	





#######################################################
# print plot matrix
#######################################################

if not mode == "now":
	print ""
	for i in reversed(xrange(len(plotmat))):
		print ''.join(plotmat[i])
	idx = max(0, len(plotmat[1])-22)
	print ''.join([' ' for i in xrange(idx)]) + '(src: www.forecast.io)'
	print ""



