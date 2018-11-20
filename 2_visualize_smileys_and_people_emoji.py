import re
import sys
sys.path.insert(0,'./utils/')
from visualize_specific_emojis_using_html import *
from read_unicode_of_face_emojis import *
from calculate_number_of_face_emojis import *

data_name = 'tweets_of_interests.csv'

# extract unique tweets and their tweeting time 
list_all_tweet = []
with open (data_name, 'rb') as f:
	for line in f:
		line = str(line)
		# extract tweet
		tweet = line.strip()[2:-3] # delete 'b and \n'
		list_all_tweet.append(tweet)

# get unique tweets
list_unique_tmp = list(set(list_all_tweet))

# remove meaningless characters, like RT @xxxxxxxx:
list_unique_tweet = list(set([re.sub(r'\ART @.+: ', '', tweet) for tweet in list_unique_tmp]))
list_unique_tweet = [tweet for tweet in list_unique_tweet if tweet != '']

# extract unicodes of face emojis
f_face = ['face_negative', 'face_neutral', 'face_positive']
f_utf_8_to_unicode = './data/utf_8_to_unicode_table.txt'
f_emoji_ccs = './data/emoji.json'

dict_face = read_unicode_of_face_emojis(f_face) # with key: face type, value: a list of the unicodes of faces
visualize_specific_emojis_using_html(list_unique_tweet, dict_face, f_utf_8_to_unicode, f_emoji_ccs)

top_num = 5
fig_name = 'face_emoji_count_dist'
dict_face_count = calculate_number_of_face_emojis(list_unique_tweet, dict_face, f_utf_8_to_unicode, f_emoji_ccs, top_num, fig_name)

