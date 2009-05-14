#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Visualise a phylogeny as simple text (a Newick tree).

"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

from relais.dev.common import *

from relais.webviz.html.simpletag import *
import baseqryviz
from config import *


__all__ = [
	'PhyloTextViz',
]


### CONSTANTS & DEFINES ###

### IMPLEMENTATION ###	
		
class PhyloTextViz (baseqryviz.BaseQryViz):
	id = __module__ + '.PhyloTextViz'.lower()
	label='Text representation of phylogeny'
	input_type = DATA_TYPE.PHYLOGENY_INSTANCE
	resources = []
	
	def render (self):
		from phylotree.io.newick import NewickWriter
		from StringIO import StringIO
		buffer = StringIO()
		tree = self.data
		MSG (tree, type (tree))
		writer = NewickWriter()
		writer.write (tree, buffer)
		treestr = buffer.getvalue()
		return tag_with_contents ('div', treestr, class_="revi_treestring")
	


### TEST & DEBUG ###

def _doctest ():
	import doctest
	doctest.testmod ()


### MAIN ###

if __name__ == '__main__':
	_doctest()


### END ######################################################################
