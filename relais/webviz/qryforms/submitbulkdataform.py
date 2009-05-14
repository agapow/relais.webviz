#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Form definition for submission of data in files to a Relais repository.

"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

from django import forms

import baseqryform
from config import *

__all__ = [
	'SubmitBulkDataForm',
]


### CONSTANTS & DEFINES ###

### IMPLEMENTATION ###

class SubmitBulkDataForm (baseqryform.BaseQryForm):
	id = __module__ + '.SubmitBulkDataForm'.lower()
	label='Submit data in bulk'
	description ="""Here you can submit a series of samples for
		inclusion in the database. We accept XML (in the Relais format),
		Excel or CSV (using the simple Relais tabular format). We strongly
		suggest doing a dry-run first to pick up any problesm with the
		data formatting."""
	submits = ['submit']
	output_type = DATA_TYPE.SAMPLE_GROUPS

	class FormDef (forms.Form):
		submitter = forms.CharField (
			label='Your name',
			widget=forms.TextInput (attrs={'size':'48'})
		)
		email = forms.CharField (
			label='Your email',
			widget=forms.TextInput (attrs={'size':'48'})
		)
		institution = forms.CharField (
			label='Institution',
			widget=forms.TextInput (attrs={'size':'48'})
		)
		datafile = forms.FileField (
			label='Data file',
			help_text="""Select a file (XML, Excel or CSV in the appropriate
				format) for upload.""",
		)
		overwrite = forms.BooleanField (
			label='Overwrite existing records',
			help_text="""If you have submitted data witth the same ID, overwrite
				the old records with this new data.""",
			required=False,
		)
		dryrun = forms.BooleanField (
			label='Dry run',
			help_text="""Don't actually store data, just test reading and
				if overwriting will occur""",
			required=False,
			initial=True,
		)
		report = forms.BooleanField (
			label='Report submitted data',
			help_text="""Print out a summary of the submitted data to the screen.
				Note that large submissions may create a very big summary""",
			required=True,
		)

### TEST & DEBUG ###

def _doctest ():
	import doctest
	doctest.testmod ()


### MAIN ###

if __name__ == '__main__':
	main()


### END ######################################################################
