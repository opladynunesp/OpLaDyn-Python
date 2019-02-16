
# coding: utf-8

# In[1]:


# -*- coding: utf-8 -*-
"""
Created on Sep 11 2018

@author: Fernanda Farinelli
"""


# In[2]:


consumer_key = 'rWxMBAKB6IgXNVrsXkisVebMU'
consumer_secret = 'xRFc47WcbcgoZYb26OHfMXakda7UFIQMvZw2WftbOsAXpBRKMS'
access_token_key = '1028301224519589889-hrC4g78bb0PJ9RiEbusi657it517wf'
access_token_secret = 'hhwamERYlZUJuLQwWnJtvWvqpB5hFCyNBOCiDVDrT5xIL'
#filename = "C://Users//unesp//ProjetoOpLaDyn//inputs//twitter_tokens_pt.txt"
fileInput = "C://Users//unesp//ProjetoOpLaDyn//inputs//twitter_tokens_Marielle_pt.txt"
folderOutput = 'C:\\Users\\unesp\\ProjetoOpLaDyn\\outputs\\'


# In[3]:


import tweepy #https://github.com/tweepy/tweepy
import csv
import json
import time


# In[4]:


def get_all_tweets(tokens):
    fetched_tweets = ''
    alltweets = []    

    #authorize twitter, initialize tweepy
    # Creating the authentication object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # Setting your access token and secret
    auth.set_access_token(access_token_key, access_token_secret)
    # Creating the API object while passing in auth information
    api = tweepy.API(auth)
    
    # Language code (follows ISO 639-1 standards)
    # language = "pt"    
    '''
    query = 'python'
    max_tweets = 1000
    searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]
    searched_tweets = []
    last_id = -1
    while len(searched_tweets) < max_tweets:
        count = max_tweets - len(searched_tweets)
        try:
            new_tweets = api.search(q=query, count=count, max_id=str(last_id - 1))
            if not new_tweets:
                break
            searched_tweets.extend(new_tweets)
            last_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # depending on TweepError.code, one may want to retry or wait
            # to keep things simple, we will give up on an error
            break    
    '''   
    i=0
    # The search term you want to find    
    while i < len(tokens):
        if i == 0:
            #SEARCH_TERM = tokens[i].strip()
            #fetched_tweets = api.search(q=tokens[i].strip(),lang = "pt")
            fetched_tweets = api.search(q=tokens[i].strip(),lang = "pt",rpp=100,count=1000)
            print('Tweets to "',tokens[i].strip(),'" keyword:',len(fetched_tweets))
        else:
            #SEARCH_TERM = SEARCH_TERM + ' or '+ tokens[i].strip()
            fetched_tweets = api.search(q=tokens[i].strip(),lang = "pt",rpp=100,count=1000)
            alltweets.extend(fetched_tweets)
            print('Tweets to "',tokens[i].strip(),'" keyword:',len(fetched_tweets))
        i = i + 1
    # parsing tweets one by one
    print('alltweets:',len(alltweets))

    #preparing file to write
    timestr = time.strftime("%Y%m%d-%H%M%S")
    #print(timestr)
    
    writeJSON(alltweets,timestr)
    
    
def writeJSON(alltweets,timestr):
    filename = folderOutput + "tweetsKeywordsCaseMarielle_pt_" + timestr
    #write tweet objects to JSON
    file = open(filename + '.json','w')
    print ("Writing tweet objects to JSON please wait...")
    for status in alltweets:
        json.dump(status._json,file,sort_keys = True,indent = 4)
    #close the file
    print ("Done with JSON")
    file.close()

def writeCSV(alltweets,timestr):
    #transform the tweepy tweets into a 2D array that will populate the csv	
    print ("...writing csv - step 1")
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
    filename = folderOutput + "tweetsKeywordsCaseMarielle_pt_" + timestr
    #write the csv	
    with open(filename + '.csv', 'w') as f:
        print ("...writing csv")        
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])        
        writer.writerows(outtweets)    
    


# In[5]:


if __name__ == '__main__':
    #pass in the username of the account you want to download
    with open(fileInput, 'r') as twitter_tokens:
        tokens = twitter_tokens.read().split(',')
        print('Keywords list:',tokens)

    get_all_tweets(tokens)

