#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base class for query result visualisations.

"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

from relais.dev import mountpoint, enum

from relais.webviz.html.simpletag import *
from config import *


__all__ = [
	'BaseQryViz',
]


### CONSTANTS & DEFINES ###

### IMPLEMENTATION ###	

class BaseQryViz (object):
	__metaclass__ = mountpoint.Mountpoint
	"""
	Base class for query result visualisations.
	
	"""
	# all these should be overriden by derived classes
	id = __module__ + '.BaseQryViz'.lower()
	label='Base query visualisation'
	description ="This is a description of BaseQryViz."
	input_type = 'This is the sort of results we expect'
	resources = []
	
	def __init__ (self, data, context=None):
		self.data = data
		self.context = context
		self.files = {}
		self.images = {}

	@classmethod
	def required_resources (cls):
		"""
		What external resources should be loaded in order to render the form?
		"""
		return cls.resources

	def render (self):
		return u'<div>blah</blah>'
	

### TEST & DEBUG ###

def _doctest ():
	import doctest
	doctest.testmod ()


### MAIN ###

if __name__ == '__main__':
	_doctest()


### END ######################################################################
