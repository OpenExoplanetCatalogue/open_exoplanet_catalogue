#!/usr/bin/python
import xml.etree.ElementTree as ET


class System:
    """docstring goes here    """
    
    def __init__(self, object_type, **kwargs):
        """bleg"""

        for key, value in kwargs.iteritems():
            setattr(self, key, value)
        self.name = []
        self.object_type = object_type
        self.planets = []
        self.stars = []
        self.binaries = []

    def __str__(self, tab=""):
        tempstr = ""
        subtempstr = ""
        name = ""
        for tag in reversed(dir(self)):
            if(tag == "name"):
                name = tab + tag + ": " + str(getattr(self,tag)) + "\n"
            elif(tag[:4] == "add_" or tag == "str_nochild"):
                pass
            elif(tag[:2] != "__"):
                if(tag == "planets" or tag == "stars" or tag == "binary"):
                    for sub in getattr(self,tag):
                        subtempstr += sub.__str__(tab + "    ") 
                else:
                    if(getattr(self,tag) != []):
                        tempstr += tab+tag + ": " +str(getattr(self,tag)) + "\n"
        return name + tempstr + subtempstr

    def str_nochild(self):
        tempstr = ""
        name = ""
        for tag in reversed(dir(self)):
            if(tag == "name"):
                name = tag + ": " + str(getattr(self,tag)) + "\n"
            elif(tag[:4] == "add_" or tag == "str_nochild"):
                pass
            elif(tag[:2] != "__"):
                if(tag == "planets" or tag == "stars" or tag == "binary"):
                    pass
                else:
                    if(getattr(self,tag) != []):
                        tempstr += tag + ": " +str(getattr(self,tag)) + "\n"
        return name + tempstr



    def add_planet(self, planet):
        
        if(planet.object_type == "planet"):
            self.planets.append(planet)
        else:
            raise Exception("Not a planet")
    def add_star(self, star):
        if(star.object_type == "star"):
            self.stars.append(star)
        else:
            raise Exception("Not a star")

    def add_binary(self, binary):
        if(binary.object_type == "binary"):
            self.binaries.append(binary)
        else:
            raise Exception("Not a binary")

    def add_any_system(self, system):
        object_type = system.object_type
        if(object_type == "star"):
            self.add_star(system)
        elif(object_type == "planet"):
            self.add_planet(system)
        elif(object_type == "binary"):
            self.add_binary(system)
        else:
            raise Exception("Not known system type")

    def __setattr__(self, key, value):
        """ """
        if(key == "name" and type(value) == str):
            self.name.append(value)
        elif(key == "name" and type(value) == list):
            self.__dict__["name"] = value
        elif(key == "planet" and type(value) == str):
            self.planets.append(value)
        elif(key == "planet" and type(value) == list):
            self.__dict__["planets"] = value
        elif(key == "star" and type(value) == str):
            self.stars.append(value)
        elif(key == "star" and type(value) == list):
            self.__dict__["stars"] = value
        elif(key == "binary" and type(value) == str):
            self.binaries.append(value)
        elif(key == "binary" and type(value) == list):
            self.__dict__["binaries"] = value
        else:
            self.__dict__[key] = value


class number:
    """Number class for values containing errors. Math operations use the \
    the value given. Checking for no 'value' must use "=="

    num = Number(10, errorminus=0.5, errorplus=0.8)
    str(num)
    >>>10(+0.5 -0.8)

    num * 2
    >>>20

    num + 2
    >>>12

    num.errorminus
    >>>0.5

    num = Number(None, upperlimit=10)
    str(num) 
    >>>"upperlimit=10"
    
    num + 2
    >>>TypeError:....

    num == None
    >>>True

    num is None
    >>>False
    """

    def __init__(self, value, **kwargs):
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
        for key,val in kwargs.iteritems():
            setattr(self, key, value)
   

    def __str__(self):
        """(number) -> str
        Returns a string representation of the number

        example for a number with value=2.0, errorminus = 0.5, errorplus = 0.2
            2.0 (+0.5 -0.2)
        """
        tempstr = ""
        if(self.value is not None):
            tempstr += str(self.value)
        if(hasattr(self, "errorplus") and self.errorplus is not None):
            tempstr += "(+" + str(self.errorplus)
        if(hasattr(self,"errorminus") and self.errorminus is not None):
            tempstr += " -" + str(self.errorminus) + ")"
        if(hasattr(self,"upperlimit") and self.upperlimit is not None):
            tempstr += "upperlimit="+ str(self.upperlimit)
        if(hasattr(self,"lowerlimit") and self.lowerlimit is not None):
            tempstr += " lowerlimit="+ str(self.lowerlimit)
        return tempstr 

    def __setattr__(self, key, val):

        try:
            self.__dict__[key] = float(val)
        except:
            self.__dict__[key] = val

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


def xml_to_obj_helper(element):

    sys = System(element.tag)
    for el in element:
        if(len(list(el)) != 0):
            sys.add_any_system(xml_to_obj_helper(el))
        elif(len(el.attrib) == 0):
            setattr(sys, el.tag, el.text)
        else:
            tempnum = number(el.text)
            if(el.attrib.has_key("errorminus")):
                tempnum.errorminus = el.attrib["errorminus"]
            if(el.attrib.has_key("errorplus")):
                tempnum.errorplus = el.attrib["errorplus"]
            if(el.attrib.has_key("upperlimit")):
                tempnum.upperlimit = el.attrib["upperlimit"]
            if(el.attrib.has_key("lowerlimit")):
                tempnum.lowerlimit = el.attrib["lowerlimit"]
            setattr(sys, el.tag, tempnum)
    return sys

def xml_to_obj(xml):
    root = ET.fromstring(xml)
    return xml_to_obj_helper(root)


def xml_to_obj_bkup(xml):
    """(str) -> System
    Given an xml file as a str, will return a system object
    """

    root = ET.fromstring(xml)
    system = System("system")
    for sysel in root:
        if(sysel.tag == "planet"):
            planet = System("planet")
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
            system.add_planet(planet)
        elif(sysel.tag == "star"):
            star = System("star")
            for starel in sysel:
                if(starel.tag == "planet"):
                    planet = System("planet")
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
                    star.add_planet(planet)
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
            system.add_star(star)
        elif(sysel.tag == "binary"):
            binary = System("binary")
            for binel in sysel:
                if(binel.tag == "star"):
                    star = System("star")
                    for starel in binel:
                        if(starel.tag == "planet"):
                            planet = System("planet")
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
                            star.add_planet(planet)
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
                    binary.add_star(star)
                elif(binel.tag == "binary"):
                    binarysub = System("binary")
                    for binelsub in binel:
                        if(binelsub.tag == "star"):
                            star = System("star")
                            for starel in binelsub:
                                if(starel.tag == "planet"):
                                    planet = System("planet")
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
                                    star.add_planet(planet)
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
                            binarysub.add_star(star)
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
                    binary.add_binary(binarysub)
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
            system.add_binary(binary)
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

    a = xml_to_obj(open("systems/Kepler-20.xml").read())
    print(a)
    b = xml_to_obj(open("systems/WASP-99.xml").read())
    print(b)
    print("----")
    print(b.str_nochild())
