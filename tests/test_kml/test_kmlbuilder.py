#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for relais.webviz.kml.kmlbuilder, using nose.

"""

### IMPORTS ###

from relais.webviz.kml import kmlbuilder


### CONSTANTS & DEFINES ###

OUTPATH = 'tests/out/kml/'


### TESTS ###

def test_ctor():
	bldr = kmlbuilder.KmlBuilder()
	out = OUTPATH + 'test_ctor.kml'
	bldr.write (out)
	

def test_new_folder():
	bldr = kmlbuilder.KmlBuilder()
	f1 = bldr.new_folder()
	assert (len (f1) == 0)
	f2 = bldr.new_folder (name='ABC')
	assert (len (f2) == 1)
	f3 = bldr.new_folder (desc='DEF HIJ')
	assert (len (f3) == 1)
	f4 = bldr.new_folder (name='ABC', desc='DEF HIJ')
	assert (len (f4) == 2)



### END ######################################################################
