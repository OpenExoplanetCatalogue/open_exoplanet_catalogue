#!/usr/bin/python
import xml.etree.ElementTree as ET


class System:
    
    def __init__(self, name=None, rightascension=None, declination=None,\
            distance=None, epoch=None,*args):
        """bleg"""

        self.name = []
        if(name.__class__.__name__ == "str"):
            self.name.append(name)
        elif(name is None):
            pass
        else:
            self.name = list(name)
        self.rightascension = rightascension
        self.declination = declination
        self.distance = distance
        self.children = list(args)
        self.epoch = epoch

    def __str__(self):
        tempstr = ""
        for tag in reversed(dir(self)):
            if(tag[:2] != "__"):
                if(getattr(self, tag).__class__.__name__ == "list"):
                    for item in getattr(self, tag):
                        tempstr += tag + ":" + item.__str__() + "\n"
                else:
                    tempstr += tag + ":"+ getattr(self, tag).__str__() + "\n" 
        return tempstr

class Binary:

    def __init__(self, name=None, semimajoraxis=None, eccentricity=None,\
            periastron=None, longitude=None, ascendingnode=None,\
            inclination=None, period=None, transittime=None, magB=None,\
            magV=None, magI=None, magJ=None, magH=None, magK=None, *args):
        """bleg"""

        self.name = []
        if(name.__class__.__name__ == "str"):
            self.name.append(name)
        elif(name is None):
            pass
        else:
            self.name = list(name)
        self.semimajoraxis = semimajoraxis
        self.eccentricity = eccentricity
        self.periastron = periastron
        self.longitude = longitude
        self.ascendingnode = ascendingnode
        self.inclination = inclination
        self.period = period
        self.transittime = transittime
        self.magV = magV
        self.magB = magB
        self.magI = magI
        self.magJ = magJ
        self.magH = magH
        self.magK = magk
        self.children = list(args)

    def __str__(self):
        tempstr = ""
        for tag in dir(self):
            if(tag[:2] != "__"):
                if(getattr(self, tag).__class__.__name__ == "list"):
                    for item in getattr(self, tag):
                        tempstr += "     " + tag + ":" + item.__str__() + "\n"
                else:
                    tempstr += +"   " + tag + ":"+ getattr(self, tag).__str__() + "\n" 
        return tempstr
    
class Star:

    def __init__(self, name=None, mass=None, radius=None, temperature=None, age=None, metallicity=None, \
            spectraltype=None, magB=None, magV=None, magI=None, magJ=None, magH=None, magK=None, *args):
        """bleg"""

        self.name = []
        if(name.__class__.__name__ == "str"):
            self.name.append(name)
        elif(name is None):
            pass
        else:
            self.name = list(name)
        self.mass = mass
        self.radius = radius
        self.temperature = temperature
        self.age = age
        self.metallicity = metallicity
        self.spectraltype = spectraltype
        self.magV = magV
        self.magB = magB
        self.magI = magI
        self.magJ = magJ
        self.magH = magH
        self.magK = magK
        self.children = list(args)

    def __str__(self):
        tempstr = ""
        for tag in dir(self):
            if(tag[:2] != "__"):
                if(getattr(self, tag).__class__.__name__ == "list"):
                    for item in getattr(self, tag):
                        tempstr += "        " + tag + ":" + item.__str__() + "\n"
                else:
                    tempstr += "        "+tag + ":"+ getattr(self, tag).__str__() + "\n" 
        return tempstr

