#!/usr/bin/python
import xml.etree.ElementTree as ET
import glob
import os
import sys

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


def convertunit(elem, factor):
    print "Converting unit of tag \"" + elem.tag + "\"."
    del elem.attrib['unit']
    if elem.text:
        elem.text = "%f" % (float(elem.text) * factor)
    if "error" in elem.attrib:
        elem.attrib["error"] = "%f" % (float(elem.attrib["error"]) * factor)
    if "errorplus" in elem.attrib:
        elem.attrib[
            "errorplus"] = "%f" % (
                float(
                    elem.attrib[
                        "errorplus"]) * factor)
    if "errorminus" in elem.attrib:
        elem.attrib[
            "errorminus"] = "%f" % (
                float(
                    elem.attrib[
                        "errorminus"]) * factor)
    if "upperlimit" in elem.attrib:
        elem.attrib[
            "upperlimit"] = "%f" % (
                float(
                    elem.attrib[
                        "upperlimit"]) * factor)
    if "lowerlimit" in elem.attrib:
        elem.attrib[
            "lowerlimit"] = "%f" % (
                float(
                    elem.attrib[
                        "lowerlimit"]) * factor)


# Loop over all files and  create new data
for filename in glob.glob("systems*/*.xml"):
#	try:
    f = open(filename, 'rt')
    root = ET.parse(f).getroot()
    f.close()
    # convert units to default
    for mass in root.findall(".//planet/mass[@unit='me']"):
        convertunit(mass, 0.0031457007)
    for radius in root.findall(".//planet/radius[@unit='re']"):
        convertunit(radius, 0.091130294)

    # check names
    if not root.findtext("./name") + ".xml" == os.path.basename(filename):
        print "Name of system not the same as filename: " + filename
    objectswithnames = root.findall(".//planet | .//star")
    for obj in objectswithnames:
        name = obj.findtext("./name")
        if not name:
            print "Didn't find name tag for object \"" + obj.tag + "\" in file \"" + filename + "\"."
    # check tags
    problematictag = checkforvalidtags(root)
    if problematictag:
        print "Problematic tag/attribute '" + problematictag + "' found in file \"" + filename + "\"."
    discoverymethods = root.findall(".//discoverymethod")
    for dm in discoverymethods:
        if not (dm.text in validdiscoverymethods):
            print "Problematic discoverymethod '" + dm.text + "' found in file \"" + filename + "\"."
    # cleanup
    removeemptytags(root)
    indent(root)
    ET.ElementTree(root).write(filename)
#	except:
#		print "Error parsing file "+filename+": ",sys.exc_info()[0]
