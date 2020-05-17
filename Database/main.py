#!/usr/bin/env python
# coding: utf-8

# In[1]:


# This is Main function.
# Extracting streaming data from Twitter, pre-processing, and loading into MySQL
import credentials # Import api/access_token keys from credentials.py
import settings # Import related setting constants from pogdb.py 

import re
import tweepy
from textblob import TextBlob


# In[2]:


# Import api/access_token keys from credentials.py
import credentials
auth  = tweepy.OAuthHandler(credentials.API_KEY,                             credentials.API_SECRET_KEY)
auth.set_access_token(credentials.ACCESS_TOKEN,                        credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


# In[3]:


#The fuctions are used to clean the tweets
def clean_tweet(self, tweet): 
    ''' 
    Use sumple regex statemnents to clean tweet text by removing links and special characters
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])                                 |(\w+:\/\/\S+)", " ", tweet).split()) 
def deEmojify(text):
    '''
    Strip all non-ASCII characters to remove emoji characters
    '''
    if text:
        return text.encode('ascii', 'ignore').decode('ascii')
    else:
        return None


# In[4]:


#This connnects to the database, checks if a table {"Tablename"} exits, if not creates one and closes the connection
import os
import psycopg2

dbconn = psycopg2.connect("host=ec2-54-81-37-115.compute-1.amazonaws.com dbname=d58g5m66umb113 user=eigxqdhsrlaffv password=b1495696080d3ad38656b3e2973e25cd8890a1570a7639abdf756cbbd793c8f1")
if dbconn:
    print("Connected")
    '''
    Check if this table exits. If not, then create a new one.
    '''
    mycursor = dbconn.cursor()
    """mycursor.execute(
    SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '{0}'.format(settings.TABLE_NAME))
    print("table exists")
    if mycursor.fetchone()[0] != 1:"""
    mycursor.execute("CREATE TABLE {} ({})".format(settings.TABLE_NAME, settings.TABLE_ATTRIBUTES))
    print("Table does not exist so it has been created")
    dbconn.commit()
    mycursor.close()
else:
    print('Not connected')


# In[6]:


#creating a listener to watch for our data
#has two functions
#on_status it to check for tweets
#on_error is to stop tweet checking incase a limit is reached
class MyStreamListener(tweepy.StreamListener):
    '''
    Tweets are known as “status updates”. So the Status class in tweepy has properties describing the tweet.
    https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.html
    '''
    
    def on_status(self, status):
        '''
        Extract info from tweets
        '''
        
        if status.retweeted:
            # Avoid retweeted info, and only original tweets will be received
            return True
        # Extract attributes from each tweet
        id_str = status.id_str
        created_at = status.created_at
        text = deEmojify(status.text)    # Pre-processing the text  
        sentiment = TextBlob(text).sentiment
        polarity = sentiment.polarity
        subjectivity = sentiment.subjectivity
        
        user_created_at = status.user.created_at
        user_location = deEmojify(status.user.location)
        user_description = deEmojify(status.user.description)
        user_followers_count =status.user.followers_count
        longitude = None
        latitude = None
        if status.coordinates:
            longitude = status.coordinates['coordinates'][0]
            latitude = status.coordinates['coordinates'][1]
            print(longitude)
            print(latitude)
        retweet_count = status.retweet_count
        favorite_count = status.favorite_count
        
        print(status.text)
        print("Long: {}, Lati: {}".format(longitude, latitude))
        
        # Store all data in MySQL
        if dbconn:
            mycursor = dbconn.cursor()
            sql = "INSERT INTO {} (id_str,created_at,text,polarity,                subjectivity, user_created_at, user_location,                user_description, user_followers_count, longitude,                latitude, retweet_count, favorite_count) VALUES                 (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(settings.TABLE_NAME)
            val = (id_str, created_at, text, polarity, subjectivity,                 user_created_at, user_location, user_description, user_followers_count, longitude, latitude, retweet_count, favorite_count)
            mycursor.execute(sql, val)
            dbconn.commit()
            mycursor.close()
    
    
    def on_error(self, status_code):
        '''
        Since Twitter API has rate limits, stop srcraping data as it exceed to the thresold.
        '''
        if status_code == 420:
            # return False to disconnect the stream
            return False


# In[ ]:


#This calls the class myStreamListener thereby witing into the database
'''places = api.search(query="Nairobi", granularity="city")
place_id = places[0].id
public_tweets = api.search(q="place:%s" %place_id)
'''
GEOBOX_WORLD = [-180,-90,180,90]
GEOBOX_NAIROBI = [-1.1597918307560573,36.665974517587834,-1.3891756881977984,37.106463945682584]
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)
myStream.filter(locations=GEOBOX_NAIROBI)
                            
# Close the postgres connection as it finished
# However, this won't be reached as the stream listener won't stop automatically
# Press STOP button to finish the process.
dbconn.close()


# In[ ]:





# In[ ]:


#Fetch data from database


# In[ ]:


#This is used to read data from the database
import psycopg2
try:
    connection = psycopg2.connect(user="eigxqdhsrlaffv",
                                  password="b1495696080d3ad38656b3e2973e25cd8890a1570a7639abdf756cbbd793c8f1",
                                  host="ec2-54-81-37-115.compute-1.amazonaws.com",
                                  database="d58g5m66umb113")
    cursor = connection.cursor()
    postgreSQL_select_Query = "select * from nairobitweets"

    cursor.execute(postgreSQL_select_Query)
    print("Selecting rows from tweets table using cursor.fetchall")
    tweet_records = cursor.fetchall() 
   
    print("Print each row and it's columns values")
    for row in tweet_records:
        print("Id = ", row[0], )
        print("created_at = ", row[1], )
        print("text  = ", row[2], )
        print("polarity = ", row[3], )
        print("subjectivity = ", row[4], "\n")

except (Exception, psycopg2.Error) as error :
    print ("Error while fetching data from PostgreSQL", error)

finally:
    #closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed").close()


# In[ ]:


#\copy (SELECT * FROM tweets) to 'C:\tmp\persons_client.csv' with csv

