# importing packages for twitter
import json
import pandas as pd
import matplotlib.pyplot as plt
from twitter import *

# Import flask modules
from flask import render_template, request, send_from_directory, jsonify
from flask import Flask

app = Flask(__name__,
		static_url_path='', 
        static_folder='static',
        template_folder='templates')

# Calling Twitter API
t = Twitter(auth=OAuth('4659614468-aTNttzrV0J5eEjvpFLxkwl0PzLCmv5Of0VD6B17', 'hUXXqB5RefF7hPV6x46meXnkq81tf82T2C8EzBpKZjpoh', 'joBl9cFZMOIlG3jsMzTfLNiFG','TMjMiLnmtU9ZAl5QBYT4nULIoIVOgmQaQg5mhZH8uQnMpKWZlw'))


@app.route('/')
def index():
	# Get the tweets
	tweets_frame,tweets_dict=tweets_frame_fun("Happy")
	tweet_words_count=tweets_word_counts_func(tweets_frame)
	return render_template('index.html',tweets_frame=tweets_dict,tweet_words_count=tweet_words_count)

# return tweets
def tweets_frame_fun(word):
	results=t.search.tweets(q=word,count=100)
	resultFrame = pd.DataFrame(columns=["username","created_at","tweet"])
	for i in range(len(results['statuses'])):
		resultFrame.loc[i, "username"] = results['statuses'][i]['user']['screen_name']
		resultFrame.loc[i, "created_at"] = results['statuses'][i]['created_at']
		resultFrame.loc[i, "tweet"] = results['statuses'][i]['text']
	
	resultFrame["#"]=resultFrame.index+1
	tweets=resultFrame[['tweet','#']]
	tweets_dict=tweets.set_index('#')['tweet'].to_dict()

	return resultFrame,tweets_dict

# return word count in tweets
def tweets_word_counts_func(tweets_frame):
	def word_count(str,count):
	    words = str.split()

	    for word in words:
	        if word in counts:
	            counts[word] += 1
	        else:
	            counts[word] = 1
	    return counts
	counts = dict()
	for i in tweets_frame['tweet']:
	    counts=word_count(i,counts)
	tweet_words_count = sorted(counts.items(), key=lambda counts: counts[1])
	tweet_words_count.reverse()
	tweet_words_count=dict(tweet_words_count[0:10])
	return tweet_words_count

@app.route("/getData")
def getData():

    entry2Value = request.args.get('entry2_id')
    entry1Value = request.args.get('entry1_id')

    var1 = int(entry2Value) + int(entry1Value)
    var2 = 10
    var3 = 15
    tweets_frame,tweets_dict=tweets_frame_fun("MSFT")
    tweet_words_count=tweets_word_counts_func(tweets_frame)
    print("hello")
    return render_template('update_data.html',tweets_frame=tweets_dict,tweet_words_count=tweet_words_count)
	#return jsonify({ 'tweets_frame':tweets_dict,'tweet_words_count':tweet_words_count})

if __name__ == '__main__':
    app.run(debug=True)



