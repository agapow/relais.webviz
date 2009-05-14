#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Form definition for matching a submitted sequence against a Relais repository.

"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

import exceptions

from django import forms
from phylotree.reconstruct import nj
from phylotree.tree import Ptree

from relais.core.dbi.relaisconnection import RelaisConnection
from relais.core.content import BioseqCollection, Biosequence
from relais.core.bpcompat import convert
from relais.analysis import clustal, fasta, mafft
from relais.dev.common import *
from relais.dev.io.utils import readable_from_string
from relais.analysis.reconstruct import qjoincline, qjoinreader
from relais.dev.htmltag import * 

from relais.webviz.forms import (extrafields, extravalidators, extrawidgets)
from config import DATA_TYPE
import baseqryform
from phyloimageviz import *
from phylotextviz import *
from fastamatchviz import *


__all__ = [
	'MatchSequenceForm',
]


### CONSTANTS & DEFINES ###

SEQLIMIT = 150


### IMPLEMENTATION ###

class MatchBseqForm (baseqryform.BaseQryForm):
	id = __module__ + '.MatchSequenceForm'.lower()
	label='Match sequences'
	description ="""Here you can enter and sequence and search for matches
		or near-relatives via phylogenetic reconstruction. Several sets
		of reference sequences are provided for matching. Note that due to
		security and curating, not all sequences are available as part of
		reference sets."""
	submits = ['match']
	output_type = DATA_TYPE.PHYLOGENY_INSTANCE,
	
	def _dyn_choices_refsets (self):
		# TODO: correct 
		if (self.context and isinstance (self.context, RelaisConnection)):
			bcolls = self.context.get_all_objs (BioseqCollection)
			choices = [[x.identifier, '%s (%s seqs)' % (x.title or x.identifier,
				len (x))] for x in bcolls if (0 < len (x))]
			return choices
		else:
			return []
			
	def execute_default (self):
		try:
			# is everything as it should be?
			assert (self.is_valid()), "parameters are invalid"
			assert (self.context), "failed to pass repository connection"
			assert (isinstance (self.context, RelaisConnection)), \
				"repository connection is invalid"
			
			# set up connection and parameters
			conn = self.context
			bioseq = self._formdef.cleaned_data['bioseq']
			refsets = self._formdef.cleaned_data['refsets']
			method = self._formdef.cleaned_data['method']
			
			# get collections, to get bioseq ids, to get bioseqs
			bioseqcolls = conn.get_objs_by_id (BioseqCollection, refsets)
			bioseq_ids = []
			for coll in bioseqcolls:
				for b_id in coll:
					if b_id not in bioseq_ids:
						bioseq_ids.append (b_id)
			bioseqs = conn.get_objs_by_id (Biosequence, bioseq_ids)
			assert (2 <= len (bioseqs)), \
				"too few biosequences (%s) to compare against" % len (bioseqs)
			if (SEQLIMIT):
				assert (len (bioseqs) <= SEQLIMIT), "you have selected %s reference sequences, %s is the limit" % (len (bioseqs), SEQLIMIT)
			MSG (bioseq_ids, len (bioseqs))
			
			# add test sequence, convert to biopython seqrecs
			test_bseq = Biosequence (identifier='TEST', title='TEST', 
				seqdata=bioseq)
			bioseqs.append (test_bseq)
			bp_seqrecs = [convert.bioseq_to_bp_seqrec (x, False, False) for x
				in bioseqs]
			# build description table
			seq_descs = []
			for s in bp_seqrecs:
				new_desc = []
				title, ident = s.name.strip(), s.id.strip()
				if (title) and ('unknown ' not in title):
					name = u'%s (%s)' % (title, ident)
				else:
					name = ident
				seq_descs.append ((name, s.description))
			seq_descs = tuple (seq_descs)
			self.output_data.append (seq_descs)
			
			# align and build tree
			MSG (method)
			if ('nj_qjoin' in method):
				#bp_alignment = clustal.align_with_clustal (bp_seqrecs)
				mafft_app = mafft.MafftCline()
				mafft_app.run_fftns (bp_seqrecs)
				bp_alignment = mafft_app.extract_results()
				#nameseq_pairs = [(x.id, str (x.seq)) for x in bp_alignment]
				#treebuilder = nj.NjReconstructor()
				#phyl = treebuilder.reconstruct (nameseq_pairs)
				cli = qjoincline.QjoinCline()
				cli.run (bp_alignment)
				phyl = cli.extract_results()
				#MSG ('Collected results:\n', results)
				#rdr = qjoinreader.QjoinReader (readable_from_string (results))
				#phyl = rdr.read()
				MSG ('Produced tree of size', len (phyl))
				#
				MSG (phyl, len (phyl))
				self.output_data.append (phyl)
				# report
				self.output_msgs.append ((
					'info',
					'''Your sequence (named 'TEST') has been aligned with the
						reference sequences and built into a phylogeny.''',
				))
			
			# do the fasta stuff
			if ('fasta' in method):
				fcline = fasta.FastaCline()
				fcline.run (bp_seqrecs[0], bp_seqrecs[1:])
				f_results = fcline.extract_results()
				MSG (f_results)
				self.output_data.append (f_results)
				# report
				self.output_msgs.append ((
					'info',
					'''Your sequence (named 'TEST') has been matched against the
					 	reference sequences via FASTA with the results below.''',
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
		for data in self.output_data:
			if isinstance (data, Ptree):
				for viz_class in [PhyloTextViz, PhyloImageViz]:
					viz = viz_class (data)
					text += viz.render()
					self.images.update (viz.images)
					self.files.update (viz.files)
			elif (isinstance (data, tuple)):
				text += tag_with_contents ('p', 'The submitted data was  matched against the following sequences:')
				rows = []

				header_names = ['Seq. name', 'Description']
				header_cells = [tag_with_contents ('th', x, class_="nosort column") for x in header_names]
				rows.append (header_cells)

				for record in data:
					MSG (record)
					curr_row = []
					curr_row.append (tag_with_contents ('td', record[0]))
					curr_row.append (tag_with_contents ('td', record[1]))
					rows.append (curr_row)

				row_text = [tag_with_contents ('tr', ''.join (row)) for
					row in rows]
				thead_text = tag_with_contents ('thead', row_text[0])
				tbody_text = tag_with_contents ('tbody', '\n'.join (row_text[1:]))
				table_text = tag_with_contents ('table', thead_text + tbody_text,
					class_="listing", id_="seq_desc")
				text +=  tag_with_contents ('div', table_text)
				
			else:
				for viz_class in [FastaMatchViz]:
					viz = viz_class (data)
					text += viz.render()
					self.images.update (viz.images)
					self.files.update (viz.files)
		return text

	class FormDef (forms.Form):
		if (SEQLIMIT):
			seqlimit_help = " Comparisons can be made against up to %s sequences." % SEQLIMIT
		else:
			seqlimit_help = ''
		bioseq = forms.CharField (
			label='Sequence data',
			help_text="""Enter a nucleotide sequence to be tested against a
				reference set. It should just be the sequence and not contain
				identifiers or annotations. Any whitespace will be scrubbed before
				matching.""" + seqlimit_help,
			required=True,
			widget=forms.widgets.Textarea (attrs={
				'rows': 5,
				'cols': 60,
				'wrap': 'soft',
				'style': 'overflow-y: scroll',
				'class': 'biosequence'
			}),
		)
		refsets = extrafields.ExMultipleChoiceField (
			label="Reference sets",
			help_text="""The following sets of reference sequences are
				available for you to match against.""",
			choices=[['dynchoice', 'dynchoice'], ['B', 'kkkkk']],
			required=True,
			widget=forms.widgets.SelectMultiple (attrs={'size':5}), 
		)
		method = extrafields.ExMultipleChoiceField (
			label="Method",
			help_text="""Select the method for comparing sequences: 
				reconstruction of phylogeny via neighbour joining or FASTA
				sequence comparision.""",
			choices=[
				('nj_qjoin', 'Neighbour-joining (using qjoin)'),
				('fasta', 'FASTA'),
			],
			initial=['nj'],
			required=True,
			widget=extrawidgets.ExSelectMultiple,
		)
		
		def clean_bioseq (self):
			bseq_data = self.cleaned_data['bioseq']
			data = extravalidators.clean_whitespace (bseq_data)
			data = extravalidators.validate_nonblank (data)
			data = extravalidators.validate_alphabet (data,
				alpha='GATCRYWSMKHBVDN-', case_insensitive=True)
			return data


### TEST & DEBUG ###

def _doctest ():
	import doctest
	doctest.testmod ()


### MAIN ###

if __name__ == '__main__':
	main()


### END ######################################################################
