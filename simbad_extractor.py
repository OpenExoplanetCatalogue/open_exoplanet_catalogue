'''
From Marc-Antoine Martinod
No particular license or rights, you can change it as you feel, just be honest. :)
For python puritain, sorry if this script is not "pythonic".
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

from HTMLParser import HTMLParser
import urllib
import re
import os
import glob
import time

class MyHTMLParser(HTMLParser):#HTML parser to get the information from the webpage
    def handle_starttag(self, tag, attrs): #get start tag and may store its attributes
        global boolean, dictio, data2
        if boolean == 1:# and tag == "a":
            dictio.append(data2)
            boolean = 0

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        global data2, boolean, spectre
        if re.findall("[A-Z] *\d*\.?\d*? *\[+.+\]", data):#Search magnitude
            data2 = data
            data2 = data2.replace("\n", "").replace(" ","")
            boolean = 1

#set magnitude values in XML file
def magnitude(dic, filename, path):
    #The idea is to read the file to have a big string then concatenate the magnitudes then rewrite the whole file
    if os.path.isfile(path+"/"+filename+".xml"):
        with open(path+"/"+filename+".xml","r") as readable:
            read_file = readable.read()

            tabulation = ""
            try:
                #positionning the magnitudes in the file
                if "</magV>" in read_file:
                    elt_index = read_file.index("</magV>")
                    elt_len = len("</magV>")
                    if "<binary>" in read_file:
                        tabulation = "\t"
                elif "<binary>" in read_file:
                    elt_index = read_file.index("<binary>")
                    elt_len = len("<binary>")
                else:
                    elt_index = read_file.index("<star>")
                    elt_len = len("<star>")
            except ValueError: # ie free floating planet (no star or parent)
                print '{} failed (no parent object tag'.format(filename)
                return False


        with open(path+"/"+filename+".xml", "w") as writable:#Write mag in the file
            dic2 = dic
            dic2.sort()

            magJ = ""
            magH = ""
            magK = ""
            magV = ""
            magB = ""
            magR = ""
            magI = ""

            for key in dic2:#concatenate magnitudes in the string from XML
                expr = key
                if not "[~]" in expr:
                    sigma = re.findall('\[+.+\]', expr)
                    sigma = str(sigma[0].replace('[','').replace(']',''))
                else:
                    sigma = ""

                expr = re.sub('\[+.+\]', '', expr)#Remove uncertainty from string

                expr2 = re.sub('[A-Z]', '', expr)#Remove letters from string, just mag left.
                if "J" in expr and not "magJ" in read_file:
                    if sigma != "":
                        magJ = "\n"+tabulation+"\t\t<magJ errorminus=\""+sigma+"\" errorplus=\""+sigma+"\">"+expr2+"</magJ>"
                    else:
                        magJ = "\n"+tabulation+"\t\t<magJ>"+expr2+"</magJ>"
                elif "H" in expr and not "magH" in read_file:
                    if sigma != "":
                        magH = "\n"+tabulation+"\t\t<magH errorminus=\""+sigma+"\" errorplus=\""+sigma+"\">"+expr2+"</magH>"
                    else:
                        magH = "\n"+tabulation+"\t\t<magH>"+expr2+"</magH>"
                elif "K" in expr and not "magK" in read_file:
                    if sigma != "":
                        magK = "\n"+tabulation+"\t\t<magK errorminus=\""+sigma+"\" errorplus=\""+sigma+"\">"+expr2+"</magK>"
                    else:
                        magK = "\n"+tabulation+"\t\t<magK>"+expr2+"</magK>"
                elif "V" in expr and not "magV" in read_file:
                    if sigma != "":
                        magV = "\n"+tabulation+"\t\t<magV errorminus=\""+sigma+"\" errorplus=\""+sigma+"\">"+expr2+"</magV>"
                    else:
                        magV = "\n"+tabulation+"\t\t<magV>"+expr2+"</magV>"
                elif "B" in expr and not "magB" in read_file:
                    if sigma != "":
                        magB = "\n"+tabulation+"\t\t<magB errorminus=\""+sigma+"\" errorplus=\""+sigma+"\">"+expr2+"</magB>"
                    else:
                        magB = "\n"+tabulation+"\t\t<magB>"+expr2+"</magB>"
                elif "R" in expr and not "magR" in read_file:
                    if sigma != "":
                        magR = "\n"+tabulation+"\t\t<magR errorminus=\""+sigma+"\" errorplus=\""+sigma+"\">"+expr2+"</magR>"
                    else:
                        magR = "\n"+tabulation+"\t\t<magR>"+expr2+"</magR>"
                elif "I" in expr and not "magI" in read_file:
                    if sigma != "":
                        magI = "\n"+tabulation+"\t\t<magI errorminus=\""+sigma+"\" errorplus=\""+sigma+"\">"+expr2+"</magI>"
                    else:
                        magI = "\n"+tabulation+"\t\t<magI>"+expr2+"</magI>"

            #check if mag already exists or not on simbad
            if magJ != "" or magH != "" or magK != "" or magV != "" or magB != "" or magR != "" or magI != "":
                print elt,"\t mag done."
            else:
                print elt," Mag error or already exists."

            read_file = read_file[0:elt_index+elt_len]+magB+magV+magR+magI+magJ+magH+magK+read_file[elt_index+elt_len:]
            writable.write(read_file)

    else:
        print filename," not found."

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
                                    print filename+"\tSP done."
                        else:
                            print filename, " has already a spectral type."
                    else:
                        print filename, " is a binary system."
                        log.write(filename+"\t:\tbinary system\n")

                except ValueError: # ie free floating planet (no star or parent)
                    print '{} failed (no parent object tag - probably)'.format(filename)
    else:
        print filename, "not found."

#Another script exists for that. Splitting the two functions lets me to control
#the list is in correct format and won't bring any troubles.
#However, as it is a copy/paste of the script, it should work.
def generateList(path):
    planet_list = open("list.txt", "w")
    for filename in glob.glob(path+"/*.xml"):
        # Open file
        name = os.path.split(filename)
        name = name[1]
        name = name.replace(".xml","")
        planet_list.write(name+"\n")
    planet_list.close()



#****************************MAIN*********************************
parser = MyHTMLParser()

path = "systems"  # systems or systems_kepler
generateList(path)
system_list = open("list.txt","r") #list of the systems to process
line = system_list.readlines()
line = [elt.replace('\n','') for elt in line]

log = open("log_planet.log", "a")#log 404 web error and binary systems error
log.write("\n*****"+time.strftime("%A %d %B %Y %H:%M:%S")+"*****\n")

for elt in line:#read all the list of systems and run the parser class and the magnitude function for each one
    dictio = []
    boolean = 0
    data2 = ""
    spectre = ""

    planet = elt
    try:
        code_source = urllib.urlopen('http://simbad.u-strasbg.fr/simbad/sim-basic?Ident='+planet).read()
    except IOError:
        print('Lookup failed - sleeping for 10 seconds')
        time.sleep(10)

        try:
            code_source = urllib.urlopen('http://simbad.u-strasbg.fr/simbad/sim-basic?Ident='+planet).read()
        except IOError:
            print('Lookup failed again for {} - skipping'.format(planet))
            log.write('Lookup failed for {}'.format(planet))

    #First check its existence on simbad
    if not re.findall("Identifier not found in the database", code_source):
        parser.feed(code_source)
        magnitude(dictio, planet, path)
        #if re.search('Spectral type:( *<.*?>\n){5}\w*/?\w*', code_source):
        #    extraction_spectre = re.search('Spectral type:( *<.*?>\n){5}\w*/?\w*', code_source).group(0)
        #    spectre = re.search('(?<=<TT>\n)\w*/?\w*', extraction_spectre).group(0)
        #    spectralType(spectre, planet, path)
        #else:
        #    print elt, " has no spectral type."
        #    log.write(elt+"\t:\tno spectral type\n")
        #
    else:
        print planet,"\t:\t404 page not found"
        log.write(planet+" 404 page not found\n")

log.close()
system_list.close()
