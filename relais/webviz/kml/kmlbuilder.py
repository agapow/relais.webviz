#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
A class for constructing KML files for Google Earth.
"""

__docformat__ = 'restructuredtext'


### IMPORTS ###

from datetime import date, datetime

from relais.core.xml import builder


### CONSTANTS & DEFINES ###

MIMETYPE_KML = 'application/vnd.google-earth.kml+xml'
MIMETYPE_KMZ = 'application/vnd.google-earth.kmz'

EXT_KML = 'kml'
EXT_KMZ = 'kmz'


### IMPLEMENTATION ###

class KmlBuilder (builder.BaseBuilder):
	def __init__ (self):
		builder.BaseBuilder.__init__ (self, 'kml',
			xmlns="http://www.opengis.net/kml/2.2")
			
	def new_folder (self, name=None, desc=None):
		folder_elem = self.new_element ('Folder')
		self.append_namedesc (folder_elem, name, desc)
		return folder_elem
		
	def add_folder (self, parent, *args, **kwargs):
		folder_elem = self.new_folder (*args, **kwargs)
		parent.append (folder_elem)
		return folder_elem
		
	def new_placemark (self, lon, lat, alt=None, name=None, desc=None,
			timestamp=None):
		pm_elem = self.new_element ('Placemark')
		self.append_namedesc (pm_elem, name, desc)
		if (timestamp is not None):
			tstamp_elem = self.add_timestamp (pm_elem, timestamp)
		point_elem = self.add_element (pm_elem, 'Point')
		coord_elem = self.add_element (point_elem, 'coordinates', desc)
		coord_text = "%s,%s" % (lon, lat)
		if (alt is not None):
			coord_text += ",%s" % alt
		coord_elem.text = coord_text
		return coord_elem
		
	def add_placemark (self, parent, *args, **kwargs):
		pm_elem = self.new_placemark (*args, **kwargs)
		parent.append (pm_elem)
		return pm_elem

	def new_timestamp (self, parent, when):
		"""
		Create a Timestamp element.
		
		:Params:
			parent
				The element this is a child of.
			when
				Either a datetime, or date or year (as integer).
				
		:Returns:
			The newly created element.
				
		"""
		## Preconditions:
		legal_pars = ['Placemark', 'Folder']
		assert parent.tag in legal_pars
		## Main:
		tstamp_elem = self.new_element ('TimeStamp')
		when_elem = self.add_element (parent, 'when')
		if (isinstance (when, date)):
			when_str = when.strftime ('%Y-%m-%d')
		elif (isinstance (when, datetime)):
			when_str = when.strftime ('%Y-%m-%dT%H:%M:%SZ')
		elif (isinstance (when, int)):
			when_str = str (when)
			assert (len (when_str) == 4)
		else:
			assert (False), "timestamp '%s' should be date or datetime" % when
		when.text = when_str
		return tstamp_elem
		
	def add_timestamp (self, parent, *args, **kwargs):
		tstamp_elem = self.new_timestamp (*args, **kwargs)
		parent.append (tstamp_elem)
		return tstamp_elem
		
	def append_namedesc (self, parent, name=None, desc=None):
		if (name is not None):
			name_elem = self.add_element (parent, 'name')
			name_elem.text = name
		if (desc is not None):
			desc_elem = self.add_element (parent, 'description')
			desc_elem.text = desc

	def write (self, dst, encoding='utf8', prettyprint=True):
		"""
		Write the tree to a file-like object.
		
		KML files are usually pretty-printed, so this method exists solely to
		provide that default.
		
		"""
		builder.BaseBuilder.write (self, dst, encoding, prettyprint)
				

### TEST & DEBUG ###

def _doctest ():
	import doctest
	doctest.testmod()


### MAIN ###

if __name__ == '__main__':
	_doctest()


### END ######################################################################
