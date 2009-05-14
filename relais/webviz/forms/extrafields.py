#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Extra fields for use with django forms.

"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

from django.forms import fields

__all__ = [
	'ExMultipleChoiceField',
]


### CONSTANTS & DEFINES ###

### IMPLEMENTATION ###	

class ExMultipleChoiceField (fields.MultipleChoiceField):
	"""
	An extension of the standard MultipleChoiceField.
	
	Currently, the sole modification is to allow a single (non-sequence) value
	to be passed in and accepted as a valid choice. This is because if two or
	more values are chosen, the request contains them as a list::
	
		['A', 'B']
		
	while if only one choice the request holds::
		
		'A'
		
	"""
	# TODO: allow min and max choices
	
	def clean (self, value):
		"""
		Validates that the input is a list or tuple.
		"""
		if ((value) and not isinstance (value, (list, tuple))): 
			value = [value]
		return fields.MultipleChoiceField.clean (self, value)


### TEST & DEBUG ###

def _doctest ():
	import doctest
	doctest.testmod ()


### MAIN ###

if __name__ == '__main__':
	main()


### END ######################################################################
