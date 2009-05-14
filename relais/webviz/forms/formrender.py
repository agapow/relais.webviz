#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base class for QryForms

"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

from django import forms
from django.forms.forms import BoundField
from django.utils.html import conditional_escape
from django.utils.encoding import StrAndUnicode, smart_unicode, force_unicode
from django.utils.safestring import mark_safe
from django.forms.util import ErrorList

from relais.webviz.html.simpletag import *

#__all__ = [
#	'TagAttrib',
#]


### CONSTANTS & DEFINES ###

### IMPLEMENTATION ###	

def allow_forms_outside_django():
	"""
	Allow the use of of Django forms outside Django.
	
	By default, at rendering Django routes all form error messages through
	internal encoding machinery that attempts to load the its settings file
	to check for internationalisation. To allow the use of use of these forms
	outside of Django, this function should be called before rendering. It
	supplies the internationalisation setting, thus preventing the problematic
	load.
	
	"""
	from django.conf import settings
	if (not settings._target):
		settings.configure (USE_I18N=False)

		
class PlainErrorList (ErrorList):
	"""
	A simple representation for error lists.
	"""
	def __unicode__ (self):
		return self.as_divs()

	def as_divs (self):
		if not self:
			return u''
		return u'<div class="error_list">%s</div>' % \
			''.join ([u'<div class="error">%s</div>' % e for e in self])


def form_as_p (frm):
	"""
	The standard paragraph styling for forms.
	"""
	assert (isinstance (frm, forms.Form))
	return frm.as_p()


def form_as_table (frm):
	"""
	The standard table styling for forms, including the 'table' tags.
	"""
	assert (isinstance (frm, forms.Form))
	return _enclose_in_table (frm.as_table())


def form_as_ul (frm):
	"""
	The standard bullet-point styling for forms.
	"""
	assert (isinstance (frm, forms.Form))
	return frm.as_ul()

	
def form_as_leftdesc_table (frm):
	"""
	The standard table styling, with the description put on the left.
	"""
	# TODO: if field.required need
	# '<span class='fieldRequired' title='Required'>(Required)</span>'
	frm.label_suffix = None
	frm.error_class = PlainErrorList
	text = frm._html_output (
		u'<tr><td><label>%(label)s</label>' \
			'<p class="discreet">%(help_text)s</p>%(errors)s</td>' \
			'<td>%(field)s</td></tr>',            # normal row
		u'<tr><td colspan="2">%s</td></tr>',     # error row
		'</td></tr>',                            # row ender
		u'<br />%s',                             # helptext
		False,                                   # errors on seperate row
	)
	return _enclose_in_table (
		closed_tag ('col') + 
		closed_tag ('col', width='50%') + 
		text
	)
		
	
def form_as_iui (frm):
	# from Andy McKay http://www.agmweb.ca/blog/andy/2173/
	return frm._html_output (
		u'<div class="row">%(label)s%(field)s%(help_text)s</div>',
		u'%s',
		'',
		u' %s',
		True
	)


def _enclose_in_table (text):
	"""
	A convenience function to enclose form html in styled table tags.
	"""
	return tag_with_contents (
		'table',
		text,
		class_='revi_formtable',
	)

	
	
### TEST & DEBUG ###

def _doctest ():
	import doctest
	doctest.testmod ()


### MAIN ###

if __name__ == '__main__':
	_doctest()


### END ######################################################################
