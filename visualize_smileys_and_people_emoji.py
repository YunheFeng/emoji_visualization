import re
import sys
sys.path.insert(0,'./utils/')
from visualize_specific_emojis_using_html import visualize_specific_emojis_using_html
from read_unicode_of_face_emojis import read_unicode_of_face_emojis
from calculate_number_of_face_emojis import calculate_number_of_face_emojis

data_file = 'tweets_sample.txt'

# read data
list_tweets = []
with open (data_file, 'rb') as f:
	for line in f:
		line = str(line)
		list_tweets.append(line)

# extract unicodes of face emojis
f_face = ['face_negative', 'face_neutral', 'face_positive']
dict_face = read_unicode_of_face_emojis(f_face) # with key: face type, value: a list of unicodes of faces

# visualize smileys and people emojis
f_utf_8_to_unicode = './data/utf_8_to_unicode_table.txt'
f_emoji_ccs = './data/emoji.json'
visualize_specific_emojis_using_html(list_tweets, dict_face, f_utf_8_to_unicode, f_emoji_ccs)

# calculate and visualize face emojis
top_num = 5
fig_name = 'face_emoji_count_dist'
dict_face_count = calculate_number_of_face_emojis(list_tweets, dict_face, f_utf_8_to_unicode, f_emoji_ccs, top_num, fig_name)

