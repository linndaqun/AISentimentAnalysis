# Import libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
import nltk 
from nltk.corpus import stopwords
import string
import re
import emoji
from nltk.stem.snowball import SnowballStemmer
import tweepy
import botometer
import csv
import pandas as pd
pd.set_option('display.max_colwidth', 100)

#FOR THE BOTOMETER
rapidapi_key = "3e780f0aa5msh2c957bc129c5c4fp1e42aajsn52ac7cb58a9d" # now it's called rapidapi key
OAUTH_KEYS = {'consumer_key':'BWDvPWSmrJ18xEBTPbTkxiGm9', 'consumer_secret':'FodmJZP8RPjdG5ZJ0dz6xpNEjOFYG5LnFTjvmKKze8e0GmAO8b',
    'access_token_key':'769205140645642240-pFoG4e2EpEQft63BjruaLmLvuehRQDx', 'access_token_secret':'NvpPKD8xZKd14NxmuzONg2rAApMjYkJK5wmkyE1UGgBOk'}

bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **OAUTH_KEYS)

def remove_emoji(text):
    """Converts emojis to words
    """
    #text  = "".join([char for char in text if char in emoji.UNICODE_EMOJI])
    text = emoji.demojize(text)
    return text

def tokenization(text):
    text = re.split('\W+', text)
    return text

def remove_stopwords(text):
    """Removes stopwords
    Makes sure to tokenize / put all words in list
    """
    stop_words = set(stopwords.words("english"))
    text = tokenization(text)
    filtered_tweet = [w for w in text if not w in stop_words] 
    return filtered_tweet

def stemming(text):
    """Assumes that text has already been tokenized
    """
    sb = SnowballStemmer("english")
    for word in text:
        print(word, " : ", sb.stem(word)) 

def remove_url(text):
    pattern = r"http\S+"
    #text = "https://www.google.com"
    text = re.sub(pattern, "",text)
    pattern2 = r"www\S+"
    return re.sub(pattern2, "",text)

def remove_hashtag(text):
    pattern = r"#\S+"
    return re.sub(pattern, "",text)

def remove_username(text):
    pattern = r"@\S+"
    return re.sub(pattern, "",text)

def checkBot(author):
    """Input can be @username or author ID
    """
    #try:
    currID = author
    result = bom.check_account(currID)
    check = result['scores']
    if check['english'] > 0.55:
        return 1 #is a Bot
    else:
        return 0
    #except tweepy.error.TweepError:
        #pass


tweet_df = pd.read_csv("output_got.csv")
df  = pd.DataFrame(tweet_df[['id', 'text']])
df['text'] = df['text'].apply(lambda x: remove_emoji(x))
df['text'] = df['text'].apply(lambda x: remove_hashtag(x))
df['text'] = df['text'].apply(lambda x: remove_url(x))
df['text'] = df['text'].apply(lambda x: remove_username(x))
df['bot?'] = df['id'].apply(lambda x: checkBot(x))
#df['text_nostop'] = df['text_noEmoji'].apply(lambda x: remove_stopwords(x))
print(df.head(10))
df.to_csv("output_got.csv")


 


tweet="Testing🤠 Sarah's @what cradle loves pizza and cats but she doesn't herself. #lol https://google.com www.cya.com"
tweet = remove_emoji(tweet)
tweet = remove_url(tweet)
tweet = remove_hashtag(tweet)
tweet = remove_username(tweet)
print(tweet)
print(tokenization(tweet))
tweet = remove_stopwords(tweet)
print(stemming(tweet))