class Planet:

    def __init__(self, name=None, semimajoraxis=None, eccentricity=None, periastron=None,\
            longitude=None, ascendingnode=None, inclination=None, period=None, transittime=None,\
            mass=None, radius=None, temperature=None, age=None, discoverymethod=None, istransiting=None,\
            description=None, discoveryyear=None, lastupdate=None, spinorbitalignment=None):
        """bleg"""
        
        self.name = []
        if(name.__class__.__name__ == "str"):
            self.name.append(name)
        elif(name is None):
            pass
        else:
            self.name = list(name)
        self.semimajoraxis = semimajoraxis
        self.eccentricity = eccentricity
        self.periastron = periastron
        self.longitude = longitude
        self.ascendingnode = ascendingnode
        self.inclination = inclination
        self.period = period
        self.transittime = transittime
        self.mass = mass
        self.radius = radius
        self.temperature = temperature
        self.age = age
        self.discoverymethod = discoverymethod
        self.istransiting = istransiting
        self.description = description
        self.discoveryyear = discoveryyear
        self.lastupdate = lastupdate
        self.spinorbitalignment = spinorbitalignment

    def __str__(self):
        tempstr = ""
        for tag in dir(self):
            if(tag[:2] != "__"):
                if(getattr(self, tag).__class__.__name__ == "list"):
                    for item in getattr(self, tag):
                        tempstr += "            " + tag + ":" + item.__str__() + "\n"
                else:
                    tempstr += "            " +tag + ":"+ getattr(self, tag).__str__() + "\n" 
        return tempstr

class number:

    def __init__(self, value, errorminus=None, errorplus=None, \
            lowerlimit=None, upperlimit=None):
        """"(float, float, float) -> (number)
        number object acts as a typical float object, but can hold\
        errorminus, errorplus, lowerlimit, upperlimit
        mathematical operations use value. number == number does compare
        the error values as well
        """
        try:
            self.value = float(value)
        except:
            self.value = value
        try:
            self.errorminus = float(errorminus)
        except:
            self.errorminus = errorminus
        try:
            self.errorplus = float(errorplus)
        except:
            self.errorplus = errorplus 
        try:
            self.upperlimit = float(upperlimit)
        except:
            self.upperlimit = upperlimit
        try:
            self.lowerlimit = float(lowerlimit)
        except:
            self.lowerlimit = lowerlimit
    def __str__(self):
        """(NoType) -> str
        Returns a string representation of the number

        example for a number with value=2.0, errorminus = 0.5, errorplus = 0.2
            2.0 (+0.5 -0.2)
        """
        tempstr = str(self.value)
        if(self.errorplus is not None or self.errorminus is not None):
            tempstr += "(+" + str(self.errorplus) + " -" + str(self.errorminus) + ")"
        if(self.upperlimit is not None or self.lowerlimit is not None):
            tempstr += "(lowerlimit="+ str(self.lowerlimit)+" upperlimit="+ str(self.upperlimit) +")"
        return tempstr 
    def __eq__(self, num):
        """(any)-> any
        returns true if value of self is the same as value of num
        x == y
        if num is of type number, this will check the errors as well
        """
        if(num.__class__.__name__ == "number"):
            return (self.value == num.value and\
                    self.errorminus == num.errorminus and\
                    self.errorplus == num.errorplus and\
                    self.lowerlimit == num.lowerlimit and\
                    self.upperlimit == num.upperlimit)
        else:
            return self.value == num


    def __add__(self, num):
        """(any) -> any
        adds the value of the number to the given number, returns as expected\
        with a typical float, int, or double type
        """

        return self.value + num

    def __sub__(self, num):
        """(any) -> any
        returns the self value minus the num value
        x - y
        """

        return self.value - num

    def __lt__(self, num):
        """(any)-> any
        returns true if value of self is less than the value of num
        x < y
        """

        return self.value < num

    def __le__(self, num):
        """(any) -> any
        returns trun if self is less than or equal to the value of num
        x <= y
        """
        
        return self.value <= num

    def __ne__(self, num):
        """(any) -> any
        returns true if self value is not equal to num value
        x != y
        if num is of type number, it will check errors as well
        """

        if(num.__class__.__name__ == "number"):
            return (self.value != num.value and\
                    self.errorminus != num.errorminus and\
                    self.errorplus != num.errorplus)
        else:
            return self.value != num

    def __gt__(self, num):
        """(any)-> any
        returns true if selfs value is greater than the value of num
        x > y
        """
    
        return self.value > num
    
    def __ge__(self, num):
        """(any) -> any
        returns true if value of self is greater than or equal to value of num
        x >= y
        """

        return self.value >= num

    def __mul__(self, num):
        """(any) -> any
        returns a value of self multiplied by value of num
        x * y
        """

        return self.value * num

    def __div__(self, num):
        """(any) -> any
        x / y
        """

        return self.value / num

    def __floordiv__(self, num):
        """(any) -> any
        floor divide
        x // y
        """
        return self.value // num

    def __mod__(self, num):
        """(any) -> any
        modulus
        """

        return self.value % num

    def __divmod__(self, num):
        """(any) -> any
        dimod
        """
        return divmod(self.value, num)

    def __pow__(self, num,*z):
        """(any) -> any
        x ** y
        """
        
        return pow(self.value, num,*z)

    def __float__(self):
        """(number) -> float
        float(number.value)
        """

        return float(self.value)

    def __cmp__(self, num):

        return cmp(self.value, num)

    def __and__(self, num):

        return self.value & num

    def __abs__(self):

        return abs(self.value)

    def __coerce__(self, num):

        return coerce(self.value, num)

    def __hash__(self):

        return hash(self.value)

    def __hex__(self):

        return hex(self.value)

    def __int__(self):

        return int(self.value)

    def __invert__(self):

        return ~self.value

    def __long__(self):

        return long(self.value)

    def __lshift__(self, num):

        return self.value << num

    def __neg__(self):

        return -self.value

    def __nonzero__(self):

        return self.value != 0
    
    def __oct__(self):

        return oct(self.value)

    def __or__(self, num):

        return self.value | num

    def __pos__(self):

        return +self.value

    def __radd__(self, num):

        return num + self.value

    def __rdiv__(self, num):

        return num / self.value

    def __rdivmod(self, num):

        return divmod(num, self.value)

    def __repr__(self):

        return str(self)

    def __rfloordiv__(self, num):

        return num // self.value

    def __rlshift__(self, num):

        return num << self.value

    def __rmod__(self, num):

        return num % self.value

    def __rmul__(self, num):

        return num * self.value

    def __ror__(self,num):

        return num | self.value

    def __rpow__(self, num,*z):

        return pow(num, self.value,*z)

    def __rrshift__(self, num):

        return num >> self.value 

    def __rshift__(self, num):

        return self.value >> num

    def __rsub__(self, num):

        return num - self.value

    def __rtruediv__(self, num):

        return num / self.value

    def __rxor__(self, num):

        return num^self.value

    def __truediv__(self, num):

        return self.value / num

    def __xor__(self, num):

        return self.value^num

    def bit_length(self):

        return self.value.bit_length()

    def asymmetric(self):
        """(number) -> bool
        returns true if the error values are asymmetric
        """

        return (self.errorminus != self.errorplus)

