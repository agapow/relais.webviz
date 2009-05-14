#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Functions for constructing links to web resources.
"""

__docformat__ = 'restructuredtext'



### IMPORTS ###

### CONSTANTS & DEFINES ###

GEOHACK_TMPL = """<A HREF="http://stable.toolserver.org/geohack/geohack.php?%(pagename)s&params=%(lat)s;%(lon)s_type:country">%(text)s</A>""" 


### IMPLEMENTATION ###

def locn_at_geohack (lon, lat, text="geohack", name=None, scale="country"):
	"""
	Construct a link for a location at geohack.
	
	:Params:
		lon
			Longitude, in decimal format.
		lat
			Latitude, in decimal format.
		text
			The text to appear in the link.
		name
			The name for the page.
		scale
			How much to zoom the map.
			
	:Returns:
		A string giving a hyperlink in HTML.
			
	"""
	# TODO: escape pagename
	# TODO: check for correct zoom name
	## Preconditions:
	## Main:
	if (name is None):
		pagename = ''
	else:
		pagename = 'pagename=' + name.strip()
	return GEOHACK_TMPL % {
		'pagename': ident,
		'lat': rec.get ('locn_lat'),
		'lon': rec.get('locn_lon'),
		'text': text,
	}



### TEST & DEBUG ###

def _doctest ():
	import doctest
	doctest.testmod()


### MAIN ###

if __name__ == '__main__':
	_doctest()


### END ######################################################################
