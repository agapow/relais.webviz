#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
A class for recording samples in KML files.
"""
# TODO: include a "produced by ReLaIS" comment?
# TODO: style to seperate folders?

__docformat__ = 'restructuredtext'


### IMPORTS ###

import kmlbuilder


### CONSTANTS & DEFINES ###

### IMPLEMENTATION ###

class SampleBuilder (kmlbuilder.KmlBuilder):
	def __init__ (self):
		kmlbuilder.KmlBuilder.__init__ (self)
			
	def new_sample (self, sample, style=None):
		when = sample.date_collected
		locn = sample.location
		name = sample.get_name()
		desc = sample.desc
		pm_elem = self.new_placemark (lon=locn.lon, lat=lon.lat, name=name,
			desc=desc, timestamp=when)
		return pm_elem
		
	def append_sample (self, parent, sample, style=None):
		"""
		Write the data for a folder full of samples.
		"""
		sample_elem = self.new_sample (sample, style)
		parent.append (sample_elem)
		
	def append_samples_in_folder (self, samples, name=None, desc=None):
		"""
		Write the data for a folder full of samples.
		"""
		folder_elem = self.add_folder (self.root, name=name, desc=desc)
		for s in samples:
			self.append_sample (folder_elem, s)



### TEST & DEBUG ###

def _doctest ():
	import doctest
	doctest.testmod()


### MAIN ###

if __name__ == '__main__':
	_doctest()


### END ######################################################################
