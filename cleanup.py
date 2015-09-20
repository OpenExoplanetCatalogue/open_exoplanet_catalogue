#!/usr/bin/python
import xml.etree.ElementTree as ET
import glob
import os
import hashlib
import sys
import datetime
import re

num_format = re.compile(r'^\-?[0-9]*\.?[0-9]*e?[\-\+]?[0-9]?[0-9]?$')


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
    if 'e' in elem.attrib:
        err = elem.attrib['e']
        del elem.attrib['e']
        elem.attrib['errorminus'] = err
        elem.attrib['errorplus'] = err

# Check if an unknown tag is present (most likely an indication for a typo)
validtags = [
    "system", "name", "new", "description", "ascendingnode", "discoveryyear",
    "lastupdate", "list", "discoverymethod", "semimajoraxis", "period", "magV", "magJ",
    "magH", "magR", "magB", "magK", "magI", "magU", "distance",
    "longitude", "imagedescription", "image", "age", "declination", "rightascension",
    "metallicity", "inclination", "spectraltype", "binary", "planet", "periastron", "star",
    "mass", "eccentricity", "radius", "temperature", "videolink", "transittime", 
    "spinorbitalignment", "istransiting", "separation", "positionangle", "periastrontime",
    "meananomaly"]
validattributes = [
    "error",
    "errorplus",
    "errorminus",
    "unit",
    "upperlimit",
    "lowerlimit",
    "type"]
validlists = [
    "Confirmed planets",
    "Planets in binary systems, S-type",
    "Controversial",
    "Orphan planets",
    "Planets in binary systems, P-type",
    "Kepler Objects of Interest",
    "Solar System",
    "Retracted planet candidate",
    "Planets in open clusters",
    "Planets in globular clusters"]
validdiscoverymethods = ["RV", "transit", "timing", "imaging", "microlensing"]
tagsallowmultiple = ["list", "name", "planet", "star", "binary", "separation"]
numerictags = ["mass", "radius", "ascnedingnode", "discoveryyear", "semimajoraxis", "period",
    "magV", "magJ", "magH", "magR", "magB", "magK", "magI", "magU", "distance", "longitude", "age",
    "metallicity", "inclination", "periastron", "eccentricity", "temperature", "transittime",
    "spinorbitalignment", "separation", "positionangle", "periastrontime", "meananomaly"]
numericattributes = ["error", "errorplus", "errorminus", "upperlimit", "lowerlimit"]
nonzeroattributes = ["error", "errorplus", "errorminus"]


def checkforvalidtags(elem):
    problematictag = None
    if elem.tag in numerictags:
        if elem.text:
            if not re.match(num_format,elem.text):
                return elem.tag
        deleteattribs = []
        for a in elem.attrib:
            if a in numericattributes:
                if not re.match(num_format,elem.attrib[a]):
                    return elem.tag
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

def checkforvaliderrors(elem):
    problematictag = None
    if elem.tag in numerictags:
        deleteattribs = []
        for a in elem.attrib:
            if a in nonzeroattributes:
                try:
                    if len(elem.attrib[a])==0 or float(elem.attrib[a])==0.:
                        deleteattribs.append(a)
                except:
                    print "Warning: problem reading error bars in tag "+elem.tag
                    return 1
        for a in deleteattribs:
            print "Warning: deleting error bars with value 0 in tag "+elem.tag
            del elem.attrib[a]
        if "errorplus" in elem.attrib:
            if not "errorminus" in elem.attrib:
                print "Warning: one sided error found in tag "+elem.tag+". Fixing it."
                elem.attrib["errorminus"] = elem.attrib["errorplus"]
        if "errorminus" in elem.attrib:
            if not "errorplus" in elem.attrib:
                print "Warning: one sided error found in tag "+elem.tag+". Fixing it."
                elem.attrib["errorplus"] = elem.attrib["errorminus"]
    for child in elem:
        if checkforvaliderrors(child):
            return 1
    return 0


# Convert units (makes data entry easier)
def convertunitattrib(elem, attribname, factor):
    if attribname in elem.attrib:
        elem.attrib[attribname] = "%f" % ( float(elem.attrib[attribname]) * factor)


def convertunit(elem, factor):
    print "Converting unit of tag \"" + elem.tag + "\"."
    del elem.attrib['unit']
    if elem.text:
        elem.text = "%f" % (float(elem.text) * factor)
    convertunitattrib(elem, "e", factor)
    convertunitattrib(elem, "error", factor)
    convertunitattrib(elem, "errorplus", factor)
    convertunitattrib(elem, "errorminus", factor)
    convertunitattrib(elem, "ep", factor)
    convertunitattrib(elem, "em", factor)
    convertunitattrib(elem, "upperlimit", factor)
    convertunitattrib(elem, "lowerlimit", factor)


def checkForBinaryPlanet(root, criteria, liststring):
    """ Checks if binary planets have been added to corresponding list
    """
    global fileschanged
    planets = root.findall(criteria)
    for planet in planets:
        plists = planet.findall(".//list")
        if liststring not in [plist.text for plist in plists]:
            ET.SubElement(planet, "list").text = liststring
            print "Added '" + filename + "' to list '" + liststring + "'."
            fileschanged += 1


def checkForTransitingPlanets(root):
    """ Checks for transisting planets by first seeing if there is a transittime and then checking the discovery
    method
    """
    global fileschanged
    global issues
    planets = root.findall(".//planet")
    for planet in planets:
        if not planet.findtext('.//istransiting'):
            addtag = 0
            hasTransittime = planet.findtext(".//transittime")
            discoveryMethod = planet.findtext(".//discoverymethod")
            planetRadius = planet.findtext(".//radius")
            if hasTransittime or 'transit' == discoveryMethod:
                addtag = 1
            else:
                if planetRadius:  # only measured from transits, imaging for now
                    planetName = planet.findtext(".//name")
                    excludeList = ('Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto',
                    'PSR J1719-1438 b',  # radius estimated from  Roche Lobe radius
                    '',
                    )
                    if planetName not in excludeList:
                        if not discoveryMethod == 'imaging':
                            print '{} in {} has a radius but is is missing a istransiting tag'.format(planetName, filename)
                            issues += 1

            if addtag:
                ET.SubElement(planet, "istransiting").text = '1'
                print 'Added istransiting tag to {}'.format(filename)
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
    if checkforvaliderrors(root):
        print "Problematic errorbar in in file \"" + filename + "\"."

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
    
    # Check for valid list names
    lists = root.findall(".//list")
    for l in lists:
        if l.text not in validlists:
                print "Error: Invalid list \"" + l.text + "\" in file \"" + filename + "\"."
                issues += 1

    # Check if each planet is in at least one list
    oneListOf = ["Confirmed planets", "Controversial", "Kepler Objects of Interest","Solar System", "Retracted planet candidate"]
    for p in planets:
        isInList = 0
        for l in p.findall("./list"):
            if l.text in oneListOf:
                isInList += 1
        if isInList!=1:
            print "Error: Planet needs to be in exactly one of the following lists: '" +"', '".join(oneListOf)+"'. Check planets in file \"" + filename + "\"."
            issues += 1


    # Check transiting planets
    checkForTransitingPlanets(root)

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

