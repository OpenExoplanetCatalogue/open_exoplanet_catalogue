#!/usr/bin/python
import xml.etree.ElementTree as ET
class color:
    """"Colours for highlighting console print text"""
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class System:
    """System object. May be a planet, star, or binary.
   
    System type is the only required parameter for creation. The following\
    are acceptable types:

    sys = System("system")
    bin = System("binary")
    star = System("star")
    planet = System("planet")

    System parameters must be defined with a key:
    star = System("star", mass=2)

    Adding systems to each other can be done as follows

    sys.add_binary(bin)
    bin.add_star(star)
    star.add_planet(planet)
    
    setting as a property will also add to the list:
    sys.star = System("star")

    children can be accessed as follows:
    sys = System("system")
    sys.planets
    >>>['<planet1>', '<planet2>'...]
    sys.stars
    sys.binaries

    system properties can be accessed as any attribute would
    sys.mass
    >>>10
    sys.radius
    >>>15
 
    str(sys) will by default return the system and all children

    str_nochild will return the properties of just the system, no children

    str_planets, str_stars, str_binaries will return all of the given type

    """
    
    def __init__(self, object_type, **kwargs):
        """(str)->System
        arguments must be given with keys. All values and keys are assumed \
        to be correct and accurate.

        sys = System("planet", mass=10)
        sys = System("system")
        sys = System("star")
        sys = System("binary")
        """

        for key, value in kwargs.iteritems():
            setattr(self, key, value)
        self.name = []
        self.object_type = object_type
        self.planets = []
        self.stars = []
        self.binaries = []

    def __str__(self, tab=""):
        """(System, str="") -> str
        returns a string with each system property. Children are indented.\
        Name is always the first tag.

        planet = System("planet", name="foo", mass=10)
        str(planet)
        >>>name:['foo']
        mass: 10
        object_type: planet
        """

        tempstr = ""
        subtempstr = ""
        name = "\n"
        for tag in reversed(dir(self)):
            if(tag == "name" and getattr(self,tag) != []):
                name += tab + color.BOLD + tag + color.END + ": " + str(getattr(self,tag)) + "\n"
            elif(tag[:4] == "add_" or tag[:4] == "str_"):
                pass
            elif(tag[:2] != "__"):
                if(tag == "planets" or tag == "stars" or tag == "binaries"):
                    for sub in getattr(self,tag):
                        subtempstr += sub.__str__(tab + "    ") 
                else:
                    if(getattr(self,tag) != []):
                        tempstr += tab + color.BOLD + tag + color.END + ": " +str(getattr(self,tag)) + "\n"
        return name + tempstr + subtempstr

    def str_nochild(self):
        """(System) - str
        Same as str(system), but children are not included
        """

        tempstr = ""
        name = "\n"
        for tag in reversed(dir(self)):
            if(tag == "name" and getattr(self,tag) != []):
                name += color.BOLD + tag + color.END + ": " + str(getattr(self,tag)) + "\n"
            elif(tag[:4] == "add_" or tag[:4] == "str_"):
                pass
            elif(tag[:2] != "__"):
                if(tag == "planets" or tag == "stars" or tag == "binaries"):
                    pass
                else:
                    if(getattr(self,tag) != []):
                        tempstr += color.BOLD + tag + color.END + ": " +str(getattr(self,tag)) + "\n"
        return name + tempstr

    def str_planets(self):
        """Same as default str method, but only returns planet elements"""

        tempstr = ""
        for pl in self.planets:
            tempstr += pl.str_nochild()
        for st in self.stars:
            tempstr += st.str_planets()
        for bi in self.binaries:
            tempstr += bi.str_planets()
        return tempstr
    def str_stars(self):
        """Same as default str method, but only returns star elements"""

        tempstr = ""
        for st in self.stars:
            tempstr += st.str_nochild()
        for bi in self.binaries:
            tempstr += bi.str_stars()
        return tempstr
    def str_binaries(self):
        """Same as default str method, but only returns binary elements"""

        tempstr = ""
        for bi in self.binaries:
            tempstr += bi.str_nochild()
        return tempstr

    def add_planet(self, planet):
        """(System) -> NoType
        attach a planet system as a child to the given system. Planet is \
        appended to the planets list
        """
        
        if(planet.object_type == "planet"):
            self.planets.append(planet)
        else:
            raise Exception("Not a planet")
    def add_star(self, star):
        """(System) -> NoType
        attach a planet system as a child to the given system. Star is \
        appended to the stars list
        """

        if(star.object_type == "star"):
            self.stars.append(star)
        else:
            raise Exception("Not a star")

    def add_binary(self, binary):
        """(System) -> NoType
        attach a planet system as a child to the given system. Binary is \
        appended to the binaries list
        """
        if(binary.object_type == "binary"):
            self.binaries.append(binary)
        else:
            raise Exception("Not a binary")

    def add_any_system(self, system):
        """(System) -> NoType
        System is added to the list it belongs in.
        """

        object_type = system.object_type
        if(object_type == "star"):
            self.add_star(system)
        elif(object_type == "planet"):
            self.add_planet(system)
        elif(object_type == "binary"):
            self.add_binary(system)
        else:
            raise Exception("Not known system type")

    def find_system(self, name, object_type):
        """(System, str, str) -> System
        find a subsystem by its name and object_type.
        Should not have to find a system (has no parent)
        """

        if(object_type == "star"):
            for st in self.stars:
                if name in st.name:
                    return st
            for binary in self.binaries:
                return binary.find_system(name, object_type)
        elif(object_type == "planet"):
            for plan in self.planets:
                if name in plan.name:
                    return plan
            for st in self.stars:
                return st.find_system(name, object_type)
            for binary in self.binaries:
                return binary.find_system(name, object_type)
        elif(object_type == "binary"):
            for binary in self.binaries:
                if name in binary.name:
                    return binary
                else:
                    return binary.find_system(name, object_type)
        else:
            raise Exception("Not known system type")




    def __setattr__(self, key, value):
        """ """
        if(key == "name" and type(value) == str):
            self.name.append(value)
        elif(key == "name" and type(value) == list):
            self.__dict__["name"] = value
        elif(key == "planet" and type(value) == System):
            self.planets.append(value)
        elif(key == "planet" and type(value) == list):
            self.__dict__["planets"] = value
        elif(key == "star" and type(value) == System):
            self.stars.append(value)
        elif(key == "star" and type(value) == list):
            self.__dict__["stars"] = value
        elif(key == "binary" and type(value) == System):
            self.binaries.append(value)
        elif(key == "binary" and type(value) == list):
            self.__dict__["binaries"] = value
        else:
            self.__dict__[key] = value

