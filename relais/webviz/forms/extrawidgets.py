#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SHORT DESCRIPTION.

"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

from django.forms import widgets

__all__ = [
	'ExSelectMultiple',
]


### CONSTANTS & DEFINES ###

### IMPLEMENTATION ###	

class ExSelectMultiple (widgets.SelectMultiple):
	def render (self, name, value, attrs=None, choices=()):
		"""
		So it can cope with single choices.
		"""
		if value is None:
			value = []
		elif (isinstance (value, basestring)):
			value = [value]
		return widgets.SelectMultiple.render (self, name, value, attrs, choices)


### TEST & DEBUG ###

def _doctest ():
	import doctest
	doctest.testmod ()


### MAIN ###

if __name__ == '__main__':
	main()


### END ######################################################################
