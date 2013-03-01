Open Exoplanet Catalogue Atmospheres
==============
This is a fork of the main catalogue (see [here](https://github.com/hannorein/open_exoplanet_catalogue)). The aim is to include more information useful to researchers making atmospheric observations. This includes uncertanties on all measurements and known spectral measurments.

This catalogue is an experiment and once standards are decided upon it may be merged into the original.

I am currently using the 'err' tag for unceranties on quantities eg for +-0.1 <inclination err='0.1'>88.8</inclination> or for +0.1 - 0.2 <inclination err='0.1, 0.2'>88.8</inclination>) However this may change.

If you would like to contibute please contact me at r.varley@ucl.ac.uk

Open Exoplanet Catalogue
==============
The Open Exoplanet Catalogue is a database of all discovered extra-solar planets. New planets are usually added within 24 hours of their announcement.

The database is licensed under an MIT license (see below), which basically says you can do everything with it. If you use it for a scientific publication, please include a reference to the Open Exoplanet Catalogue on [github](https://github.com/hannorein/open_exoplanet_catalogue) or to [this arXiv paper](http://arxiv.org/abs/1211.7121).  

The catalogue is maintained by Hanno Rein, Institute for Advanced Study, Princeton. However, I hope this will become a community project. Please send corrections and additions via pull request or [email](mailto:exoplanet@hanno-rein.de). If you have questions or comments about git or the database, please do not hesitate to contact me directly.

When I started this project, it was an experiment. I didn't know much about git and made a couple of stupid mistakes. The biggest mistake was to include many derived files (e.g. resized images and compressed gz files) in the repository. Whenever a single line in the catalogue was changed, those binary files changed as well. This increased the size of the repository dramatically. I therefore decided to rewrite history on November 29th 2012. I removed all derived files from the repository  and only kept the actual planet data (what is now in the systems directory). You can still access the old repository with all files [here](https://github.com/hannorein/oec_old) if you wish to do so. Note that the size of that repository is about 50 times larger (500MB compared to 10MB). 

If you are looking for a simple comma/tab separated table, you might want to check out [this repository](https://github.com/hannorein/oec_tables/).

Plots
-------------
![Mass vs semi-major axis](https://raw.github.com/hannorein/oec_plots/master/plot_mass_vs_semimajoraxis_discovery.svg.png "Plot")
![Architecture](https://raw.github.com/hannorein/oec_plots/master/plot_architecture.svg.png "Plot")
![Discovery year](https://raw.github.com/hannorein/oec_plots/master/plot_discoveryyear.svg.png "Plot")
![Period ratios](https://raw.github.com/hannorein/oec_plots/master/plot_periodratio.svg.png "Plot")

To create custom plots please visit [this repository](https://github.com/hannorein/oec_plots) for example scripts.


Download ASCII tables
--------------
A few words of caution: Many planetary systems are part of binary star systems. The architecture of these systems is correctly represented in the original XML files of the Open Exoplanet Catalogue. In fact, it is to my knowlegde the only catalogue that can do that. However, you might prefer to work with a simpler comma or tab separated table instead of the hierarchical XML file format. During the convertion process, some information is inevitably lost. Most importantly, the architecture of the star system. One cannot easily represent an arbitrary binary/tripple/quadruple system in a simple table. Additionally, if planets have multiple identifiers only the first identifier is outputted. Using the original XML file format and git, you can use the `git blame` funtionality to find references to scientific publications for every numeric value in the database. This functionality is also lost in the convertion process.

In a [separate repository](https://github.com/hannorein/oec_tables/), you will find a [comma separated](https://github.com/hannorein/oec_tables/raw/master/comma_separated/open_exoplanet_catalogue.txt) and a [tab separated](https://github.com/hannorein/oec_tables/blob/master/tab_separated/open_exoplanet_catalogue.txt) ASCII table of the Open Exoplanet Catalogue. 



Documentation
--------------
[This file](https://raw.github.com/hannorein/open_exoplanet_catalogue/master/oec_paper.pdf) describes the philosophy and data-format of the catalogue. However, everything should be rather self-explanatory. The actual data is in the `systems` directory. Each xml file corresponds to one planetary system. 

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

 * [oec_web](https://github.com/hannorein/oec_web): A suite of HTML pages acting as a front-end of the Open Exoplanet Catalogue. It includes visualizations of orbits, planet sizes and habitable zones. It also includes a plotting tool to generate correlation diagrams. The website is hosted at [openexoplanetcatalogue.com](http://openexoplanetcatalogue.com).
 * [oec_plots](https://github.com/hannorein/oec_plots): Plots and example scripts that make use of the Open Exoplanet Catalogue.
 * [oec_iphone](https://github.com/hannorein/oec_iphone): Compressed files, references to refereed publications, resized images and legacy support for various versions of the mobile version are in the repository.
 * [iPhone Exoplanet App](http://exoplanetapp.com): Popular iOS application with many visualizations of the entire catalogue. Version 9.1 and later will fully support planets in multiple star systems.


License
--------------
Copyright (C) 2012 Hanno Rein

Permission is hereby granted, free of charge, to any person obtaining a copy of this database and associated scripts (the "Database"), to deal in the Database without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Database, and to permit persons to whom the Database is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Database.
A reference to the Database shall be included in all scientific publications that make use of the Database.

THE DATABASE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE DATABASE OR THE USE OR OTHER DEALINGS IN THE DATABASE.
