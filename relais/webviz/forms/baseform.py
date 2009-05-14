#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base class for QryForms

"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

from django.forms.util import ErrorList
from django import forms

from relais.dev import mountpoint, enum
from relais.dev.common import *

from relais.webviz.html.simpletag import *
import formrender

__all__ = [
	'BaseForm',
]


### CONSTANTS & DEFINES ###

DATA_TYPE = enum.Enum (
	'SAMPLE_LIST',
	'SAMPLE_GROUPS',
	'PHYLOGENY_INSTANCE',
	'BIOSEQ_LIST',
)


### IMPLEMENTATION ###

class SafeErrorList (ErrorList):
	"""
	A simple representation for error lists.
	
	The basic Django error representation does a call that eventually relies
	upon the Django configuration machinery. This removes that call and thus
	allows up to use the Django forms outside of Django.
	"""
	def __unicode__ (self):
		return self.as_divs()
	
	def as_divs (self):
		if not self:
			return u''
		return u'<div class="errorlist">%s</div>' % ''.join ([u'<div class="error">%s</div>' % e._proxy____args for e in self])


class BaseForm (object):
	"""
	A class for describing forms for rendering and execution.
	
	A common problem (in the development of Relais) has been the creation of
	forms. Too often web frameworks have their own peculiar form frameworks, 
	which means that forms must be rewritten for every framework in which they
	are used. Furthermore, some of these (and more general frameworks) are
	found wanting, often at a late stage of development.
	
	The webviz forms are an attempt to get around these problems. They use the
	Django (newforms) framework to describe forms internally while providing an
	abstract outer API that should be adapatable to most scenarios. It should
	be easy if need be to mutate the Django forms or replace them with another
	form description framework.
	
	The methods for calling form rendering, exexcution and return of results
	can be called seperately or together.
	
	"""
	# all these should be overriden by derived classes
	id = __module__ + '.BaseForm'.lower()
	label='Base form'
	description ="This is a description of base form."
	submits = ['submit']
	output_type = 'This is the sort of results we expect'
	resources = []
	
	def __init__ (self, request={}, context=None, action=None):
		"""
		C'tor for class, feeding data to form and validating it.
		
		In our scheme, a form is created in preparation for rendering, 
		validation of input and execution.
		"""
		self._formdef = self.create_form (request, context)
		self.valid_data = {}
		self.action = action
		self.output_data = None
		self.output_msgs = []
		MSG ("argh")
		
	class FormDef (forms.Form):
		pass
	
	@classmethod
	def required_resources (cls):
		"""
		What external resources should be loaded in order to render the form?
		"""
		return cls.resources
		
	def create_form (self, request, context):
		"""
		Factory method for creating the internal form definition.
		
		Can be overridden to allow the creation of dynamic forms, with variable
		fields or vocabularies.
		"""
		return self.FormDef (request, error_class=SafeErrorList)
		
	def render_body (self):
		"""
		Render the body (fields) of the form in HTML, excluding submit buttons.
		"""
		return formrender.form_as_table (self._formdef)
		
	def render_form (self):
		"""
		Render the entire form in HTML, including submit buttons and form tags.
		"""
		text = u''
		text += start_tag ('form', method="post",
			enctype="multipart/form-data") + '\n'		
		text += self.render_body ()
		text += self.render_submits()
		text += stop_tag ('form') + '\n'
		return text
		
	def render_submits (self):
		"""
		Render the submit buttons of a form in HTML.
		"""
		text = u''
		text += start_tag ('div', class_="formControls") + '\n'
		text += start_tag ('input', type_="hidden", name="_form_id",
			value=self.id)  + '\n'
		text += start_tag ('input', type_="hidden", name="form.submitted",
			value="1")  + '\n'
		for btn in self.submits:
			text += start_tag ('input', class_="context", type_="submit",
				name="form_submit", value=btn)  + '\n'
		text += stop_tag ('div') + '\n'
		return text
		
	def render_output (self):
		"""
		Render the results of a form execution.
		"""
		return self.render_output_msgs() + self.render_output_data()
		
	def render_output_msgs (self):
		return u"<P>executed</P>"
		
	def render_output_data (self):
		return u"output"
		
	def is_valid (self):
		return self._formdef.is_valid()
		
	def execute (self, context):
		"""
		Do the actual operation.
		"""
		## Preconditions:
		assert (self.is_valid())
		debug.MSG (context=context, ctype=type(context))
		## Main:
		submit_button = request.get ('submit')
		if (submit_button):
			execute_fxn_name = 'execute_' + submit_button.lower()
			if (hasattr (self, execute_fxn_name)):
				execute_fxn = getattr (self, execute_fxn_name)
				return execute_fxn (context)
		return self.execute_default (context)

	def execute_default (self, context):
		self.output_msgs.append ('foo')
		return "no operation here"
	

### TEST & DEBUG ###

def _doctest ():
	import doctest
	doctest.testmod ()


### MAIN ###

if __name__ == '__main__':
	_doctest()


### END ######################################################################
