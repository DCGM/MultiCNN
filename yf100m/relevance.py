#!/usr/bin/env python

import urllib
import sys
from math import log
import json
import pprint
from os import listdir
import os

datadir = '../data/dataset/'
outdir = '../output/'
download_dir = '../downloads_test/'

'''
with open(outdir + 'images0') as f:
		images += json.load(f)
with open(outdir + 'synsets0') as f:
		for syn in json.load(f):
			imgcount, freq = synsets.setdefault(syn['id'], [0,0])
			synsets[syn['id']] = [ imgcount + syn['img_count'], freq + syn['freq'] ]
#with open(outdir + 'urls0') as f:
#		for img in json.load(f):
#			urls[img['id']] = img['url']
'''
def loadImgSynFreqs():
	img_syn_freqs = []
	for i in range(10):
		with open(outdir + 'img_syn_freqs' + str(i)) as f:
			img_syn_freqs += json.load(f)
	return img_syn_freqs

def countSynsets():
	synsets = {}
	for i in range(10):
		with open(outdir + 'synsets' + str(i)) as f:
			for syn in json.load(f):
				#imgcount, freq = synsets.setdefault(syn['id'], [0,0])
				actual = synsets.setdefault(syn['id'], {'img_count': 0, 'freq': 0})
				imgcount = actual['img_count'] + syn['img_count']
				freq = actual['freq'] + syn['freq']
				synsets[syn['id']] = {'img_count': imgcount, 'freq': freq}
				#synsets[syn['id']] = [ imgcount + syn['img_count'], freq + syn['freq'] ]
	return synsets

def toDict(img_syn_freqs):
	adict = {}
	for img in img_syn_freqs:
		adict[img['id']] = img['syn_freq']
	return adict	
'''
def getImgSynsets():
	img_synsets = {}
	for n in range(10):
		with open(outdir + 'images' + str(n)) as f:
			for img in json.load(f):
				img_synsets[img['id']] = img['syn_freq']
	return img_synsets
'''
def getUrls():
	urls = {}
	for n in range(10):
		with open(outdir + 'urls' + str(n)) as f:
			for img in json.load(f):
				urls[img['id']] = img['url']
	return urls

def getPages():
	pages = {}
	for fn in os.listdir(datadir):
		with open(datadir + fn) as f:
			for line in f:
				items = line.split('\t')
				# filter videos
				if items[22][0] == '1': continue # items[22][1] == '\n'
				# all empty
				if all(item == '' for item in items[6:10]): continue
				iid = items[0]
				pages[iid] = items[13]
	return pages

#with open(outdir + 'pages', 'w') as f:
#	json.dump(pages, f, indent=1)

def relevance(images, synsets):
	n_imgs = (float)(len(images))
	relevance = {}

	for img in images:
		rel = 0
		for sid in img['syn_freq']:
			rel += img['syn_freq'][sid] * log( n_imgs / synsets[sid]['img_count'] )
		relevance[img['id']] = rel
		#relevance.append( {'id': img['id'], 'relevance': rel} )
	return relevance

# write images data
def writeImages():
	images = []
	img_syn_freqs = toDict(loadImgSynFreqs())
	synsets = countSynsets()
	relevance = relevance(img_syn_freqs, synsets)

	for iid in relevance:
		images.append( {'id': iid, 'relevance': relevance[iid]} ) #TODO

'''
def relevance(fn='images'):
	print 'Calculating relevance ...'
	n_imgs = (float)(len(images))
	images_rel = []

	for img in images:
		rel = 0
		for sid in img['syn_freq']:
			rel += img['syn_freq'][sid] * log( n_imgs / synsets[sid][0] )
		images_rel.append( {'id': img['id'], 'relevance': rel} )
    	#images_rel.append( {'id': img['id'], 'relevance': rel, 'url': urls[img['id']]} ) 

	print 'Sorting ...'
	images_sort = sorted(images_rel, key=lambda k: k['relevance'], reverse=True)

	with open(outdir + fn, 'w') as f:
		json.dump(images_sort, f, indent=1)
'''
#relevance('images_sort')

# Export synsets to json

# return: dict { id: def }
def synsetDefs():
    synsets = {}
    with open('../1000_synsets.txt') as f:
        for line in f:
            sid, sdef = line.lower().split(' ',1)
            synsets[sid] = sdef.strip()
    return synsets

#TODO exportJson()
def synsetDetails(fn='synsets.js'):
	syn_defs = synsetDefs()
	syn_list = [ {'id': sid, 'img_count': imgcount, 'freq': freq} for sid, [imgcount, freq] in synsets.items() ]
	syn_sort = sorted(syn_list, key=lambda k: k['img_count'], reverse=True)
	syn_details = []

	for n in range(50):
		sid = syn_sort[n]['id']
		syn_details.append( {'id': int(sid), 'words': syn_defs[sid].split(), 'count': syn_sort[n]['img_count']} )

	with open(outdir + fn, 'w') as f:
		f.write('var synsets = ' + json.dumps(syn_details, indent=1))

#synsetDetails()

# Create html page with images

def html(fn='images.html'):
	with open(outdir + 'relevance_sample100') as f:
		relevance = json.load(f)
	#with open(outdir + 'pages') as f:
	#	pages = json.load(f)
	urls = getUrls()
	img_synsets = getImgSynsets()
	syn_defs = synsetDefs()
	pages = getPages()
	html = '<html><body><table>'

	for i in range(50):
		iid = relevance[i]['id']
		html += '<tr><td><img src="{}"></td>'.format(urls[iid])
		html += '<td> {}.<br> <b>Relevance</b>: {}<br> <b>Synsets</b>: '.format(i+1, relevance[i]['relevance'])
		for sid in img_synsets[iid]:
			html += '{} | '.format(syn_defs[sid])
		html += '<br> <b>Page</b>: <a href="{}">{}</a><br> <b>ID</b>: {} </td></tr>'.format(pages[iid], pages[iid], iid)

	html += '</table></body></html>'

	with open(outdir + fn, 'w') as f:
		f.write(html)

#html()

# Download n most relevant images

def download(n):
	print 'Downloading ...' 
	count = -1
	for img in db.images.find( {}, {'url': 1} ).sort('relevance', -1).limit(n):  # return only url and id (default)
		count += 1
		#if count % threadNum != threadId: continue
		filename = download_dir + img['_id'] + '.jpg'
		urllib.urlretrieve(img['url'], filename)
		print count
	print 'done download'

#threadNum = int(sys.argv[1])
#threadId = int(sys.argv[2])
#print threadNum, threadId
#download(5)


'''
def updateRelevance():
	db.images.update( {}, {'$set': {'relevance': 0}}, multi=True )
	n_img_total = (float)(db.images.find().count())
	syn_relevance = {}

	for synset in db.synsets.find():
		relevance = log( n_img_total / synset['n_img'] )
		syn_relevance[synset['_id']] = relevance

	for img in db.images.find():
		img_relevance = 0
		for sid in img['synsets']:
			img_relevance += syn_relevance[sid]
		db.images.update( {'_id': img['_id']}, {'$set': {'relevance': img_relevance}} )

	print 'done relevance update'

updateRelevance()
'''

