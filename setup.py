#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A setup script using setuptools.

If run like this::

	python setup.py install

it will install itself into the appropriate python's site packages. Although
not everyone will have setuptools, ``ez_setup.py`` is included as a bootstrap.
Those who do have setuptools, but don't have a constant internet connection
can always download a package or egg. Those who have neither are kinda stuck.

This script also installs non-programatic data, like documentation and
examples. There's no completely apt way of doing this through ``distutils`` or
``setuptools``, so one is hacked in. First, we look for the existence of
several "standard" locations for installed documentation, being:

	* ``/usr/share/doc`` (for Unix-like systems including OSX)
	* ``<sys.prefix>/share/doc`` (for Windows like systems)

The first found is chosen. The final documentation directory is then selected
as:

	DOC_DIR / LIB_NAME / vVERSION

This stops the top level documentation directory getting filled by multiple
versions of the same library. distutils / setuptools "data_files" is used to
copy the documentation across.

"""

### IMPORTS ###

# ensure setuptools is available
from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
from glob import glob

# for placing documentation
import sys
import os

# get module info
from relais.webviz import __version__

### CONSTANTS & DEFINES ###

LIBNAME = 'relais.webviz'
POSSIBLE_DOC_PATHS = [
	'/usr/share/doc',
	os.path.join (sys.prefix, 'share', 'doc'),
]
packages = [
	'relais',
	LIBNAME,
]

### SETUP ###

DOC_PATH = ''
for path in POSSIBLE_DOC_PATHS:
	if (os.path.isdir (path)):
		DOC_PATH = path
		break
DOC_PATH = os.path.join (DOC_PATH, LIBNAME, 'v' + __version__)


setup (
	# program metadata
	name = LIBNAME,
	version=__version__,
	author='Paul-Michael Agapow',
	author_email='relais@agapow.net',
	description="Web visualisation tools for ReLaIS",
	long_description="""\
	""",
	keywords=[
	],
	classifiers=[
		"Programming Language :: Python",
		"Topic :: Software Development :: Libraries :: Python Modules",
	],
	# download & distribution info
	url              = 'http://www.agapow.net/software/realis',
	download_url     = 'http://www.agapow.net/software/realis',
	license          = 'MIT',
	platforms        = ['Linux','Mac OSX'],
	# setuptools data
	test_suite       = 'nose.collector',
	packages         = find_packages(),
	data_files       = [
		# (os.path.join (DOC_PATH, 'examples'), glob ("examples/*.py")),
		# (DOC_PATH, ['LICENSE.txt', 'README.txt']),
	],
	zip_safe         = False,
	install_requires=[
		'setuptools',
		# -*- Extra requirements: -*-
	],
)
