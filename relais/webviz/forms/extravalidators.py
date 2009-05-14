#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Extra validators for use with django forms.

This should be called from validation functions within Django and are all
of the form::

	validate_x (data, ...) => clean and valid data
	clean_x (data, ...) => clean data

"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

import re

from django import forms

from relais.dev.common import *

__all__ = [
	'ExMultipleChoiceField',
	'validate_nonblank',
	'clean_whitespace',
	'validate_alphabet',
]


### CONSTANTS & DEFINES ###

WHITESPACE_RE = re.compile ('\s+')


### IMPLEMENTATION ###

def unique (iterable):
	uniq_data = []
	for x in iterable:
		if (x not in uniq_data):
			uniq_data.append (x)
	return uniq_data


def clean_whitespace (data):
	"""
	Removes all whitespace from data.
	"""
	return WHITESPACE_RE.sub ('', data)


def validate_alphabet (data, alpha, case_insensitive=False, msg=None):
	"""
	Ensure all characters of data are within the given alphabet.
	"""
	uniq_data = []
	for x in data:
		if (x not in uniq_data):
			uniq_data.append (x)
	if (case_insensitive):
		alpha = alpha.lower()
		uniq_data = ''.join (uniq_data).lower()
	illegal_chars = [x for x in uniq_data if x not in alpha]
	if illegal_chars:
		msg = msg or "The input contains the illegal characters '%s'." % \
			''.join (illegal_chars)
		raise forms.ValidationError (msg)
	return data
	
	
def validate_nonblank (data, msg=None):
	if (not data):
		msg = msg or "The input is blank."
		raise forms.ValidationError (msg)
	else:
		return data



### TEST & DEBUG ###

def _doctest ():
	import doctest
	doctest.testmod ()


### MAIN ###

if __name__ == '__main__':
	main()


### END ######################################################################
