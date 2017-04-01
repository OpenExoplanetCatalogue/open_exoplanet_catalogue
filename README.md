Open Exoplanet Catalogue
==============

Status update
--------------
As you might have notice, the Open Exoplanet Catalogue has been in a a dormant state for a few months, recieving only few updates. This is mainly due to a lack of contributors. In the fall, we plan to have about 100 undergraduates in computer science to work on the OEC. Their main goal will be to implement an automated way to gather data from various sources on the internet. We will keep the data fully referenced so that it is easy to find out where the data is coming from. We will also allow manual edits of the accumulated data (as it has been in the past). All of these things together should make the OEC the most complete and most up-to-date exoplanet catalogue out there. In the meantime, please keep your pull request coming! -- Hanno Rein -- June 2016. 


About the Open Exoplanet Catalogue
--------------

[![Travis](http://img.shields.io/travis/OpenExoplanetCatalogue/open_exoplanet_catalogue/master.svg?style=flat)](https://travis-ci.org/OpenExoplanetCatalogue/open_exoplanet_catalogue/)
[![MIT](http://img.shields.io/badge/license-MIT-green.svg?style=flat)](http://opensource.org/licenses/MIT)
[![arXiv](http://img.shields.io/badge/arXiv-1211.7121-orange.svg?style=flat)](http://arxiv.org/abs/1211.7121)

The Open Exoplanet Catalogue is a database of all discovered extra-solar planets. New planets are usually added within 24 hours of their announcement.

The database is licensed under an MIT license. If you use it for a scientific publication, please include a reference to the Open Exoplanet Catalogue on [github](https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue) or to [this arXiv paper](http://arxiv.org/abs/1211.7121).  

The catalogue is a community project. Please send corrections and additions via pull request or [email](mailto:exoplanet@hanno-rein.de). If you have questions or comments about git or the database, please do not hesitate to contact of the contributors directly.

If you are looking for a simple comma/tab separated table, you might want to check out [this repository](https://github.com/OpenExoplanetCatalogue/oec_tables/).

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
A few words of caution: Many planetary systems are part of binary star systems. The architecture of these systems is correctly represented in the original XML files of the Open Exoplanet Catalogue. In fact, it is (to my knowledge) the only catalogue that can do that. However, you might prefer to work with a simpler comma or tab separated table instead of the hierarchical XML file format. During the conversion process, some information will inevitably be lost; most importantly, the architecture of the star system. One cannot easily represent an arbitrary binary/triple/quadruple system in a simple table. Additionally, if planets have multiple identifiers, only the first identifier is outputted. Using the original XML file format and git, you can use the `git blame` functionality to find references to scientific publications for every numeric value in the database. This functionality is also lost in the conversion process.

In a [separate repository](https://github.com/OpenExoplanetCatalogue/oec_tables/), you will find a [comma separated](https://github.com/OpenExoplanetCatalogue/oec_tables/raw/master/comma_separated/open_exoplanet_catalogue.txt) and a [tab separated](https://github.com/OpenExoplanetCatalogue/oec_tables/blob/master/tab_separated/open_exoplanet_catalogue.txt) ASCII table of the Open Exoplanet Catalogue. 



Documentation
--------------
[This file](https://raw.github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue/master/oec_paper.pdf) describes the philosophy and data-format of the catalogue. However, everything should be rather self-explanatory. The actual data is in the `systems` directory. Each XML file corresponds to one planetary system. 

If you are editing the file with vim, have a look at the [xmledit plugin](http://www.vim.org/scripts/script.php?script_id=301). I found it very helpful.


How to include references to publications
--------------
It seems that the most elegant place to put references to publications is in the commit message.
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
