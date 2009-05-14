#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for the pilfont provision.

"""

### IMPORTS ###

import os
import os.path

from relais.webviz import pilfonts


### CONSTANTS & DEFINES ###

### TESTS ###

class test_pilfonts (object):
	def setUp (self):
		curr_dir = os.getcwd()
		self.data_dir = os.path.join (curr_dir, 'relais', 'webviz', 'pilfonts',
			'data')
	
	def test_getfont (self):
		font_path = pilfonts.getFontPath ('18.PIL')
		expected_path = os.path.join (self.data_dir, '18.PIL')
		assert (font_path == expected_path), \
			"expected path of font '%s' is actually '%s'" % (font_path,
				expected_path)

	def test_fontpaths (self):
		assert (pilfonts._DATAPATH == self.data_dir), \
			"expected path of font data '%s' is actually '%s'" % (self.data_dir,
				pilfonts.__DATAPATH)
	
	def test_listfonts (self):
		fontlist = pilfonts.listFontsByExtension ('.pil')
		expected_fonts = [
			'profont_r400_15.pil',
			'courier_18.pil',
		]
		for item in expected_fonts:
			assert (item in fontlist), 'cannot find font %s' % item
	
	def test_listttfonts (self):
		fontlist = pilfonts.listTruetypeFonts ()
		expected_fonts = [
			'vera.ttf',
			'VeraMono.ttf',
		]
		for item in expected_fonts:
			assert (item in fontlist), 'cannot find font %s' % item



### END ########################################################################