class number:
    """Number class for values containing errors. Math operations use the \
    the value given. Checking for no 'value' must use "==". Numbers with\
    upper or lower limits as assumed to have no value.

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

        return self.value + num

    def __sub__(self, num):

        return self.value - num

    def __lt__(self, num):

        return self.value < num

    def __le__(self, num):
        
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
    
        return self.value > num
    
    def __ge__(self, num):

        return self.value >= num

    def __mul__(self, num):

        return self.value * num

    def __div__(self, num):
        
        return self.value / num

    def __floordiv__(self, num):
        
        return self.value // num

    def __mod__(self, num):

        return self.value % num

    def __divmod__(self, num):
        
        return divmod(self.value, num)

    def __pow__(self, num,*z):
        
        return pow(self.value, num,*z)

    def __float__(self):

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
    """(ElementTree.Element) -> System
    Helper function to traverse element tree to construct an arbitrary system.\
    Intended to be used with xml_to_obj
    """

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
    """(str) -> System
    Converts a str xml file to a System object. Xml file is assumed to be\
    correct in both format and content.
    """

    root = ET.fromstring(xml)
    return xml_to_obj_helper(root)

if __name__ is "__main__":
    kepler67 = xml_to_obj(open("systems/Kepler-67.xml").read())
    print(kepler67)
    print(kepler67.find_system("Kepler-67 b", "planet"))

