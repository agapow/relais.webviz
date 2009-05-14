#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Form definition for searching and visualsing samples from a Relais source.

"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

from django import forms

import baseqryform
from config import *

__all__ = [
	'SearchSamplesForm',
]


### CONSTANTS & DEFINES ###

### IMPLEMENTATION ###

class SearchSamplesForm (baseqryform.BaseQryForm):
	id = __module__ + '.SearchSamplesForm'.lower()
	label='Search for samples'
	description ="""Retrieve and visualise samples from the Relais
		database. Enter the search parameters below. Parameters are combined
		with a logical 'AND'. Any left blank will be treated as wildcards."""
	submits = ['search']
	output_type = DATA_TYPE.SAMPLE_GROUPS
	
	class FormDef (forms.Form):
		identifier = forms.CharField (
			label='Your name',
			help_text="The unique ID or accession for the sample.",
			widget=forms.TextInput (attrs={'size':'24'}),
			required=False,
		)
		fromdate = forms.DateField (
			label='From date',
			help_text="The earliest date for collection of the sample",
			required=False,
		)
		todate = forms.DateField (
			label='To date',
			help_text="The latest date for collection of the sample",
			required=False,
		)
		outcomes = forms.MultipleChoiceField (
			label="Final outcome",
			help_text="""What strain was finally recorded, if any. Multiple
				selections can be made.""",
			choices=[['A', 'The A'], ['B', 'kkkkk']],
			required=False,
		)
		regions = forms.MultipleChoiceField (
			label="Region",
			help_text="Country of origin. Multiple selections can be made.",
			choices=[['A', 'The A'], ['B', 'kkkkk']],
			required=False,
		)
		status = forms.MultipleChoiceField (
			label="Status",
			help_text="""Type of report or diagnosis progress. Multiple
				selections can be made.""",
			choices=[['A', 'The A'], ['B', 'kkkkk']],
			required=False,
		)
		groupby = forms.ChoiceField (
			label="Group",
			help_text="Seperate and distinguish the results?",
			choices=[
				('', 'No'),
				('country', 'Country'),
				('host', 'Host'),
				('result', 'Result'),
				('status', 'Status'),
				('year', 'Year'),
			],
			required=False,
		)
		host = forms.CharField (
			label='Host',
			help_text="Host species or animal type.",
			widget=forms.TextInput (attrs={'size':'24'}),
			required=False,
		)
		limit = forms.IntegerField (
			label='Limit',
			help_text="Restrict the number of results returned.",
			initial=100,
			min_value=1,
			max_value=200,
			required=True,
		)
		presentation = forms.MultipleChoiceField (
			label="Presentation",
			help_text="How the results will be displayed.",
			choices=[
				('table', 'Table'),
				('map', 'Map'),
				#('graph', 'Graph'),
			],
			initial='table',
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
