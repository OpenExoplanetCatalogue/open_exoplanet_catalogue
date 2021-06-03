'''
From Marc-Antoine Martinod
No particular license or rights, you can change it as you feel, just be honest. :)
For python puritain, sorry if this script is not "pythonic".

Significant changes made by Hanno Rein, August 23, 2020
'''


'''
This script picks up the magnitudes and the spectral type from Simbad website.
*How to use it:
    ***In variable "path", put the path of the repo where you have the XMLs.
    ***Run the script

*Structure:
    ***HTMLparser class to extract information from a webpage.
    ***Two main functions : magnitude : pick up magnitudes from Simbad
                            spectralType : pick up spectral type from Simbad, it is currently commented because I don't need to run it at the moment.
    ***A list generator function : create a file containing the name of the XML files in "path".

*Logs:
    ***Log_planet.txt has all files for which there was a 404 error. This file is not reset
    when the script is rerun. It works for both functions.

*Troubleshooting:
    ***If Simbad don't recognize this name, either you search manually or you create a list with the
    other names for a system (Kepler, 2MASS...) and you rename the file with this name to let the script
    writing in it.

*Improvements:
    ***You can improve this script by a multi-name recognition :for a system, if there is a 404 error on simbad web page
    the script can try another name picked up in the XMLs and try it.
    This would avoid to make a manual reasearch or rename the files, recreate a list and rerun the script.

    ***There can be a problem with binaries system. Simbad always has only SP (spectral type) and mag for one star (don't know which)
    or the whole system but if this information exists for each star of a binary system, this script doesn't deal with it.

    ***Adapt it for other kind of extraction or for other website.
'''

from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.parse import quote_plus
import xml.etree.ElementTree as ET

import re
import os
import glob
import time

def indent(elem, level=0):
    i = "\n" + level * "\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

class MyHTMLParser(HTMLParser):#HTML parser to get the information from the webpage
    def handle_starttag(self, tag, attrs): #get start tag and may store its attributes
        global boolean, dictio_mags, data2, dictio_ident, inname
        if tag =="a" and section=="identifiers":
            inname = 1
        if boolean == 1 and section == "mag":
            dictio_mags.append(data2)
            boolean = 0
        if boolean == 1 and section == "identifiers":
            if len(data2):
                worthyCats = ["HD", "GJ", "Gaia DR2", "NAME", "HIP", "KOI", "Kepler", "KIC", "TYC"]
                for wc in worthyCats:
                    if wc in data2 and not "**" in data2:
                        data2 = data2.replace("NAME","").strip()
                        dictio_ident.append(data2)
            boolean = 0
            inname = 0
            data2 = ""

    def handle_endtag(self, tag):
        global inname
        if tag=="tt":
            inname = 0
        pass

    def handle_data(self, data):
        global data2, boolean, section, inname, dictio_distance, dictio_coord, dictio_spectral
        if section=="mag" and re.findall("[A-Z] +\d*\.?\d*? *\[+.+\]", data):#Search magnitude
            data2 = data
            data2 = data2.replace("\n", "").replace(" ","")
            boolean = 1
        if section=="identifiers" and inname==1:
            data2 = data2+data
            data2 = data2.replace("\n", "").replace("\"", "").strip()
            boolean = 1
        if re.findall("Identifiers \(\d+\) :", data):
            section = "identifiers"
            data2 = ""
        if re.findall("Spectral type:", data):
            section = "spectraltype"
        if section=="spectraltype" and re.findall("[OBAFGKM]",data):
            dictio_spectral = data.strip()
            section = "spectral done"
        if re.findall("Plots and Images", data):
            section = "plotsandimages"
        if re.findall("ICRS", data):
            section = "ICRS"
        if section=="ICRS" and re.findall("coord.",data):
            section = "ICRScoord"
        if section=="ICRScoord":
            res = re.search(r"\s+(\d\d \d\d \d\d\.\d{4})\d+ ([\+\-]\d\d \d\d \d\d\.\d{4})\d+",data)
            if res:
                dictio_coord = [res.group(1), res.group(2)]
                section = "coords done"
        if re.findall("distance Q unit", data):
            section = "distance"
            res = re.search(r"\s+\|\s*(\d+\.\d+)\s+pc\s+\|\s+\-(\d+\.\d+)\s+\+(\d+\.\d+)\s+\|",data)
            if res:
                dictio_distance = [res.group(1), res.group(2), res.group(3)]