def xml_to_obj(xml):
    """(str) -> System
    Given an xml file as a str, will return a system object
    """
    
    root = ET.fromstring(xml)
    system = System()
    for sysel in root:
        if(sysel.tag == "planet"):
            planet = Planet()
            for planel in sysel:
                if(len(planel.attrib) == 0):
                    if(planel.tag == "name"):
                        planet.name.append(planel.text)
                    else:
                        setattr(planet, planel.tag, planel.text)

                else:
                    tempnum = number(planel.text)
                    if(planel.attrib.has_key("errorminus")):
                        tempnum.errorminus = planel.attrib["errorminus"]
                    if(planel.attrib.has_key("errorplus")):
                        tempnum.errorplus = planel.attrib["errorplus"]
                    if(planel.attrib.has_key("upperlimit")):
                        tempnum.upperlimit = planel.attrib["upperlimit"]
                    if(planel.attrib.has_key("lowerlimit")):
                        tempnum.lowerlimit = planel.attrib["lowerlimit"]
                    setattr(planet, planel.tag, tempnum)
            system.children.append(planet)
        elif(sysel.tag == "star"):
            star = Star()
            for starel in sysel:
                if(starel.tag == "planet"):
                    planet = Planet()
                    for planel in starel:
                        if(len(planel.attrib) == 0):
                            if(planel.tag == "name"):
                                planet.name.append(planel.text)
                            else:
                                setattr(planet, planel.tag, planel.text)
                        else:
                            tempnum = number(planel.text)
                            if(planel.attrib.has_key("errorminus")):
                                tempnum.errorminus = planel.attrib["errorminus"]
                            if(planel.attrib.has_key("errorplus")):
                                tempnum.errorplus = planel.attrib["errorplus"]
                            if(planel.attrib.has_key("upperlimit")):
                                tempnum.upperlimit = planel.attrib["upperlimit"]
                            if(planel.attrib.has_key("lowerlimit")):
                                tempnum.lowerlimit = planel.attrib["lowerlimit"]
                            setattr(planet, planel.tag, tempnum)
                    star.children.append(planet)
                elif(len(starel.attrib) == 0):
                    if(starel.tag == "name"):
                        star.name.append(starel.text)
                    else:
                        setattr(star, starel.tag, starel.text)
                else:
                    tempnum = number(starel.text)
                    if(starel.attrib.has_key("errorminus")):
                        tempnum.errorminus = starel.attrib["errorminus"]
                    if(starel.attrib.has_key("errorplus")):
                        tempnum.errorplus = starel.attrib["errorplus"]
                    if(starel.attrib.has_key("upperlimit")):
                        tempnum.upperlimit = starel.attrib["upperlimit"]
                    if(starel.attrib.has_key("lowerlimit")):
                        tempnum.lowerlimit = starel.attrib["lowerlimit"]
                    setattr(star, starel.tag, tempnum)
            system.children.append(star)
        elif(sysel.tag == "binary"):
            binary = Binary()
            for binel in sysel:
                if(binel.tag == "star"):
                    star = Star()
                    for starel in binel:
                        if(starel.tag == "planet"):
                            planet = Planet()
                            for planel in starel:
                                if(len(planel.attrib) == 0):
                                    if(planel.tag == "name"):
                                        planet.name.append(planel.text)
                                    else:
                                        setattr(planet, planel.tag, planel.text)
                                else:
                                    tempnum = number(planel.text)
                                    if(planel.attrib.has_key("errorminus")):
                                        tempnum.errorminus = planel.attrib["errorminus"]
                                    if(planel.attrib.has_key("errorplus")):
                                        tempnum.errorplus = planel.attrib["errorplus"]
                                    if(planel.attrib.has_key("upperlimit")):
                                        tempnum.upperlimit = planel.attrib["upperlimit"]
                                    if(planel.attrib.has_key("lowerlimit")):
                                        tempnum.lowerlimit = planel.attrib["lowerlimit"]
                                    setattr(planet, planel.tag, tempnum)
                            star.children.append(planet)
                        elif(len(starel.attrib) == 0):
                            if(starel.tag == "name"):
                                star.name.append(starel.text)
                            else:
                                setattr(star, starel.tag, starel.text)
                        else:
                            tempnum = number(starel.text)
                            if(starel.attrib.has_key("errorminus")):
                                tempnum.errorminus = starel.attrib["errorminus"]
                            if(starel.attrib.has_key("errorplus")):
                                tempnum.errorplus = starel.attrib["errorplus"]
                            if(starel.attrib.has_key("upperlimit")):
                                tempnum.upperlimit = starel.attrib["upperlimit"]
                            if(starel.attrib.has_key("lowerlimit")):
                                tempnum.lowerlimit = starel.attrib["lowerlimit"]
                    binary.children.append(star)
                elif(binel.tag == "binary"):
                    binarysub = Binary()
                    for binelsub in binel:
                        if(binelsub.tag == "star"):
                            star = Star()
                            for starel in binelsub:
                                if(starel.tag == "planet"):
                                    planet = Planet()
                                    for planel in starel:
                                        if(len(planel.attrib) == 0):
                                            if(planel.tag == "name"):
                                                planet.name.append(planel.text)
                                            else:
                                                setattr(planet, planel.tag, planel.text)
                                        else:
                                            tempnum = number(planel.text)
                                            if(planel.attrib.has_key("errorminus")):
                                                tempnum.errorminus = planel.attrib["errorminus"]
                                            if(planel.attrib.has_key("errorplus")):
                                                tempnum.errorplus = planel.attrib["errorplus"]
                                            if(planel.attrib.has_key("upperlimit")):
                                                tempnum.upperlimit = planel.attrib["upperlimit"]
                                            if(planel.attrib.has_key("lowerlimit")):
                                                tempnum.lowerlimit = planel.attrib["lowerlimit"]
                                            setattr(planet, planel.tag, tempnum)
                                    star.children.append(planet)
                                elif(len(starel.attrib) == 0):
                                    if(starel.tag == "name"):
                                        star.name.append(star.text)
                                    else:
                                        setattr(star, starel.tag, starel.text)
                                else:
                                    tempnum = number(starel.text)
                                    if(starel.attrib.has_key("errorminus")):
                                        tempnum.errorminus = starel.attrib["errorminus"]
                                    if(starel.attrib.has_key("errorplus")):
                                        tempnum.errorplus = starel.attrib["errorplus"]
                                    if(starel.attrib.has_key("upperlimit")):
                                        tempnum.upperlimit = starel.attrib["upperlimit"]
                                    if(starel.attrib.has_key("lowerlimit")):
                                        tempnum.lowerlimit = starel.attrib["lowerlimit"]
                            binarysub.children.append(star)
                        elif(len(binelsub.attrib) == 0):
                            if(binelsub.tab == "name"):
                                binarysub.name.append(binelsub.text)
                            else:
                                setattr(binarysub, binelsub.tag, binelsub.text)
                        else:
                            tempnum = number(binelsub.text)
                            if(binelsub.attrib.has_key("errorminus")):
                                tempnum.errorminus = binelsub.attrib["errorminus"]
                            if(binelsub.attrib.has_key("errorplus")):
                                tempnum.errorplus = binelsub.attrib["errorplus"]
                            if(binelsub.attrib.has_key("upperlimit")):
                                tempnum.upperlimit = binelsub.attrib["upperlimit"]
                            if(binelsub.attrib.has_key("lowerlimit")):
                                tempnum.lowerlimit = binelsub.attrib["lowerlimit"]
                            setattr(binarysub, binelsub.tag, tempnum)

                    binary.children.append(binarysub)
                elif(len(binel.attrib) == 0):
                    if(binel.tag == "name"):
                        binary.name.append(binel.text)
                    else:
                        setattr(binary, binel.tag, binel.text)
                else:
                    tempnum = number(binel.text)
                    if(binel.attrib.has_key("errorminus")):
                        tempnum.errorminus = binel.attrib["errorminus"]
                    if(binel.attrib.has_key("errorplus")):
                        tempnum.errorplus = binel.attrib["errorplus"]
                    if(binel.attrib.has_key("upperlimit")):
                        tempnum.upperlimit = binel.attrib["upperlimit"]
                    if(binel.attrib.has_key("lowerlimit")):
                        tempnum.lowerlimit = binel.attrib["lowerlimit"]
                    setattr(binary, binel.tag, tempnum)
            system.children.append(binary)

        if(len(sysel.attrib) == 0):
            if(sysel.tag == "name"):
                system.name.append(sysel.text)
            else:
                setattr(system, sysel.tag, sysel.text)
        else:
            tempnum = number(sysel.text)
            if(sysel.attrib.has_key("errorminus")):
                tempnum.errorminus = sysel.attrib["errorminus"]
            if(sysel.attrib.has_key("errorplus")):
                tempnum.errorplus = sysel.attrib["errorplus"]
            if(sysel.attrib.has_key("upperlimit")):
                tempnum.upperlimit = sysel.attrib["upperlimit"]
            if(sysel.attrib.has_key("lowerlimit")):
                tempnum.upperlimit = sysel.attrib["lowerlimit"]
            setattr(system, sysel.tag, sysel.text)
        
    return system 
    

if __name__ == "__main__":

    a = xml_to_obj(open("systems/Kepler-69.xml").read())
    print(a)
