#!/usr/bin/python
import xml.etree.ElementTree as ET
import glob
import os

# Nicely indents the XML output
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

# Removes empty nodes from the tree
def removeemptytags(elem):
    if elem.text:
        elem.text = elem.text.strip()
    toberemoved = []
    for child in elem:
        if len(child) == 0 and child.text is None and len(child.attrib) == 0:
            toberemoved.append(child)
    for child in toberemoved:
        elem.remove(child)
    for child in elem:
        removeemptytags(child)
    # Convert error to errorminus and errorplus
    if 'ep' in elem.attrib:
        err = elem.attrib['ep']
        del elem.attrib['ep']
        elem.attrib['errorplus'] = err
    if 'em' in elem.attrib:
        err = elem.attrib['em']
        del elem.attrib['em']
        elem.attrib['errorminus'] = err
    if 'error' in elem.attrib:
        err = elem.attrib['error']
        del elem.attrib['error']
        elem.attrib['errorminus'] = err
        elem.attrib['errorplus'] = err

# Check if an unknown tag is present (most likely an indication for a typo)
validtags = [
    "system", "name", "new", "description", "ascendingnode", "discoveryyear",
    "lastupdate", "list", "discoverymethod", "semimajoraxis", "period", "magV", "magJ",
    "magH", "magR", "magB", "magK", "magI", "distance",
    "longitude", "imagedescription", "image", "age", "declination", "rightascension",
    "metallicity", "inclination", "spectraltype", "binary", "planet", "periastron", "star",
    "mass", "eccentricity", "radius", "temperature", "videolink", "transittime", "rossitermclaughlin"]
validattributes = [
    "error",
    "errorplus",
    "errorminus",
    "unit",
    "upperlimit",
    "lowerlimit"]
validdiscoverymethods = ["RV", "transit", "timing", "imaging", "microlensing"]
tagsallowmultiple = ["list","name","planet","star","binary"]

def checkforvalidtags(elem):
    problematictag = None
    for child in elem:
        _tmp = checkforvalidtags(child)
        if _tmp:
            problematictag = _tmp
    if elem.tag not in validtags:
        problematictag = elem.tag
    for a in elem.attrib:
        if a not in validattributes:
            return a
    return problematictag

# Convert units (makes data entry easier)
def convertunitattrib(elem,attribname,factor):
    if attribname in elem.attrib:
        elem.attrib[attribname] = "%f" % ( float(elem.attrib[attribname]) * factor)

def convertunit(elem, factor):
    print "Converting unit of tag \"" + elem.tag + "\"."
    del elem.attrib['unit']
    if elem.text:
        elem.text = "%f" % (float(elem.text) * factor)
    convertunitattrib(elem,"error",factor)
    convertunitattrib(elem,"errorplus",factor)
    convertunitattrib(elem,"errorminus",factor)
    convertunitattrib(elem,"upperlimit",factor)
    convertunitattrib(elem,"lowerlimit",factor)

# Loop over all files and  create new data
for filename in glob.glob("systems*/*.xml"):
    # Open file
    f = open(filename, 'rt')

    # Try to parse file
    try:
        root 		= ET.parse(f).getroot()
    	planets 	= root.findall(".//planet")
    	stars 		= root.findall(".//star")
    	binaries 	= root.findall(".//binary")
    except ET.ParseError as error:
        print '{}, {}'.format(filename, error)
    f.close()

    # Convert units to default units
    for mass in root.findall(".//planet/mass[@unit='me']"):
        convertunit(mass, 0.0031457007)
    for radius in root.findall(".//planet/radius[@unit='re']"):
        convertunit(radius, 0.091130294)

    # Check that names follow conventions
    if not root.findtext("./name") + ".xml" == os.path.basename(filename):
        print "Name of system not the same as filename: " + filename
    for obj in planets + stars:
        name = obj.findtext("./name")
        if not name:
            print "Didn't find name tag for object \"" + obj.tag + "\" in file \"" + filename + "\"."

    # Check if tags are valid and have valid attributes
    problematictag = checkforvalidtags(root)
    if problematictag:
        print "Problematic tag/attribute '" + problematictag + "' found in file \"" + filename + "\"."
    discoverymethods = root.findall(".//discoverymethod")
    for dm in discoverymethods:
        if not (dm.text in validdiscoverymethods):
            print "Problematic discoverymethod '" + dm.text + "' found in file \"" + filename + "\"."

    # Check if there are duplicate tags
    for obj in planets + stars + binaries:
        uniquetags = []
        for child in obj:
            if not child.tag in tagsallowmultiple:
                if child.tag in uniquetags:
                    print "Error: Found duplicate tag \""+child.tag+"\" in file \""+filename+"\"."
                else:
                    uniquetags.append(child.tag)
	


    # Cleanup XML
    removeemptytags(root)
    indent(root)

    # Write XML to file.
    ET.ElementTree(root).write(filename)
