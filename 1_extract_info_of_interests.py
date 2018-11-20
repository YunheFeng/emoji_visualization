'''
This file extracts the tweet json information of interests
'''

import json
import re				

# collected data files 
f_data = 'TweetsChampions.json'
output_file_name = 'tweets_of_interests'

# read and process tweets 
with open(f_data) as f:
	for line in f:
		try:
			dict_tweet = json.loads(line)
				
			# get tweet text 
			if ('text' in dict_tweet):
				tweet_text = dict_tweet['text']
				tweet_text = re.sub(r'\n', ' ', tweet_text)
				tweet_text = re.sub(r'\r', ' ', tweet_text)
			else: 
				tweet_text = 'None'	
				
			# append new line symbol
			tweet_text = tweet_text + '\n'
			
			# encoding in utf-8
			tweet_text = tweet_text.encode('utf-8')
			with open(output_file_name + '.csv', 'ab') as f:
				f.write(tweet_text)
		except:
			continue
			