#Another script exists for that. Splitting the two functions lets me to control
#the list is in correct format and won't bring any troubles.
#However, as it is a copy/paste of the script, it should work.
def generateList(path):
    with open("list.txt", "w") as planet_list:
        for filename in glob.glob(path+"/*.xml"):
            # Open file
            name = os.path.split(filename)
            name = name[1]
            name = name.replace(".xml","")
            planet_list.write(name+"\n")



#****************************MAIN*********************************
parser = MyHTMLParser()

path = "systems"  # systems or systems_kepler
generateList(path)
system_list = open("list.txt","r") #list of the systems to process
lines = system_list.readlines()
lines = [line.replace('\n','') for line in lines]

try:
    willskip = open("simbad_skip.txt","r").readlines() #list of the systems to process
    willskip = [s.strip() for s in willskip]
except:
    willskip = []

nummax = 10000

for line in lines:#read all the list of systems and run the parser class and the magnitude function for each one
    filename = path+"/"+line+".xml"
    f = open(filename, 'rt')
    root = ET.parse(f).getroot()
    stars = root.findall(".//star")
    binaries = root.findall(".//binary")
    systemname = root.findtext("./name")
    if line in willskip:
        continue
    if len(binaries):
        continue
    #if root.findall(".//spectraltype"):
    #    continue

    ## One request per star
    for stari, star in enumerate(stars):
        starnames = star.findall("./name")
        # do request
        dictio_mags = []
        dictio_ident = []
        dictio_distance = []
        dictio_coord = []
        dictio_spectral = []
        section = "mag"
        boolean = 0
        data2 = ""

        starname = starnames[0].text
        try:
            print('Requesting: http://simbad.cfa.harvard.edu/simbad/sim-basic?Ident='+quote_plus(starname))
            code_source = urlopen('http://simbad.cfa.harvard.edu/simbad/sim-basic?Ident='+quote_plus(starname)).read()
            #print('Requesting: http://simbad.u-strasbg.fr/simbad/sim-basic?Ident='+quote_plus(starname))
            #code_source = urlopen('http://simbad.u-strasbg.fr/simbad/sim-basic?Ident='+quote_plus(starname)).read()
            code_source = code_source.decode('utf-8')
        except IOError:
            print('Lookup failed for {} - skipping'.format(starname))
            continue
        if re.findall("Identifier not found in the database", code_source):
            print('Identifier not found in the database. - skipping')
            continue
        if re.findall("Extra-solar Confirmed Planet", code_source):
            print('Got planet, not star. - skipping')
            continue


        parser.feed(code_source)
        dictio_mags.sort()

        # Work on new star names 
        lastnameindex = -1
        for ind, child in enumerate(star):
            if child.text == starnames[-1].text:
                lastnameindex = ind
        starnames = [n.text for n in starnames]
        for newstarname in dictio_ident:
            if newstarname not in starnames:
                nsn = ET.Element("name")
                nsn.text = newstarname
                star.insert(lastnameindex+1,nsn)
                print("New star name added: ", newstarname)
        for key in dictio_mags:#concatenate magnitudes in the string from XML
            expr = key
            if not "[~]" in expr:
                sigma = re.findall('\[+.+\]', expr)
                sigma = str(sigma[0].replace('[','').replace(']',''))
            else:
                sigma = ""

            expr = re.sub('\[+.+\]', '', expr)#Remove uncertainty from string

            expr2 = re.sub('[A-Z]', '', expr)#Remove letters from string, just mag left.
            magletters = ["J", "H","K","V","B","R","I"]
           
            #find location to insert (after current mags, after names)
            maginsertindex = -1
            for magletter in magletters:
                mags = star.findall("./mag"+magletter)
                for mag in mags:
                    for ind, child in enumerate(star):
                        if child.text == mag.text:
                            maginsertindex = max(maginsertindex,ind)
            names = star.findall("./name")
            for name in names:
                for ind, child in enumerate(star):
                    if child.text == name.text:
                        maginsertindex = max(maginsertindex,ind)

            for magletter in magletters:
                if magletter in expr:
                    if not star.findtext("./mag"+magletter):
                        nmag = ET.Element("mag"+magletter)
                        nmag.text = expr2
                        if sigma:
                            nmag.attrib['errorminus'] = sigma
                            nmag.attrib['errorplus'] = sigma
                        star.insert(maginsertindex+1,nmag)
                        print("New mag",magletter,"added: ",expr2,sigma) 
            if len(dictio_spectral):
                if not star.findtext("./spectraltype"):
                    spectraltype = ET.Element("spectraltype")
                    spectraltype.text = dictio_spectral
                    star.insert(maginsertindex+1,spectraltype)
                    print("New spectraltype added: ",dictio_spectral) 

        ## Planet Names
        planets = star.findall("./planet")
        for planet in planets:
            planetname = planet.findtext("./name")
            planetsuffix = planetname.replace(starname,"")
            if planetsuffix in [" b"," c"," d"," e"," f"," g"," h"," i"," j"]:
                # will attempt to add other names
                planetnames = planet.findall("./name")
                lastnameindex = -1
                for ind, child in enumerate(planet):
                    if child.text == planetnames[-1].text:
                        lastnameindex = ind
                planetnames = [n.text for n in planetnames]
                for starname in dictio_ident:
                    newplanetname = starname + planetsuffix
                    if newplanetname not in planetnames:
                        nne = ET.Element("name")
                        nne.text = newplanetname
                        planet.insert(lastnameindex+1,nne)
                        print("New planet name added: ", newplanetname)


    ## System parameters based on last star in system
    systemnames = root.findall("./name")
    lastnameindex = -1
    for ind, child in enumerate(root):
        if child.text == systemnames[-1].text:
            lastnameindex = ind
    if not root.findtext("./distance") and len(dictio_distance):
        distance = ET.Element("distance")
        distance.text = dictio_distance[0]
        distance.attrib['errorminus'] = dictio_distance[1]
        distance.attrib['errorplus'] = dictio_distance[2]
        print("New distance added: ", dictio_distance)
        root.insert(lastnameindex+1,distance)
    if len(dictio_coord):
        coord = root.findtext("./declination")
        if coord:
            if coord[:6] in dictio_coord[1] and len(coord)<len(dictio_coord[1]):
                for ind, child in enumerate(root):
                    if child.tag == "declination":
                        lastnameindex = ind-1
                        print("Old declination removed: ", coord)
                        root.remove(child)
                        coord = None
                        break
        if not coord:
            declination = ET.Element("declination")
            declination.text = dictio_coord[1]
            print("New declination added: ", dictio_coord[1])
            root.insert(lastnameindex+1,declination)
        coord = root.findtext("./rightascension")
        if coord:
            if coord[:5] in dictio_coord[0] and len(coord)<len(dictio_coord[0]):
                for ind, child in enumerate(root):
                    if child.tag == "rightascension":
                        lastnameindex = ind-1
                        print("Old rightascension removed: ", coord)
                        root.remove(child)
                        coord = None
                        break
        if not coord:
            rightascension = ET.Element("rightascension")
            rightascension.text = dictio_coord[0]
            print("New rightascension added: ", dictio_coord[0])
            root.insert(lastnameindex+1,rightascension)





    indent(root)
    
    with open(filename, 'wb') as outfile:
        ET.ElementTree(root).write(outfile, encoding="UTF-8", xml_declaration=False)

    with open("simbad_skip.txt", "a+") as skip_list:
        skip_list.write(line+"\n")
    print("")
    
    time.sleep(1)
    nummax-=1
    if nummax==0:
        break
