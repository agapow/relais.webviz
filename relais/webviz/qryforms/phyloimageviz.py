#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Visualise a phylogeny as a image.

"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

import StringIO

from phylotree.simpledraw import *

from relais.dev.pilutils import crop_to_content

from relais.webviz.html.simpletag import *
import baseqryviz
from config import *


__all__ = [
	'PhyloImageViz',
]


### CONSTANTS & DEFINES ###

### IMPLEMENTATION ###	
		
class PhyloImageViz (baseqryviz.BaseQryViz):
	id = __module__ + '.PhyloImageViz'.lower()
	label='Image representation of phylogeny'
	input_type = DATA_TYPE.PHYLOGENY_INSTANCE
	resources = []
	
	def render (self):
		tree = self.data
		
		coords = plot_radial_coords (tree)
		fit_coords (coords)
		canvas_size = int (float (tree.count_tip_nodes())**0.5) * 100 + 50
		drwr = TreeDrawer (canvas_size)
		drwr.draw_tree (tree, coords)
		
		img = drwr.save_to_pilimage ()
		bg_clr = img.getpixel ((0, 0))
		new_img = crop_to_content (img, bg_clr, 15)
		buff = StringIO.StringIO()
		new_img.save (buff, format='PNG')
		self.images['phylo_match.png'] = buff.getvalue()
		
		return ''
	


### TEST & DEBUG ###

def _doctest ():
	import doctest
	doctest.testmod ()


### MAIN ###

if __name__ == '__main__':
	_doctest()


### END ######################################################################
