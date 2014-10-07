#!/usr/bin/env python

import urllib
import regex as re
import pymongo
import argparse
import pprint
from math import log
from os import listdir
import sys
from time import localtime
from collections import Counter
import json

to_print = 0
synsets_filename = '../1000_synsets.txt'
#synsets_filename = '10_synsets.txt'

datadir = '../data/dataset/'
#parser = argparse.ArgumentParser()
#parser.add_argument("datafile")
#args = parser.parse_args()
#datafile = args.datafile
#datafile = '../data/testsample.dat'

def myprint(a='', b=''):
	if to_print:
		print a, b

# return: dict { phrase: set of ids }
def synsetPhraseIds(synsets_filename):
	synsets = {}
	with open(synsets_filename) as f:
		for line in f:
			items = line.lower().split()
			sid = items[0] # id
			phrases = items[1:]
			for phrase in phrases:
				# each phrase can be in multiple synsets
				# add id of synset to the set of ids corresponding to this phrase
				synsets[phrase] = synsets.setdefault(phrase, set()) | set([sid])
	return synsets

# return: dict { id: phrases }
def synsetIdPhrases(synsets_filename):
    synsets = {}
    with open(synsets_filename) as f:
        for line in f:
			items = line.lower().split()
			sid = items[0] # id
			phrases = set(items[1:])
			synsets[sid] = phrases
    return synsets

def regex(synsets):
	r = ''
	for sid in synsets:
		phrases = [ re.sub('_', 's+', re.escape(phrase)) for phrase in synsets[sid] ]
		r += r'(?P<s' + sid + r'>\b(' + '|'.join(phrases) + r')\b)|'
	#print r
	return r[:-1]

# items: 4 strings - title, description, user tags, machine tags
# rephrases: regex to search in items
# return: dict {phrase: count} for given image
def synsetFreqForImg(items, rephrases):
	# decode from url encoding and convert to lower case
	items = [ urllib.unquote_plus(item).lower() for item in items ]

	# join free text to tags as another phrase
	text = ','.join(items)
	myprint('text: ', text)
	#phrases = text.split(',')
	#for phrase in phrases:
		#words = phrase.split() # remove whitespaces
		#if words: # not empty
			#phrase = ' ' + '  '.join(words) + ' '
			#searched_text += phrase + ','
	#myprint('searched text: ', searched_text)

	# search for phrases
	#for phrase in re.findall(rephrases, text): # re.I?
		#phrase = match.group()
	#	phrase = re.sub(r'\s+', '_', phrase)
	#	myprint('phrase: ', phrase)

	synsets = [match.lastgroup for match in rephrases.finditer(text)]
	if not synsets: return {}
	syn_freq = Counter(synsets)
	#syn_freq = Counter()
	#global total_syn_freq
	#total_syn_freq += syn_freq
	syn_freq = { k[1:]: v for k,v in syn_freq.iteritems() }
	return syn_freq

def processLine(line, filename):
	items = line.split('\t')
	# filter videos
	if items[22][0] == '1': # items[22][1] == '\n'
		return 
	# all empty
	if all(item == '' for item in items[6:10]):
		return
	myprint('id: ', items[0])
	'''
	# get phrases for image
	phrases_count = phrasesCount(items[6:10], rephrases)
	if not phrases_count: # empty
		return
	myprint('phrases: ', phrases_count)

	# get synsets frequencies for img
	syn_freq = {}
	for phrase in phrases_count:
		sids = synsets[phrase]
		for sid in sids:
			syn_freq[sid] = syn_freq.setdefault(sid, 0) + phrases_count[phrase]
	'''
	iid = items[0]
	#url = items[14]
	syn_freq = synsetFreqForImg(items[6:10], rephrases)
	if not syn_freq: 
		return
	#images[iid] = {syn_freq, url}
	images.append( {'id': iid, 'syn_freq': syn_freq} )
	#myprint('synsets: ', img_syn_freq[iid])

	# number of images for each synset
	for sid in syn_freq:
		imgcount, freq = synsets.setdefault(sid, [0,0])
		synsets[sid] = [ imgcount + 1, freq + syn_freq[sid] ]

	urls[iid] = items[14]
	myprint()

	# log
	global n_processed_img
	n_processed_img += 1
	if n_processed_img % 1000 == 0:
		info = 'file number: {}, count: {}'.format(filename[-1], n_processed_img)
		print info

'''
        status = 'file: %s, count: %d, id: %s' % (datafile, count, imgid)
        try:
            db.images.insert( {'_id': iid, 'url': url, 'synsets': list(sids)} ) # 'relevance': 0
            for sid in sids:
                db.synsets.update( {'_id': sid}, {'$inc': {'n_img': 1}}, upsert=True )
            status += ', processed'
        except pymongo.errors.DuplicateKeyError:
            status += ', skipped'
        print status
'''

def processFile(filename):
	#print datadir+filename
	with open(filename) as f:
		for line in f:
			processLine(line, filename)

# main

#synsets = synsetPhraseIds(synsets_filename)
synsets_def = synsetIdPhrases(synsets_filename)
rephrases = re.compile(regex(synsets_def))
#rephrases = ''

n_processed_img = 0
images = []
synsets = {}
urls = {}
#total_syn_freq = Counter()

try:
	processFile(sys.argv[1])
except IndexError: 
	print 'no parameter'
#try:
#	processFile(datafile)
#except NameError: print 'datafile not defined'
#try:
	for filename in listdir(datadir):
		#print filename
		processFile(datadir+filename)
#except NameError: print 'datadir not defined'

#print 'image: {synset: freqency}'
#pprint.pprint(img_syn_freq)
#pprint.pprint(syn_imgcount)
#pprint.pprint(total_syn_freq)

n = sys.argv[1][-1] # number of datafile
outdir = '../output/'

#f = open(outdir + 'images' + n, 'w')
with open(outdir + 'images' + n, 'w') as f:
	json.dump(images, f, indent=1)

synsets_json = [ {'id': sid, 'img_count': imgcount, 'freq': freq} for sid, [imgcount, freq] in synsets.items() ]
with open(outdir + 'synsets' + n, 'w') as f:
	json.dump(synsets_json, f, indent=1)
'''
print 'Calculating relevance ...'

n_imgs = (float)(len(images))
relevance = {}
relevance = []
for img in images:
	syn_freq = img['syn_freq']
	rel = 0
	for sid in syn_freq:
		rel += syn_freq[sid] * log( n_imgs / synsets[sid][0] )
		#print sid, syn_freq[sid], log( n_imgs / syn_imgcount[sid]), rel
		#relevance[iid] = relevance.setdefault(iid, 0) + rel
	#images.append( {'_id': iid, 'relevance': relevance[iid], 'url': urls[iid]} ) 
	relevance.append( {'id': img['id'], 'relevance': rel, 'url': urls[img['id']]} ) 

with open(outdir + 'relevance' + n, 'w') as f:
	json.dump(relevance, f, indent=1)
'''
#with open(outdir + 'relevance' + n, 'r') as f:
#	o = json.load(f)
#	pprint.pprint(o)


'''
print 'inserting to db ...'

#db = pymongo.MongoClient().test1
db = pymongo.MongoClient().test2
#db = pymongo.MongoClient().test # real data
db.images.insert(images)

print time() + ': data inserted to db'
'''
