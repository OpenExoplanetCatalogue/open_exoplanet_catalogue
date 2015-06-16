Open Exoplanet Catalogue
==============

[![Travis](http://img.shields.io/travis/OpenExoplanetCatalogue/open_exoplanet_catalogue/master.svg?style=flat)](https://travis-ci.org/OpenExoplanetCatalogue/open_exoplanet_catalogue/)
[![MIT](http://img.shields.io/badge/license-MIT-green.svg?style=flat)](http://opensource.org/licenses/MIT)
[![arXiv](http://img.shields.io/badge/arXiv-1211.7121-orange.svg?style=flat)](http://arxiv.org/abs/1211.7121)

The Open Exoplanet Catalogue is a database of all discovered extra-solar planets. New planets are usually added within 24 hours of their announcement.

The database is licensed under an MIT license (see below), which basically says you can do everything with it. If you use it for a scientific publication, please include a reference to the Open Exoplanet Catalogue on [github](https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue) or to [this arXiv paper](http://arxiv.org/abs/1211.7121).  

The catalogue is a community project. Please send corrections and additions via pull request or [email](mailto:exoplanet@hanno-rein.de). If you have questions or comments about git or the database, please do not hesitate to contact of the contributors directly.

If you are looking for a simple comma/tab separated table, you might want to check out [this repository](https://github.com/OpenExoplanetCatalogue/oec_tables/).

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

Data Structure
-------------
The following table shows all the possible tags in the Open Exoplanet Catalogue. 

| Tag      | Can be child of | Description | Unit |
| -------- | --------------- | ----------- | ---- |
| `system` |                 | This is the root container for an entire planetary system |  |
| ` planet` | `system`, `binary`, `star` | This is the container for a single planet. The planet is a free floating (orphan) planet if this tag is a child of `system`. | 
| `star`  | `system`, `binary` | This is the container for a single star. A star can be host to one or more planets (circum-stellar planets). | 
| `binary` 		| `system`, `binary` | A binary consists of either two stars, one star and one binary or two binaries. In addition a binary can be host to one or more planets (circum-binary planets).| |
| | | | |
| `declination`	| `system` | Declination | +/- dd mm ss   |
| `rightascension`	| `system` | Right ascension | hh mm ss   |
| `distance`		| `system` | Distance from the Sun | parsec   |
| `name`		| `system`, `binary`, `star`, `planet` | Name of this object. This tag can be used multiple times if the object has multiple Names. |   |
| `semimajoraxis` 	| `binary`, `planet` | Semi-major axis of a planet (heliocentric coordinates) if child of `planet`. Semi-major axis of the binary if child of `binary`. |  AU |
| `separation`	 	| `binary`, `planet` | Projected separation of planet from its host, or if child of `binary` the projected separation from one component to the other. This tag can occur multiple times with different units. It is different from the tag `semimajoraxis` as it does not imply a specific orbital configuration. |  AU, arcsec |
| `positionangle` | `binary` | Position angle | degree |
| `eccentricity` 	| `binary`, `planet` | Eccentricity  | |
| `periastron` 	| `binary`, `planet` | Longitude of periastron | degree  |
| `longitude` 	| `binary`, `planet` | Mean longitude at a given Epoch (same for all planets in one system) | degree  |
| `meananomaly`	| `binary`, `planet` | Mean anomaly at a given Epoch (same for all planets in one system) | degree  |
| `ascendingnode` 	| `binary`, `planet` | Longitude of the ascending node | degree  |
| `inclination` 	| `binary`, `planet` | Inclination of the orbit | degree  |
| `epoch` | `system` | Epoch for the orbital elements | BJD |
| `period`	 	| `binary`, `planet` | Orbital period   | day  |
| `transittime` | `binary`, `planet` | Time of the center of a transit | BJD |
| `periastrontime` | `binary`, `planet` | Time of periastron | BJD |
| `mass`		| `planet`, `star` |Mass (or m sin(i) for radial velocity planets) | Jupiter masses (`planet`), Solar masses (`star`)  |
| `radius`		| `planet`, `star` |Physical radius | Jupiter radii (`planet`), Solar radii (`star`)  |
| `temperature`	| `planet`, `star` |Temperature (surface or equilibrium) | Kelvin  |
| `age`		| `planet`, `star` |Age | Gyr  |
| `metallicity`	| `star` | Stellar metallicity  | log, relative to solar  |
| `spectraltype`	| `star`, `planet` | Spectral type  |   |
| `magB`		| `binary`, `star`, `planet` | B magnitude |   |
| `magV`		| `binary`, `star`, `planet` | Visual magnitude |   |
| `magR`		| `binary`, `star`, `planet` | R magnitude |   |
| `magI`		| `binary`, `star`, `planet` | I magnitude |   |
| `magJ`		| `binary`, `star`, `planet` | J magnitude |   |
| `magH`		| `binary`, `star`, `planet` | H magnitude |   |
| `magK`		| `binary`, `star`, `planet` | K magnitude |   |
| | | | |
| `discoverymethod` 	| `planet` | Discovery method of the planet. For example: timing, RV, transit, imaging.  |   |
| `istransiting` 	| `planet` | Whether the planet is transiting (1) or not (0).  |   |
| `description` 	| `planet` | Short description of the planet  |   |
| `discoveryyear`	| `planet` | Year of the planet's discovery | yyyy  |
| `lastupdate`	| `planet` | Date of the last (non-trivial) update | yy/mm/dd   |
| `spinorbitalignment` | `planet` | Rossiter-McLaughlin Effect. | degree |

Errors
-------------
Uncertainties can be added to values using the following attributes of the tag. We assume that these uncertainties represent the standard error of the measurement (68.2% confidence level). However, keep in mind that it is often not possible to collapse an entire posterior distribution to a single number.

The syntax for error bars is: `<mass errorminus="0.1" errorplus="0.1">1.0</mass>`

The syntax for upper/lower limits is: `<mass upperlimit="1.0" />`

Constants
-------------
There are several constant used in defining the units in the Open Exoplanet Catalogue. The following table can be used to convert them into SI units.

| Constant used in catalogue | Definition in SI units |
| -------- | --------------- |
| Jupiter mass | 1.8991766e+27 kg |
| Solarmass | 1.9891e+30 kg |
| Jupiter radius | 69911000 m |
| Solarradius | 6.96e+08 m |


Plots
-------------
![Mass vs semi-major axis](https://raw.github.com/OpenExoplanetCatalogue/oec_plots/master/plot_mass_vs_semimajoraxis_discovery.svg.png "Plot")
![Architecture](https://raw.github.com/OpenExoplanetCatalogue/oec_plots/master/plot_architecture.svg.png "Plot")
![Discovery year](https://raw.github.com/OpenExoplanetCatalogue/oec_plots/master/plot_discoveryyear.svg.png "Plot")
![Period ratios](https://raw.github.com/OpenExoplanetCatalogue/oec_plots/master/plot_periodratio.svg.png "Plot")

To create custom plots please visit [this repository](https://github.com/OpenExoplanetCatalogue/oec_plots) for example scripts.


Download ASCII tables
--------------
A few words of caution: Many planetary systems are part of binary star systems. The architecture of these systems is correctly represented in the original XML files of the Open Exoplanet Catalogue. In fact, it is to my knowledge the only catalogue that can do that. However, you might prefer to work with a simpler comma or tab separated table instead of the hierarchical XML file format. During the conversion process, some information is inevitably lost. Most importantly, the architecture of the star system. One cannot easily represent an arbitrary binary/triple/quadruple system in a simple table. Additionally, if planets have multiple identifiers only the first identifier is outputted. Using the original XML file format and git, you can use the `git blame` functionality to find references to scientific publications for every numeric value in the database. This functionality is also lost in the conversion process.

In a [separate repository](https://github.com/OpenExoplanetCatalogue/oec_tables/), you will find a [comma separated](https://github.com/OpenExoplanetCatalogue/oec_tables/raw/master/comma_separated/open_exoplanet_catalogue.txt) and a [tab separated](https://github.com/OpenExoplanetCatalogue/oec_tables/blob/master/tab_separated/open_exoplanet_catalogue.txt) ASCII table of the Open Exoplanet Catalogue. 



Documentation
--------------
[This file](https://raw.github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue/master/oec_paper.pdf) describes the philosophy and data-format of the catalogue. However, everything should be rather self-explanatory. The actual data is in the `systems` directory. Each XML file corresponds to one planetary system. 

If you are editing the file with vim, have a look at the [xmledit plugin](http://www.vim.org/scripts/script.php?script_id=301). I found it very helpful.


How to include references to publications
--------------
It seems that the most elegant place to put references to publications is the commit message.
This allows one to trace back each individual value in the database to the source using `git blame`. 
Furthermore it does not add any additional clutter to the text files themselves.
So, when committing any changes, please create one commit per publication and include the reference in the commit message from now on.


Derived products
--------------
The following list contains links to other catalogues, websites and apps that are derived from or make use of the Open Exoplanet Catalogue.

 * [oec_web](https://github.com/OpenExoplanetCatalogue/oec_web): A suite of HTML pages acting as a front-end of the Open Exoplanet Catalogue. It includes visualizations of orbits, planet sizes and habitable zones. It also includes a plotting tool to generate correlation diagrams. The website is hosted at [openexoplanetcatalogue.com](http://openexoplanetcatalogue.com).
 * [oec_plots](https://github.com/OpenExoplanetCatalogue/oec_plots): Plots and example scripts that make use of the Open Exoplanet Catalogue.
 * [oec_outreach](https://github.com/hannorein/oec_outreach): A clone of the main repository with images and tags that are mainly used for outreach purposes.
 * [oec_iphone](https://github.com/hannorein/oec_iphone): Compressed files, references to refereed publications, resized images and legacy support for various versions of the mobile version are in the repository.
 * [ExoData](https://github.com/ryanvarley/ExoData): A Python module for loading the catalogue into python for use with applications along with many exoplanet related equations and tools.
 * [iPhone Exoplanet App](http://exoplanetapp.com): Popular iOS application with many visualizations of the entire catalogue. Version 9.1 and later will fully support planets in multiple star systems.


License
--------------
Copyright (C) 2012 Hanno Rein

Permission is hereby granted, free of charge, to any person obtaining a copy of this database and associated scripts (the "Database"), to deal in the Database without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Database, and to permit persons to whom the Database is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Database.
A reference to the Database shall be included in all scientific publications that make use of the Database.

THE DATABASE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE DATABASE OR THE USE OR OTHER DEALINGS IN THE DATABASE.
