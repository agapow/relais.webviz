#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Form definition for searching biosequence collections from a Relais source.

"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

import exceptions

from django import forms

from relais.core.content import BioseqCollection
from relais.core.dbi.relaisconnection import RelaisConnection
from relais.core.dbi.sqlexpr import *

import baseqryform
from config import *

__all__ = [
	'SearchBseqCollsForm',
]


### CONSTANTS & DEFINES ###

### IMPLEMENTATION ###

class SearchBseqCollsForm (baseqryform.BaseQryForm):
	id = __module__ + '.SearchBseqCollsForm'.lower()
	label='Search for biosequence collections'
	description ="""Retrieve and visualise biosequence collections from the
		Relais database. Enter the search parameters below. Parameters are
		combined with a logical 'AND'. Any left blank will be treated as
		wildcards."""
	submits = ['search']
	output_type = DATA_TYPE.BSEQCOLL_GROUPS
	
	class FormDef (forms.Form):
		identifier = forms.CharField (
			help_text="The unique ID or accession for the collection.",
			widget=forms.TextInput (attrs={'size':'24'}),
			required=False,
		)
		source = forms.CharField (
			help_text="The originating authority for the collection.",
			widget=forms.TextInput (attrs={'size':'24'}),
			required=False,
		)
		title = forms.CharField (
			help_text="Text in the title of the collection.",
			widget=forms.TextInput (attrs={'size':'64'}),
			required=False,
		)
		description = forms.CharField (
			help_text="Text in the description of the collection.",
			widget=forms.TextInput (attrs={'size':'64'}),
			required=False,
		)		
		min_size = forms.IntegerField (
			label='Minimum size',
			help_text="The minimum number of biosequences in the collection.",
			required=False,
			initial=0,
			min_value=0,
		)
		limit = forms.IntegerField (
			help_text="Return at most this many collections.",
			required=False,
			initial=10,
			min_value=1,
			max_value=100,
		)
		
		presentation = forms.MultipleChoiceField (
			label="Presentation",
			help_text="How the results will be displayed.",
			choices=[
				('summary', 'Summary'),
				('listing', 'Detailed Listing'),
				# ('dl_fasta', 'Download as FASTA'),
			],
			initial='listing',
			required=True,
		)

	def execute_default (self):
		try:
			# is everything as it should be?
			assert (self.is_valid()), "parameters are invalid"
			assert (self.context), "failed to pass repository connection"
			assert (isinstance (self.context, RelaisConnection)), \
				"repository connection is invalid"

			# set up connection and parameters
			conn = self.context
			identifier = self._formdef.cleaned_data['identifier']
			source = self._formdef.cleaned_data['source']
			title = self._formdef.cleaned_data['title']
			description = self._formdef.cleaned_data['description']
			min_size = self._formdef.cleaned_data['min_size']
			limit = self._formdef.cleaned_data['limit']

			# construct expression
			expr = []
			if (identifier):
				expr.append (string_contains ('identifier', identifier))
			if (source):
				expr.append (string_contains ('source', source))
			if (description):
				expr.append (string_contains ('description', description))
			if (title):
				expr.append (string_contains ('title', title))
			if (expr):
				expr = and_list (expr)

			# make query
			if (expr):
				results = conn.select (BioseqCollection, expr)
			else:
				results = conn.select (BioseqCollection)
			
			# filter the request
			if (min_size):
				results = [r for r in results if (min_size < len (r))]
			results = results[:limit]
			self.output_data.append (results)
			
			# message
			self.output_msgs.append ((
				'info',
				'''%s biosequence collections have been found with those
					parameters.''' % len (results),
			))

		except exceptions.Exception, err:
			self.output_msgs.append ((
				'error',
				'''Execution error (%s).''' % str (err),
			))
			raise
		except:
			self.output_msgs.append ((
				'error',
				'''Execution error (unknown problem).''',
			))
			raise

	def render_output_data (self):
		text = u''
		for x in self.output_data[0]:
			text += unicode (x)
		return text


### TEST & DEBUG ###

def _doctest ():
	import doctest
	doctest.testmod ()


### MAIN ###

if __name__ == '__main__':
	main()


### END ######################################################################
