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
| `impactparameter`	| `planet` | Impact parameter of transit | |
| `epoch` | `system` | Epoch for the orbital elements | BJD |
| `period`	 	| `binary`, `planet` | Orbital period   | day  |
| `transittime` | `binary`, `planet` | Time of the center of a transit | BJD |
| `periastrontime` | `binary`, `planet` | Time of periastron | BJD |
| `maximumrvtime` | `binary`, `planet` | Time of maximum radial velocity | BJD |
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
