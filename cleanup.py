#!/usr/bin/python
import xml.etree.ElementTree as ET
import glob
import os
import hashlib
import sys
import datetime

# Variables to keep track of progress
fileschecked = 0
issues = 0
xmlerrors = 0
fileschanged = 0


# Calculate md5 hash to check for changes in file.
def md5_for_file(f, block_size=2 ** 20):
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.digest()


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
    "lowerlimit",
    "type"]
validdiscoverymethods = ["RV", "transit", "timing", "imaging", "microlensing"]
tagsallowmultiple = ["list", "name", "planet", "star", "binary"]


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
def convertunitattrib(elem, attribname, factor):
    if attribname in elem.attrib:
        elem.attrib[attribname] = "%f" % ( float(elem.attrib[attribname]) * factor)


def convertunit(elem, factor):
    print "Converting unit of tag \"" + elem.tag + "\"."
    del elem.attrib['unit']
    if elem.text:
        elem.text = "%f" % (float(elem.text) * factor)
    convertunitattrib(elem, "error", factor)
    convertunitattrib(elem, "errorplus", factor)
    convertunitattrib(elem, "errorminus", factor)
    convertunitattrib(elem, "ep", factor)
    convertunitattrib(elem, "em", factor)
    convertunitattrib(elem, "upperlimit", factor)
    convertunitattrib(elem, "lowerlimit", factor)


# Check if binary planets have been added to corresponding list
def checkForBinaryPlanet(root, criteria, liststring):
    global fileschanged
    planets = root.findall(criteria)
    for planet in planets:
        plists = planet.findall(".//list")
        inthere = 0
        for plist in plists:
            if plist.text == liststring:
                inthere = 1
        if inthere == 0:
            ET.SubElement(planet, "list").text = liststring
            print "Added '" + filename + "' to list '" + liststring + "'."
            fileschanged += 1


# Loop over all files and  create new data
for filename in glob.glob("systems*/*.xml"):
    fileschecked += 1

    # Save md5 for later
    f = open(filename, 'rt')
    md5_orig = md5_for_file(f)

    # Open file
    f = open(filename, 'rt')

    # Try to parse file
    try:
        root = ET.parse(f).getroot()
        planets = root.findall(".//planet")
        stars = root.findall(".//star")
        binaries = root.findall(".//binary")
    except ET.ParseError as error:
        print '{}, {}'.format(filename, error)
        xmlerrors += 1
        issues += 1
        continue
    finally:
        f.close()

    # Find tags with range=1 and convert to default error format
    for elem in root.findall(".//*[@range='1']"):
        fragments = elem.text.split()
        elem.text = fragments[0]
        elem.attrib["errorminus"] = "%f" % (float(fragments[0]) - float(fragments[1]))
        elem.attrib["errorplus"] = "%f" % (float(fragments[2]) - float(fragments[0]))
        del elem.attrib["range"]
        print "Converted range to errorbars in tag '" + elem.tag + "'."

        # Convert units to default units
    for mass in root.findall(".//planet/mass[@unit='me']"):
        convertunit(mass, 0.0031457007)
    for radius in root.findall(".//planet/radius[@unit='re']"):
        convertunit(radius, 0.091130294)
    for angle in root.findall(".//*[@unit='rad']"):
        convertunit(angle, 57.2957795130823)

    # Check lastupdate tag for correctness
    for lastupdate in root.findall(".//planet/lastupdate"):
        la = lastupdate.text.split("/")
        if len(la) != 3 or len(lastupdate.text) != 8:
            print "Date format not following 'yy/mm/dd' convention: " + filename
            issues += 1
        if int(la[0]) + 2000 - datetime.date.today().year > 0 or int(la[1]) > 12 or int(la[2]) > 31:
            print "Date not valid: " + filename
            issues += 1

    # Check that names follow conventions
    if not root.findtext("./name") + ".xml" == os.path.basename(filename):
        print "Name of system not the same as filename: " + filename
        issues += 1
    for obj in planets + stars:
        name = obj.findtext("./name")
        if not name:
            print "Didn't find name tag for object \"" + obj.tag + "\" in file \"" + filename + "\"."
            issues += 1

    # Check if tags are valid and have valid attributes
    problematictag = checkforvalidtags(root)
    if problematictag:
        print "Problematic tag/attribute '" + problematictag + "' found in file \"" + filename + "\"."
        issues += 1
    discoverymethods = root.findall(".//discoverymethod")
    for dm in discoverymethods:
        if not (dm.text in validdiscoverymethods):
            print "Problematic discoverymethod '" + dm.text + "' found in file \"" + filename + "\"."
            issues += 1

    # Check if there are duplicate tags
    for obj in planets + stars + binaries:
        uniquetags = []
        for child in obj:
            if not child.tag in tagsallowmultiple:
                if child.tag in uniquetags:
                    print "Error: Found duplicate tag \"" + child.tag + "\" in file \"" + filename + "\"."
                    issues += 1
                else:
                    uniquetags.append(child.tag)

    # Check binary planet lists
    checkForBinaryPlanet(root, ".//binary/planet", "Planets in binary systems, P-type")
    checkForBinaryPlanet(root, ".//binary/star/planet", "Planets in binary systems, S-type")

    # Cleanup XML
    removeemptytags(root)
    indent(root)

    # Write XML to file.
    ET.ElementTree(root).write(filename, encoding="UTF-8", xml_declaration=False)

    # Check for new md5
    f = open(filename, 'rt')
    md5_new = md5_for_file(f)
    if md5_orig != md5_new:
        fileschanged += 1

errorcode = 0
print "Cleanup script finished. %d files checked." % fileschecked
if fileschanged > 0:
    print "%d file(s) modified." % fileschanged
    errorcode = 1

if xmlerrors > 0:
    print "%d XML errors found." % xmlerrors
    errorcode = 2

if issues > 0:
    print "Number of issues: %d (see above)." % issues
    errorcode = 3
else:
    print "No issues found."

sys.exit(errorcode)

