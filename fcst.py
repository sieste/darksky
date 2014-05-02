#!/usr/bin/env python2

import urllib2
import json
import time
import datetime
import ConfigParser
import argparse 
import sys
import os
import math


##################################################
# Conversion of the units
##################################################

def celsius(F):
	"""Converts the temperature in Farenheit to Celsius"""
	return (F - 32.0) * 5.0 / 9.0
	



#######################################################
# txtplot function
#######################################################

def txtplot(data, ylim, nyticks=2, yspacer=3, xticksat=[], xmticksat=[], pch="*"):
	""" 
	Create the ascii plot on the console.

	Input parameters:
	-----------------
	data		- list of x-values to be printed
	ylim		- lower and upper limit of printed data
	nyticks		- number of ticks in y axis
	nxticks		- number of ticks in x axsis
	xticksat	- list of location for the ticks
	xmticksat	- list of location for the minor ticks
	pch		- list of symbols to be shown (for intensity)
	"""
	
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
	
	# x minor ticks
	for i in xmticksat:
		if i >=0 and i < len(plotmat[0]):
			plotmat[0][i] = "+"


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

	return plotmat









#######################################################
# get options from command line
#######################################################

# the config file has to be created. The options specified
# in the config file are overwriten by the comman line options.

# initialize the parser
parser = argparse.ArgumentParser(#usage="%(prog)s [options]",
                                 description="Command line forcast.")

# forecast mode
parser.add_argument("mode",type=str, 
		    nargs="?", 
		    default="rain",
                    help="forecast mode [rain | rain2 | now]")

# config file
parser.add_argument("-f",
		    "--file", 
		    nargs="?",
		    type=str,
		    default = "~/.pyfcio.conf",
                    help="config file")

# forcastio Api Key
parser.add_argument("-k",
		    "--key", 
		    nargs="?", 
		    type=str,
		    help="user key to the forecastio database")

# location key
parser.add_argument("-l",
		    "--location", 
		    nargs="?", 
		    type=str,
		    default = "Settings",
		    help="location defined in the config file")

# force new download of the data file
parser.add_argument("-d",
		    "--download", 
		    action = "store_true",
		    help="force new download of the data file")


# output verbosity
parser.add_argument("-v",
		    "--verbose",
		    action="store_true",
                    help="verbose output")

# parse arguments into args variable.
args = parser.parse_args()

# capitalize the location
args.location = args.location.capitalize() 


# show what has been parsed
if args.verbose:
	print "Verbose mode"
	print "---------------------------------------------------------"
	print "The following arguments were parsed from the command line"
	print "---------------------------------------------------------"
	print "Config file:\t", args.file
	print "Forecast mode:\t" , args.mode
	print "User key:\t", args.key
	print "Location:\t", args.location
	print







#######################################################
# get options from config file
#######################################################


conffile = os.path.expanduser(args.file)
config = ConfigParser.ConfigParser()

# Read config file
if os.path.isfile(conffile):
	if args.verbose:
		print "Parsing the config file options from " + args.file

	try:
		config.read(conffile)
	except:
		print "Error reading config file " + conffile + "... exiting"
		sys.exit(1)
else:
	print "No config file " + conffile + " found. Please create one first ... exiting" 
	sys.exit(1)



# forecast.io api key
if args.key:
	forecastioApiKey = args.key
elif config.has_option("Settings", "forecastioApiKey"):
	forecastioApiKey = config.get("Settings", "forecastioApiKey")
else:
	print "Please provide variable `forecastioApiKey` under section [Settings] in file "\
	    + conffile + "or specify the --key command line option."
	sys.exit(1)


# latitude and longitude
if (config.has_option(args.location, "lat") & 
    config.has_option(args.location, "lon")):
	lat = config.get(args.location, "lat")
	lon = config.get(args.location, "lon")
else:
	print "Please provide location variables `lat` and `lon` under section [" + args.location + \
	    "] in file " + conffile + " ... exiting"
	sys.exit(1)


# # downloadIfOlder option
# # maybe it would be enough to have hard coded 120s and the forced download command line option
# if (config.has_option("Settings", "downloadIfOlder")):
# 	downloadIfOlder = float(config.get("Settings", "downloadIfOlder"))
# else:
# 	downloadIfOlder = 120
downloadIfOlder = 120


# plot height
if (config.has_option("Settings", "plotsize")):
	plotsize = int(config.get("Settings", "plotsize"))
else:
	plotsize = 2


# json filename
if (config.has_option("Settings", "jsonFile")):
	# the jsonFile has to contain %s in the string
	try:
		jsonfilename = config.get("Settings", "jsonFile") % args.location
	except TypeError:
		print "The filename jsonFile in the [Settings] section in the config file: " + args.file +\
		    " Must include '%s'"
		print "Using default file"
		jsonfilename = "/tmp/forecastio"+ args.location +".json"
		
else:
	jsonfilename = "/tmp/forecastio"+ args.location +".json"








#######################################################
# download and open json file 
#######################################################

# if file doesn't exist or it's more than `downloadIfOlder` 
if not (os.path.isfile(jsonfilename)) \
    or  (time.time() - os.path.getmtime(jsonfilename) > downloadIfOlder) \
    or args.download:

	if args.verbose:
		print "Downloading the data."

 	url = ('https://api.forecast.io/forecast/' + forecastioApiKey
 	       + '/' + str(lat) + ',' + str(lon))
	try:
 		response = urllib2.urlopen(url)
	except:
		print "Connection failed."
		sys.exit(1)
 	fcstData = response.read()
	
	data = json.loads(fcstData)  # converts to the required format

 	with open(jsonfilename, 'wb') as jsonFile:
 		jsonFile.write(fcstData)
