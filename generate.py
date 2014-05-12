#!/usr/bin/python
import xml.etree.ElementTree as ET, glob, os, sys, re, csv 

# Nicely indents the XML output 
def indent(elem, level=0):
    i = "\n" + level*"\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

# Loop over all files and  create new data
totalcommits = 0
totalplanets = 0
totalsystems = 0
totalbinaries = 0
totalplanets2011 = 0
totalplanets2012 = 0
totalconfirmedsystems = 0
totalconfirmedplanets = 0
totalcontributors = []
totalcontributorsemail = []

aliases = []

for filename in glob.glob("open_exoplanet_catalogue/systems/*.xml"):
	metafilename = '/'.join(filename.split("/")[1:])
	f = open(filename, 'rt')
	root = ET.parse(f).getroot()
	f.close()

	metaroot = ET.Element("system")
	systemname = root.findtext("./name").encode('utf-8')
	ET.SubElement(metaroot,"name").text = systemname 

	contributors = os.popen("cd open_exoplanet_catalogue && git shortlog '"+metafilename+"' -n -s -e").readlines()
	sys.stdout.write('.')
	sys.stdout.flush()
	#print "Working on "+metafilename+". ",
	#print "Contributors: %d " % len(contributors),

	cstag = ET.SubElement(metaroot,"contributors")
	for contributor in contributors:
		rows = contributor.split("\t")
		commits = int(rows[0])
		email = re.search('<(.*)>', rows[1]).group(1)
		name = re.search('(.*) <', rows[1]).group(1).title()
		ctag = ET.SubElement(cstag,"contributor")
		ctag.text = unicode(name,'utf-8')
		ctag.attrib['email'] = email
		ctag.attrib['commits'] = "%d"% commits
		totalcommits += commits
		if not email in totalcontributorsemail:
			totalcontributors.append(name)
			totalcontributorsemail.append(email)


	links = os.popen("cd open_exoplanet_catalogue && git --no-pager log '"+metafilename+"' | grep -oE '\\b(https?)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]*[-A-Za-z0-9+&@#/%=~_|]'").readlines()
	if len(links)>0:
		links = set(links)
		#print "Links: %d" % len(links),
		astag = ET.SubElement(metaroot,"links")
		for link in links:
			atag = ET.SubElement(astag,"link")
			atag.text = unicode(link.strip(),'utf-8')
	
	names = root.findall("./name")
	for name in names:
		aliases.append([name.text.encode('utf-8'),systemname,"system",names[0].text.encode('utf-8')])
		
	
	stars = root.findall(".//star")
	for star in stars:
		names = star.findall("./name")
		for name in names:
			aliases.append([name.text.encode('utf-8'),systemname,"star",names[0].text.encode('utf-8')])

	#print ""
	confirmedsystem = 0
	planets = root.findall(".//planet")
	for planet in planets:
		names = planet.findall("./name")
		for name in names:
			aliases.append([name.text.encode('utf-8'),systemname,"planet",names[0].text.encode('utf-8')])
		lists = planet.findall(".//list")
		totalplanets += 1
		for l in lists:
			if "Confirmed planets" in l.text:
				totalconfirmedplanets += 1
				confirmedsystem = 1
				date = planet.findtext("./discoveryyear")
				if date=="2011":
					totalplanets2011 += 1
				if date=="2012":
					totalplanets2012 += 1

	if confirmedsystem==1:
		totalconfirmedsystems += 1
	totalsystems +=1

	binaries = root.findall(".//binary")
	if binaries:
		totalbinaries += 1

	indent(metaroot)
	ET.ElementTree(metaroot).write(metafilename) 
	#if totalsystems >3: break

print ""
statroot = ET.Element("statistiscs")
ET.SubElement(statroot,"commits").text = "%d" % totalcommits
contributors = ET.SubElement(statroot,"contributors")
for c in totalcontributors:
	ET.SubElement(contributors,"contributor").text = unicode(c,'utf-8')
contributors.attrib["num"] = "%d" % len(totalcontributors)
ET.SubElement(statroot,"planets").text = "%d" % totalplanets
ET.SubElement(statroot,"systems").text = "%d" % totalsystems
ET.SubElement(statroot,"binaries").text = "%d" % totalbinaries
ET.SubElement(statroot,"planets2011").text = "%d" % totalplanets2011
ET.SubElement(statroot,"planets2012").text = "%d" % totalplanets2012
ET.SubElement(statroot,"confirmedplanets").text = "%d" % totalconfirmedplanets
ET.SubElement(statroot,"confirmedsystems").text = "%d" % totalconfirmedsystems
indent(statroot)
ET.ElementTree(statroot).write("statistics.xml") 

with open('aliases.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
	spamwriter.writerows(aliases)


