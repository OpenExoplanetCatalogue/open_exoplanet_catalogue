#!/usr/bin/python
# This script generates the systems_kepler data files.
# The input data comes from a csv files from the NASA Exoplanet Archive http://exoplanetarchive.ipac.caltech.edu.
import math,os
import xml.etree.ElementTree as ET, glob

# Delete old data files.
os.system("rm systems_kepler/*.xml")

# Read in csv file. This file is presorted according to the KOI Name (the default file they offer as a download is not). 
# This makes matching systems with multiple planets much easier, but it should be incorporated in this script.
os.system("sort -k3 -t',' cumulative.csv >cumulative.sorted")
csvfile = open("cumulative.sorted","r")

lastsystemname = ""
numcandidates = 0

# Each row corresponds to a planer
for row in csvfile:
	if row[0]=="#" or row[0]=="r": # ignore comments
		continue
	c = row.split(",")
	kepid = c[1]	# Kepler ID (KIC)
	koi = c[2]	# KOI Number
	koi1 = koi.split(".")[0][2:]	# First part of KOI (star)
	koi2 = koi.split(".")[1]	# Second part of KOI (planet)
	systemname = "KOI-"+koi1
	disposition = c[3]		# Status flag. 
	if disposition == "FALSE POSITIVE" or disposition=="NOT DISPOSITIONED":
		continue		# Do not include false positives and planets that have not yet been dispositioned.
	description = ""
	if disposition == "CANDIDATE":	# Add a default description
		description = "This is a Kepler Object of Interest from the Q1-Q12 dataset. It has been flagged as a possible transit event but has not been confirmed to be a planet yet."
	if disposition == "CONFIRMED":
		description = "This is a Kepler Object of Interest from the Q1-Q12 dataset. It has been flagged as a confirmed planet by the Kepler team and might have already appear in a peer reviewed paper."

	# Read in paramaters (not pretty, but works)
	period = c[5]
	perioderrorplus = c[6]
	perioderrorminus = c[7]
	transittime = float(c[8])+2454833.0	# Convert to JD
	transittimeerrorplus = c[9]
	transittimeerrorminus = c[10]
	inclination = c[23]
	inclinationerrorplus = c[24]
	inclinationerrorminus = c[25]
	semia = c[26]
	semiaerrorplus = c[27]
	semiaerrorminus = c[28]
	e = c[29]
	errrorplus = c[30]
	eerrorminus = c[31]
	radius = c[41] 			# earthradii
	radiuserrorplus = c[42] 	# earthradii
	radiuserrorminus = c[43] 	# earthradii
	tempplan = c[44]
	tempplanerrorplus = c[45]
	tempplanerrorminus = c[46]
	tempstar = c[47]
	tempstarerrorplus = c[48]
	tempstarerrorminus = c[49]
	radiusstar = c[53]
	radiusstarerrorplus = c[54]
	radiusstarerrorminus = c[55]
	metallicitystar = c[56]
	metallicitystarerrorplus = c[57]
	metallicitystarerrorminus = c[58]
	massstar = c[59]
	massstarerrorplus = c[60]
	massstarerrorminus = c[61]
	age = c[62]
	ageerrorplus = c[63]
	ageerrorminus = c[64]
	ra = float(c[68])/360.*24. 	# degree
	dec = float(c[69]) 		# degreee
	rastring = "%02d %02d %02d" %(math.floor(ra), math.floor((ra-math.floor(ra))*60.) ,(ra-math.floor(ra)-math.floor((ra-math.floor(ra))*60.)/60.)*60.*60.)
	decstring = "+%02d %02d %02d" %(math.floor(dec), math.floor((dec-math.floor(dec))*60.) ,(dec-math.floor(dec)-math.floor((dec-math.floor(dec))*60.)/60.)*60.*60.)
	keplermag = float(c[70])

	# Calculate a distance estimate based on the luminosity and the stellar temperature.
	if tempstar:
		luminosity = float(radiusstar)*float(radiusstar)*float(tempstar)*float(tempstar)*float(tempstar)*float(tempstar)/5778./5778./5778./5778.

		M = -2.5*math.log10(luminosity)+4.74

		mu = keplermag - M
		distance = math.pow(10.,mu/5.+1.)


	# If this is the first planet in the system, setup the system and star tags.
	if systemname != lastsystemname:
		root = ET.Element("system")

		ET.SubElement(root,"name").text = systemname
		ET.SubElement(root,"rightascension").text = rastring
		ET.SubElement(root,"declination").text = decstring
		if tempstar:
			ET.SubElement(root,"distance").text =  "%.2f" %distance

		star = ET.SubElement(root,"star")
		ET.SubElement(star,"name").text = systemname

		if tempstar:
			element = ET.SubElement(star,"temperature")
			element.text = tempstar
			element.attrib["errorplus"] = tempstarerrorplus
			element.attrib["errorminus"] = tempstarerrorminus[1:]

		if radiusstar:
			element = ET.SubElement(star,"radius")
			element.text = radiusstar
			element.attrib["errorplus"] = radiusstarerrorplus
			element.attrib["errorminus"] = radiusstarerrorminus[1:]

		if massstar:
			element = ET.SubElement(star,"mass")
			element.text = massstar
			element.attrib["errorplus"] = massstarerrorplus
			element.attrib["errorminus"] = massstarerrorminus[1:]

		if age:
			element = ET.SubElement(star,"age")
			element.text =  age
			element.attrib["errorplus"] = ageerrorplus
			element.attrib["errorminus"] = ageerrorminus[1:]
		
		if metallicitystar:
			element = ET.SubElement(star,"metallicity")
			element.text =  metallicitystar
			element.attrib["errorplus"] = metallicitystarerrorplus
			element.attrib["errorminus"] = metallicitystarerrorminus[1:]

	# Setup planet tags
	planet = ET.SubElement(star,"planet")
	planetname = systemname+" "+chr(int(koi2)+97) 		# Converts "KOI-10.01" to "KOI-10 b", etc.
	ET.SubElement(planet,"name").text = planetname
	ET.SubElement(planet,"name").text = systemname+" "+koi2
	
	if radius:
		element = ET.SubElement(planet,"radius")
		element.text = "%.5f" % (float(radius)*0.09113029)	# Convert to Jupiter radii
		if radiuserrorplus and radiuserrorminus:
			element.attrib["errorplus"] = "%.5f" % (float(radiuserrorplus)*0.09113029)
			element.attrib["errorminus"] = "%.5f" % (float(radiuserrorminus[1:])*0.09113029)

	if period:
		element = ET.SubElement(planet,"period")
		element.text = period
		element.attrib["errorplus"] = perioderrorplus
		element.attrib["errorminus"] = perioderrorminus[1:]
	
	if transittime:
		element = ET.SubElement(planet,"transittime")
		element.text = "%.7f" % transittime
		if transittimeerrorplus and transittimeerrorminus:
			element.attrib["errorplus"] = "%.7f" % float(transittimeerrorplus)
			element.attrib["errorminus"] = "%.7f" % float (transittimeerrorminus[1:])

	if semia:
		element = ET.SubElement(planet,"semimajoraxis")
		element.text = semia
		if semiaerrorplus and semiaerrorminus:
			element.attrib["errorplus"] = semiaerrorplus
			element.attrib["errorminus"] = semiaerrorminus[1:]
	
	if e and float(e)!=0.:
		element = ET.SubElement(planet,"eccentricity")
		element.text = e
		if eerrorplus and eerrorminus:
			element.attrib["errorplus"] = eerrorplus
			element.attrib["errorminus"] = eerrorminus[1:]
	
	if tempplan:
		element = ET.SubElement(planet,"temperature")
		element.text = tempplan
		if tempplanerrorplus and tempplanerrorminus:
			element.attrib["errorplus"] = tempplanerrorplus
			element.attrib["errorminus"] = tempplanerrorminus[1:]
	
	ET.SubElement(planet,"list").text = "Kepler Objects of Interest"
	ET.SubElement(planet,"description").text = description
	
	tree = ET.ElementTree(root)
	tree.write("./systems_kepler/"+systemname+".xml")
	lastsystemname = systemname
	numcandidates += 1

print "Number of candidates: %d"%numcandidates