else:
	# load the data from the file
	with open(jsonfilename, 'r') as jsonFile:
		data = json.load(jsonFile)








#######################################################
# 60 minutes precipitation forecast
#######################################################

if args.mode == "rain":
	try:
		mData = data["minutely"]["data"]
	except KeyError:
		print "The data for minutely precision are not available for this location ("\
		    + args.location + ")."
		sys.exit(1)

	# get precip data from json file
	precipProb = []
	precipIntensity = []
	fcsttime = []
	pch = []
	for d in mData:
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
	plotmat = txtplot(data=precipProb, 
			  ylim=[0,1], 
	                  nyticks=5, 
			  yspacer=plotsize, 
	                  xticksat=[0, 15, 30, 45], 
			  pch=pch)
	
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
	
elif args.mode=="temp":
	try:
		hData = data["hourly"]["data"]
	except KeyError:
		print "The data for hourly precision are not available for this location ("\
		    + args.location + ")."
		sys.exit(1)

	
	temp = []
	fcsttime = []
	fcstday = []

	for d in hData:
		tmp = celsius(d["temperature"])
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
	xmtixat = []
	xtix = []
	for i,t in enumerate(fcsttime):
		if t == "00:00":
			xtixat.append(i)
			xtix.append(fcstday[i])
		if t == "12:00":
			xtixat.append(i)
			xtix.append(t)
		if t == "06:00" or t == "18:00":
			xmtixat.append(i)

	
	plotmat = txtplot(data=temp, 
			  ylim=[ymin,ymax], 
	                  nyticks=nytix, 
			  yspacer=plotsize, 
			  xmticksat = xmtixat,
	                  xticksat=xtixat)

	plotmat.insert(0, [" " for i in xrange(len(plotmat[0])+2)])
	for i in xrange(len(xtixat)):
		tic = list(xtix[i])
		itic = xtixat[i] + 5
		plotmat[0][itic:(itic + len(tic))] = tic





#######################################################
# 48 hours rain forecast
#######################################################
	
elif args.mode=="rain2":
	try:
		hData = data["hourly"]["data"]
	except KeyError:
		print "The data for hourly precision are not available for this location ("\
		    + args.location + ")."
		sys.exit(1)

	rain = []
	fcsttime = []
	fcstday = []
	pch = []
	for d in hData:
		rain.append(d["precipProbability"] )
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

	# creates ticks at the specified positions -- 
	xtixat = []
	xmtixat = [] # minor ticks array
	xtix = []
	for i,t in enumerate(fcsttime):
		if t == "00:00":
			xtixat.append(i)
			xtix.append(fcstday[i])
		if t == "12:00":
			xtixat.append(i)
			xtix.append(t)
		if t == "06:00" or t == "18:00":
			xmtixat.append(i)
	
	plotmat = txtplot(data=rain, 
			  ylim=[0,1], 
	                  nyticks=5, 
			  yspacer=plotsize, 
	                  xticksat=xtixat, 
			  xmticksat = xmtixat,
			  pch=pch)

	plotmat.insert(0, [" " for i in xrange(len(plotmat[0])+2)])
	for i in xrange(len(xtixat)):
		tic = list(xtix[i])
		itic = xtixat[i] + 5
		plotmat[0][itic:(itic + len(tic))] = tic





#######################################################
# print current conditions
#######################################################

elif args.mode == 'now':
	# obtain the current condition from the data file
	try:
		d = data['currently']
	except KeyError:
		print "The data for current conditions are not available for this location ("\
		    + args.location + ")."
		sys.exit(1)


	if not 'summary' in d: 
		summary = ''
	else: 
		summary = d['summary']


	if not 'temperature' in d: 
		temperature = ''
	else: 
		temperature = str(round(celsius(d['temperature']))) + ' C'


	if 'apparentTemperature' in d: 
		apptemp = round(celsius(d['apparentTemperature']), 1)
		temperature = temperature + ' (feels like ' + str(apptemp) + ' C)'


	if not 'precipType' in d: 
		d['precipType'] = 'rain'


	if not 'precipIntensity' in d: 
		d['precipIntensity'] = 0


	if d['precipIntensity'] <= 0: 
		precip = 'none'
	else: 
		precip = d['precipType'] + ' ' + str(round(d['precipIntensity'] * 25.4, 2)) + ' mm/h'

	


	# WIND
	if not 'windSpeed' in d: 
		windSpeed = '? km/h '
		bft = ''
	else: 
		windSpeed = str(int(d['windSpeed'] * 1.6093)) + ' km/h '
		bft = '('+str(int((d['windSpeed'] * 1.6093 / 3.0) ** (2.0/3.0))) + ' Bft)'


	if not 'windBearing' in d: 
		windBearing = ''
	else: 
		windBearing = ['N','NE','E','SE','S','SW', 
	                     'W', 'NW', 'N'][int(d["windBearing"] / 45.0)] + ' '
	wind = windSpeed + windBearing + bft



	if not 'humidity' in d: 
		humidity = ''
	else: 
		humidity = str(int(d['humidity'] * 100.0)) + ' %'

	
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
	print "unknown mode: "+args.mode+" "
	sys.exit(1)
	





#######################################################
# print plot matrix
#######################################################

if not args.mode == "now":
	print ""
	for i in reversed(xrange(len(plotmat))):
		print ''.join(plotmat[i])
	idx = max(0, len(plotmat[1])-22)
	print ''.join([' ' for i in xrange(idx)]) + '(src: www.forecast.io)'
	print ""



