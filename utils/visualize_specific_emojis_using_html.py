import sys
# sys.path.insert(0,'../utils/') 
# from extract_raw_emoji_and_time import *

import re
import json

def visualize_specific_emojis_using_html(list_unique_tweet, dict_face, f_utf_8_to_unicode, f_emoji_ccs):
	'''
	list_unique_tweet: the list of unique tweets
	dict_face: with key: face type, e.g. positive and negative, value: a list of the unicodes of faces
	f_utf_8_to_unicode: the file containing the mapping from utf-8 to unicode
	f_emoji_ccs: the ccs file to show emojis in a browser
	return: generate a html file which contains the visualized emojis, the expected emojis and the original tweets
	'''
	# read utf_8_to_unicode_table
	dict_utf_8_to_unicode = {} # key: utf-8, value: unicode 
	with open(f_utf_8_to_unicode) as f:
		for line in f:
			utf_8_code = line.split(',')[0].lower()
			unicode_code = line.split(',')[1].strip()
			# delete the ending blank
			utf_8_code = utf_8_code[:-1]
			# convert into \x0F format
			utf_8_code = '\\x' + re.sub(' ', '\\x', utf_8_code) + ' '
			# insert into dictionary
			dict_utf_8_to_unicode[utf_8_code] = unicode_code
			
	dict_emoji_utf_8 = {} # key: the index of the tweet, value: a list of unicode of emojis
	for index, tweet in enumerate(list_unique_tweet):
		# extract all \x0F...... format substrings
		list_emoji_utf_8 = re.findall(r'\\x\S+\s', tweet)
		for e in list_emoji_utf_8:
			if (e in dict_utf_8_to_unicode):
				if (index not in dict_emoji_utf_8):
					dict_emoji_utf_8[index] = []
				dict_emoji_utf_8[index].append(dict_utf_8_to_unicode[e])

	emoji_ccs = json.load(open(f_emoji_ccs))
	dict_unicode_to_name = {}
	for e in emoji_ccs:
		unicodes = e['file']
		name = e['name']	
		dict_unicode_to_name[unicodes] = name 

	# create html file to show emojis
	html_begin = '<!DOCTYPE html>\n<html>\n<link href="https://afeld.github.io/emoji-css/emoji.css" rel="stylesheet">\n<body>\n\n'
	html_end = '</body>\n</html>\n'	
	for face_type in dict_face:
		list_emoji_unicode = dict_face[face_type]
		f_emoji_html = face_type + '.html'
		with open(f_emoji_html, 'w') as f:
			f.write(html_begin)
			for i in dict_emoji_utf_8:
				# only process the face emojis of interest
				flag = False
				for unicode_ in dict_emoji_utf_8[i]:
					if (unicode_ in list_emoji_unicode):
						flag = True
						break
				if (flag == True):
					for unicode_ in dict_emoji_utf_8[i]:
						f.write('<i class="em em-' + dict_unicode_to_name[unicode_] + '"></i>')
						f.write(' | ' + unicode_)
					f.write(' | ' + list_unique_tweet[i])
				f.write('<p>')
			f.write(html_end)
