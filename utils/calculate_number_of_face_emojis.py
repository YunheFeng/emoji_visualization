import sys
# sys.path.insert(0,'../utils/') 
# from extract_raw_emoji_and_time import *

import re
import json
import matplotlib.pyplot as plt
import operator
import numpy as np
import os	
	
def calculate_number_of_face_emojis(list_unique_tweet, dict_face, f_utf_8_to_unicode, f_emoji_ccs, top_num, fig_name):
	'''
	list_unique_tweet: the list of unique tweets
	dict_face: with key: face type, e.g. positive and negative, value: a list of the unicodes of faces
	f_utf_8_to_unicode: the file containing the mapping from utf-8 to unicode
	f_emoji_ccs: the ccs file to show emojis in a browser
	top_num: the top k emojis that we care
	fig_name: the name of saved figures, html files and other possible files
	return: dict_face_count with key: the face emoji unicode, value: the count
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

	# extract expected emoji text from tweets
	dict_emoji_expected = {} # key: the index of the tweet, value: the extracted expected emoji in the tweet
	for index, tweet in enumerate(list_unique_tweet):
		# extract emoji and feed a fake time
		# emoji, time = extract_raw_emoji_and_time(tweet, ' ')
		# fake one function 
		emoji = 'ok'
		# the emoji is valid 
		if (emoji != 'none'):
			dict_emoji_expected[index] = emoji
		else:
			dict_emoji_expected[index] = ' '

	emoji_ccs = json.load(open(f_emoji_ccs))
	dict_unicode_to_name = {}
	for e in emoji_ccs:
		unicodes = e['file']
		name = e['name']	
		dict_unicode_to_name[unicodes] = name 

	# calculate the number of different face emojis
	dict_face_count = {} # key: the face emoji unicode, value: the count
	dict_face_type = {} # key: the face emoji type, e.g., positive and negative, value: a new dictionary with key: emoji unicode, value: the count
	for i in dict_emoji_utf_8:
		# only process those emojis that can be found in tweets 
		if (dict_emoji_expected[i] != ' '):
			# only process the face emojis of interest
			for unicode_ in dict_emoji_utf_8[i]:
				for face_type in dict_face:
					if (unicode_ in dict_face[face_type]):
						# initialize dict_face_type 
						if (face_type not in dict_face_type):
							dict_face_type[face_type] = {}
						if (unicode_ not in dict_face_type[face_type]):
							dict_face_type[face_type][unicode_] = 1
						else: 
							dict_face_type[face_type][unicode_] += 1
						# process the overall face emoji count	
						if (unicode_ not in dict_face_count):
							dict_face_count[unicode_] = 1
						else:
							dict_face_count[unicode_] += 1
	
	
	# create html file to show emojis
	html_begin = '<!DOCTYPE html>\n<html>\n<link href="https://afeld.github.io/emoji-css/emoji.css" rel="stylesheet">\n<body>\n\n'
	html_end = '</body>\n</html>\n'	
	f_emoji_html = fig_name + '.html'
	# sort the dict_face_count
	tuple_face_count = sorted(dict_face_count.items(), key=operator.itemgetter(1), reverse=True)
	unicode_, max_count = tuple_face_count[0]
	with open(f_emoji_html, 'w') as f:
		f.write(html_begin)
		for (unicode_, count) in tuple_face_count:
			f.write('<i class="em em-' + dict_unicode_to_name[unicode_] + '"></i>')
			f.write(' | ' + str((len(str(max_count))-len(str(count)))*'0') + str(count) + ' ')
			# f.write('<p>')
		f.write(html_end)
		
							
	# create latex table file to show emojis
	c_l = ''
	for i in range(top_num):
		c_l += 'c|'
	latex_begin = '\\begin{table*}[h] \n \\centering \n \\caption{Emojis Visualization} \n \\label{my-label} \n  \\scalebox{0.9}{ \n \\begin{tabular}{|l|' + c_l + '} \n \\hline Emoji Type & \\multicolumn{5}{c|}{Emoji Percentage} \\\\ \\hline\n'
	latex_end = '\\end{tabular}} \n \\end{table*}'	
	f_emoji_latex = fig_name + '.latex'
	with open(f_emoji_latex, 'w') as f:
		f.write(latex_begin)
		for face_type in dict_face_type:
			# sort the elements in dict_face_type
			tuple_face_count = sorted(dict_face_type[face_type].items(), key=operator.itemgetter(1), reverse=True)
			f.write(face_type.split('_')[1].title())
			top_k = 0
			for (unicode_, count) in tuple_face_count:
				top_k += 1
				if (top_k > top_num):
					break
				f.write(' & ' + '\\includegraphics[width=0.07\\linewidth]{figures/emoji_image/' + unicode_ + '.png}' + '' + str(count))
			f.write(' \\\\ \\hline \n')
		f.write(latex_end)
		
		top_num
			



	
	return dict_face_count
