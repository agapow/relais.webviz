#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base class for QryForms

"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

from django import forms

from relais.dev import mountpoint, enum
from relais.webviz.html.simpletag import *
from relais.webviz.forms import formrender


__all__ = [
	'BaseQryForm',
]


### CONSTANTS & DEFINES ###

DATA_TYPE = enum.Enum (
	'SAMPLE_LIST',
	'SAMPLE_GROUPS',
	'PHYLOGENY_INSTANCE',
	'BIOSEQ_LIST',
)


### IMPLEMENTATION ###	

class BaseQryForm (object):
	__metaclass__ = mountpoint.Mountpoint
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
	id = __module__ + '.BaseQryForm'.lower()
	label='Base form'
	description ="This is a description of base form."
	submits = ['submit']
	output_type = 'This is the sort of results we expect'
	resources = []
	
	def __init__ (self, request=None, context=None, action=None):
		"""
		C'tor for class, feeding data to form and validating it.

		In our scheme, a form is created in preparation for rendering, 
		validation of input and execution.
		"""
		# NOTE: request must be None or inteprets as an empty request
		self._formdef = self.create_form (request, context)
		self.valid_data = {}
		self.action = action or '.'
		self.output_data = []
		self.output_msgs = []
		self.context = context
		if (request):
			self.submit = request.get ('submit', '')
		else:
			self.submit = ''
		self._dyn_init()
		self.files = {}
		self.images = {}
		
	def _dyn_init (self):
		"""
		Initialise dynamic fields and vocabs
		"""
		#self._dyn_fields()
		self._dyn_choices()
		#self._dyn_initial()
		
	def _dyn_choices (self):
		for name, field in self._formdef.fields.items():
			fn_name = '_dyn_choices_' + name
			if hasattr (self, fn_name):
				field.choices = getattr (self, fn_name)()
				#field.choices = field_dyn_choices (self)

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
		return self.FormDef (request)

	def render_body (self):
		"""
		Render the body (fields) of the form in HTML, excluding submit buttons.
		"""
		return formrender.form_as_leftdesc_table (self._formdef)

	def render_form (self):
		"""
		Render the entire form in HTML, including submit buttons and form tags.
		"""
		text = u''
		text += start_tag ('form', method="post",
			enctype="multipart/form-data") + '\n'		
		text += self.render_body()
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
		text = u''
		for item in self.output_msgs:
			text += u'<dl class="portalMessage %(msg-class)s">' \
				'<dt>%(msg-class)s</dt><dd>%(msg-content)s</dd></dl>\n' % {
					'msg-class': item[0],
					'msg-content': item[1],
				}
		return text + '\n'

	def render_output_data (self):
		return u"output"

	def is_valid (self):
		return self._formdef.is_valid()

	def execute (self):
		"""
		Do the actual operation.
		"""
		# TODO: remove request & context as arguments
		## Preconditions:
		assert (self.is_valid()), "form isn't validated"
		## Main:
		execute_fxn_name = 'execute_' + self.submit.lower()
		if (hasattr (self, execute_fxn_name)):
			execute_fxn = getattr (self, execute_fxn_name)
			execute_fxn (self)
		else:
			self.execute_default()

	def execute_default (self):
		# TODO: remove request & context as arguments
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
