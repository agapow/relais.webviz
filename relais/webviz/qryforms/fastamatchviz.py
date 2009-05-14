#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Renders Fasta results as a table.

"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

from relais.dev.common import *

from relais.webviz.html.simpletag import *
import baseqryviz
from config import *


__all__ = [
	'FastaMatchViz',
]


### CONSTANTS & DEFINES ###

### IMPLEMENTATION ###	
		
class FastaMatchViz (baseqryviz.BaseQryViz):
	id = __module__ + '.FastaMatchViz'.lower()
	label='Table of Fasta results'
	input_type = None
	resources = []
	
	def render (self):
		rows = []
		
		header_names = ['Seq. ID', 'Ident.', 'Diff.', 'Nt compared', 'Nt. matched', 'Nt. Ambig.', ]
		header_cells = [tag_with_contents ('th', x, class_="nosort column") for x in header_names]
		rows.append (header_cells)
		
		for record in self.data:
			curr_row = []
			curr_row.append (tag_with_contents ('td', record.seq_id))
			curr_row.append (tag_with_contents ('td', '%.2f' % record.frac_identity))
			curr_row.append (tag_with_contents ('td', '%.2f' % record.frac_difference))
			curr_row.append (tag_with_contents ('td', '%d' % record.res_compared))
			curr_row.append (tag_with_contents ('td', '%d' % record.res_matched))
			curr_row.append (tag_with_contents ('td', '%d' % record.res_ambigs))
			rows.append (curr_row)
			
		row_text = [tag_with_contents ('tr', ''.join (row)) for row in rows]
		thead_text = tag_with_contents ('thead', row_text[0])
		tbody_text = tag_with_contents ('tbody', '\n'.join (row_text[1:]))
		table_text = tag_with_contents ('table', thead_text + tbody_text,
			class_="listing", id_="fasta_res")
		
		leader_txt = tag_with_contents ('p', "The following are the best %s matches with the test sequence:" % len (self.data))
		
		return tag_with_contents ('div', leader_txt + table_text)
	


### TEST & DEBUG ###

def _doctest ():
	import doctest
	doctest.testmod ()


### MAIN ###

if __name__ == '__main__':
	_doctest()


### END ######################################################################
