#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
A collection of fonts and the functions necessary for accessing them.

A common problem in drawing libraries is finding and loading fonts. The
usual functions for these (in PIL, aggdraw, matplotlib) require a specific
single path. If this path is hardcoded in, portability issues can arise.
This module solves this problem by encompassing a group of freely available
fonts, the necessary functions to list and get the paths leading to them::

	> import fonts
	> theFPath = fonts.getFontPath ("vera.ttf")
	'C:\\Documents and Settings\agapow\My Documents\...\fonts\vera.ttf'
	> fonts.gettruetypeFonts()
	['cmex10.ttf', 'cmr10.ttf', ... 'VeraSeBd.ttf']
	
Note that the truetype fonts are made available via Bitstream, Inc. See
``COPYRIGHT.TXT`` for more details.
"""
# TODO: more fonts
# TODO: default font?
# TODO: change name style

__docformat__ = 'restructuredtext'



### IMPORTS ###

import os
import os.path
import exceptions

__all__ = [
	'',
]


### CONSTANTS & DEFINES ###

# To locate (and load or open) the fonts in this module, we need to get the
# path of this file and then of the module.
__ourPath = globals() ['__file__']
__MODULEPATH = os.path.abspath (os.path.dirname (__ourPath))
_DATAPATH = os.path.join (__MODULEPATH, 'data')


### IMPLEMENTATION ###

def getFontPath (name):
	thePath = os.path.join (_DATAPATH, name)
	if (os.path.exists (thePath)):
		return thePath
	else:
		raise exceptions.ValueError ("font '%s' cannot be found or loaded" % name)
		
def listFontsByExtension (ext):
	"""
	What fonts are available that end in this extension?
	
	Note that this is case-sensitive: '18.PIL' is different to '18.pil'.
	"""
	return [x for x in os.listdir (_DATAPATH) if x.endswith (ext)]

def listTruetypeFonts ():
	return listFontsByExtension ('.ttf')


### END #######################################################################
