#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Various constants for the relai.webviz.qryforms module.

"""

__docformat__ = 'restructuredtext en'


### IMPORTS ###

from relais.dev import enum

__all__ = [
	'DATA_TYPE',
]


### CONSTANTS & DEFINES ###

DATA_TYPE = enum.Enum (
	'SAMPLE_LIST',
	'SAMPLE_GROUPS',
	'PHYLOGENY_INSTANCE',
	'BIOSEQ_LIST',
	'BSEQCOLL_GROUPS',
)


### IMPLEMENTATION ###	

### TEST & DEBUG ###

def _doctest ():
	import doctest
	doctest.testmod ()


### MAIN ###

if __name__ == '__main__':
	_doctest()


### END ######################################################################
