#!/usr/bin/env python

import pprint

synset_ids_filename = '../synset_ids.txt'
synset_defs_filename = '../synset_defs.txt'

# return: dictionary { phrase: set of ids }
def createSynsets(ids_filename, defs_filename):
	nsynsets = 1000
	synsets = {}
	# get list of relevant ids
	with open(ids_filename) as f:
		validids = set( line[1:].strip() for line in f.readlines()[:nsynsets] ) #[1:] because of 'n' at the beginning of id
	# get keywords for given ids
	with open(defs_filename) as f:
		for line in f:
			items = line.lower().split() 
			sid = items[0] # id
			if sid in validids:
				print line[:-1]
				phrases = items[1:]
				for phrase in phrases:
					# each phrase can be in multiple synsets
					# add id of synset to the set of ids corresponding to this phrase
					synsets[phrase] = synsets.setdefault(phrase, set()) | set([sid])
	return synsets

synsets = createSynsets(synset_ids_filename, synset_defs_filename)
#pprint.pprint(synsets)
