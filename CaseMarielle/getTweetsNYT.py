
# coding: utf-8

# In[1]:


# -*- coding: utf-8 -*-
"""
Created on Sep 11 2018

@author: Fernanda Farinelli
"""


# In[2]:


consumer_key = 'L4YzGvvrTHOJ0g84Ve1vPdlZw'
consumer_secret = 'JhK5F7L2hDx1Bnr0Er8tpzdYPd7HhBvBRSZGGdFUVsxyrTanrm'
access_token_key = '1028301224519589889-QmX9vmaGqEtQmz2brG3VEEf60VxE3S'
access_token_secret = 'eI7YQKC2YAzPASwQBJCrzz0Egvy3Q0VPVzEdp9Klua9VD'
account_monitor = 'nytimes'
folderOutput = 'C:\\Users\\unesp\\ProjetoOpLaDyn\\outputs\\'


# In[3]:


import tweepy #https://github.com/tweepy/tweepy
import csv
import json
import time


# In[4]:


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token_key, access_token_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	#new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)    
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print ("getting tweets before %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		#new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)        
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		#print("type alltweets",type(alltweets))
		#print("type new_tweets",type(new_tweets))
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print ("...%s tweets downloaded so far" % (len(alltweets)))
	
	timestr = time.strftime("%Y%m%d-%H%M%S")
	print(timestr)

	filename = folderOutput + "tweetsNYT_" + timestr
    
	#write tweet objects to JSON
	#file = open('tweet.json', 'wb')
	file = open(filename + '.json','w')
	print ("Writing tweet objects to JSON please wait...")
	for status in alltweets:
		json.dump(status._json,file,sort_keys = True,indent = 4)
	#close the file
	print ("Done with JSON")
	file.close()
    
	#transform the tweepy tweets into a 2D array that will populate the csv	
	print ("...writing csv - step 1")
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
	#write the csv	
	#file = open(filename + '.csv','wb')    
	#with open('%s_tweets.csv' % screen_name, 'w') as f:
	with open(filename + '.csv', 'w') as f:
		print ("...writing csv")        
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])        
		writer.writerows(outtweets)
		 
	pass


# In[5]:


if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets(account_monitor)

