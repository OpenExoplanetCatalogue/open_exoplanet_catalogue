How to access the catalogue using Python 
--------------
It is very easy to access the Open Exoplanet Catalogue using python. Here is a short [snippet](https://gist.github.com/hannorein/2a069763cf114f66641c) to print out some basic planet data. No download, no installation and no external libraries are required.

```python
# python 2.x
import xml.etree.ElementTree as ET, urllib, gzip, io
url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
oec = ET.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.urlopen(url).read())))
 
# Output mass and radius of all planets 
for planet in oec.findall(".//planet"):
    print [planet.findtext("mass"), planet.findtext("radius")]
 
# Find all circumbinary planets 
for planet in oec.findall(".//binary/planet"):
    print planet.findtext("name")
 
# Output distance to planetary system (in pc, if known) and number of planets in system
for system in oec.findall(".//system"):
    print system.findtext("distance"), len(system.findall(".//planet"))
```

If you are using python 3, replace the first three lines by 

```python
import xml.etree.ElementTree as ET, urllib.request, gzip, io
url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
oec = ET.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.request.urlopen(url).read())))
```
