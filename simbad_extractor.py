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
        global boolean, dictio, data2, dictio_ident, inname
        if tag =="a" and section=="identifiers":
            inname = 1
        if boolean == 1 and section == "mag":
            dictio.append(data2)
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
        global data2, boolean, spectre, section, inname
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
        if re.findall("Plots and Images", data):
            section = "plotsandimages"

def updateXML(filename):
    global dictio, dictio_ident
    dic2 = dictio
    dic2.sort()

    f = open(filename, 'rt')
    root = ET.parse(f).getroot()
    planets = root.findall(".//planet")
    stars = root.findall(".//star")
    binaries = root.findall(".//binary")
    systemname = root.findtext("./name")
    if len(binaries):
        print("binary system. skipping")
        return False

    ## Planet Names
    for planet in planets:
        planetname = planet.findtext("./name")
        planetsuffix = planetname.replace(systemname,"")
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

    ## Star Names and magnitudes
    for star in stars: # should be only one star
        starnames = star.findall("./name")
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
        for key in dic2:#concatenate magnitudes in the string from XML
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

    indent(root)
    # Write XML to file.
    with open(filename, 'wb') as outfile:
        ET.ElementTree(root).write(outfile, encoding="UTF-8", xml_declaration=False)

#set spectral type in the XML file.
def spectralType(spectre, filename, path):
    #Check if the file exists
    if os.path.isfile(path+"/"+filename+".xml"):
            with open(path+"/"+filename+".xml","r") as readable:
                read_file = readable.read()
                tabulation = ""
                back_line = ""

                #Positionning of the information in the file.
                try:
                    if not "<binary>" in read_file:
                        if not "<spectraltype>" in read_file:
                            elt_index = read_file.index("<star>")
                            elt_len = len("<star>")
                            back_line = "\n"

                            #Writing the SP (spectral type) in the file
                            with open(path+"/"+filename+".xml","w") as writable:
                                    spectre = back_line+"\t\t"+tabulation+"<spectraltype>"+spectre+"</spectraltype>"
                                    read_file = read_file[0:elt_index+elt_len]+spectre+read_file[elt_index+elt_len:]
                                    writable.write(read_file)
                                    print(filename+"\tSP done.")
                        else:
                            print(filename, " has already a spectral type.")
                    else:
                        print(filename, " is a binary system.")

                except ValueError: # ie free floating planet (no star or parent)
                    print('{} failed (no parent object tag - probably)'.format(filename))
    else:
        print(filename, "not found.")

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
line = system_list.readlines()
line = [elt.replace('\n','') for elt in line]

try:
    willskip = open("simbad_skip.txt","r").readlines() #list of the systems to process
    willskip = [s.strip() for s in willskip]
except:
    willskip = []

for elt in line:#read all the list of systems and run the parser class and the magnitude function for each one
    if elt in willskip:
        print("skipping ",elt)
        continue
    dictio = []
    dictio_ident = []
    section = "mag"
    boolean = 0
    data2 = ""
    spectre = ""

    planet = elt
    try:
        code_source = urlopen('http://simbad.u-strasbg.fr/simbad/sim-basic?Ident='+quote_plus(planet)).read()
        print('http://simbad.u-strasbg.fr/simbad/sim-basic?Ident='+quote_plus(planet))
    except IOError:
        print('Lookup failed - sleeping for 10 seconds')
        time.sleep(10)

        try:
            code_source = urlopen('http://simbad.u-strasbg.fr/simbad/sim-basic?Ident='+quote_plus(planet)).read()
        except IOError:
            print('Lookup failed again for {} - skipping'.format(planet))
    code_source = code_source.decode('utf-8')

    #First check its existence on simbad
    if not re.findall("Identifier not found in the database", code_source):
        parser.feed(code_source)
        updateXML(path+"/"+planet+".xml")
        #if re.search('Spectral type:( *<.*?>\n){5}\w*/?\w*', code_source):
        #    extraction_spectre = re.search('Spectral type:( *<.*?>\n){5}\w*/?\w*', code_source).group(0)
        #    spectre = re.search('(?<=<TT>\n)\w*/?\w*', extraction_spectre).group(0)
        #    spectralType(spectre, planet, path)
        #else:
        #    print elt, " has no spectral type."
        #
    else:
        print(planet,"\t:\t404 page not found")

    with open("simbad_skip.txt", "a+") as skip_list:
        skip_list.write(elt+"\n")
    print("")
