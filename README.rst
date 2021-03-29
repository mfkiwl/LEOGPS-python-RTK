.. image:: https://raw.githubusercontent.com/sammmlow/LEOGPS/master/gui/logo.png

:Project: LEOGPS
:Github: https://github.com/sammmlow/LEOGPS
:Documents: https://leogps.readthedocs.io/en/stable/
:Author: Samuel Y. W. Low
:Version: 1.0 (Stable)

.. |docs| image:: https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat-square
   :target: https://leogps.readthedocs.io/en/stable/

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
   :target: https://github.com/sammmlow/LEOGPS/blob/master/LICENSE
   
.. |orcid| image:: https://img.shields.io/badge/ID-0000--0002--1911--701X-a6ce39.svg
   :target: https://orcid.org/0000-0002-1911-701X/

|docs| |license| |orcid|

LEOGPS
------

LEOGPS is an open-source Python package that takes in GPS observations of formation flying satellites in pairs, to perform single point positioning (SPP) and precise relative positioning via carrier phase double-differential GPS (CDGPS). It currently supports only observations from the GPS constellation (L1/L2 frequency), with observation files in RINEX v2.XX format. LEOGPS gives credit to the University of Bern, for the CODE precise GPS ephemeris and clock files.

.. note:: Note that for formation flying applications, the purely kinematic CDGPS approach in LEOGPS is usually accurate up to 1m for baselines less than 200km.



Installation and First Steps
----------------------------

First, clone this repository. That's the only step in installing it. The user can then run the application by running **'leogps.py'**, in the main directory, and you should see the LEOGPS GUI launch:

.. image:: https://raw.githubusercontent.com/sammmlow/LEOGPS/master/gui/gui_v1.jpg

Second, you can paste the two RINEX observation files of your LEO satellite pairs in the inputs folder, key in your configuration parameters, and hit the **'Run LEOGPS'** button. That's it! LEOGPS will automatically source for the precise daily ephemeris and clock solutions, and process the raw GPS measurements to produce a report comprising:

- The single point positions and velocities of both LEOs.
- Precise baseline vectors between the two LEOs.
- Dilution of precision values.

LEOGPS will also (optionally, depending on your choice in the GUI) output plots or reports on the interpolated GPS satellite ephemeris and clock biases. Currently ephemeris errors are still present and we are working to resolve them.

For full documentation, please refer to the `LEOGPS Read-The-Docs <https://leogps.readthedocs.io/en/stable/>`_.



Other Package Dependencies:
---------------------------

Tested on Python version 3.6.5 (Anaconda with Spyder).

Core libraries necessary: NumPy (v1.14 and above) and matplotlib

Standard Python libaries: os, copy, math, datetime, decimal, shutil, subprocess, warnings, urllib.request

Libraries for GUI: PIL, tkinter

The above are all standard Python libraries that should come with a typical Anaconda installation.

This README was last updated on: 29-March-2021.



Contact:
--------

If you have any queries feel free to reach out to me at:

sammmlow@gmail.com