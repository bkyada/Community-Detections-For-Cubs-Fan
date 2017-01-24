from collections import Counter, defaultdict
import configparser
import matplotlib.pyplot as plt
import sys
import time
import csv

import numpy as np
from TwitterAPI import TwitterAPI
from sklearn.feature_extraction.text import CountVectorizer
import pickle
import json
import operator
from datetime import datetime

# To make connection method is created credentials are in twitter.cfg
def get_twitter(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    twitter = TwitterAPI(
                         config.get('twitter', 'consumer_key'),
                         config.get('twitter', 'consumer_secret'),
                         config.get('twitter', 'access_token'),
                         config.get('twitter', 'access_token_secret'))
    return twitter

twitter = get_twitter('twitter.cfg')
print('Established Twitter connection.')

#for i in range(0, 16): ## iterate through 16 times to get max No. of tweets
# Collect only original tweets excluding re-tweets.
def fatch_available_tweets_cubs(screen_name):
    cubs_tweet = []
    tweetCount=0
    addCount=0
    tweets = set()
    b = []
    for i in range(0, 30):
        if i==0:
            request = twitter.request('search/tweets', {'q': screen_name, 'lang':'en', 'count': 5000, 'result_type':'mixed' })
        else:
            request = twitter.request('search/tweets', {'q': screen_name, 'lang':'en', 'count': 5000, 'result_type':'mixed', 'max_id' : b[-1]})
        if request.status_code == 200:
            for tweet in request:
                text = tweet['text']
                screen_name = tweet['user']['screen_name']
                user_mentioned = tweet['entities']['user_mentions']
                created_at = tweet['created_at']
                #cubs_tweet.append({'created_at' : str(created_at), 'text': tweet['text'], 'screen_name': tweet['user']['screen_name'], 'user_mentioned': tweet['entities']['user_mentions']})
                if text not in tweets:
                    tweets.add(text)
                    if "\n" in text:
                        text = text.replace('\n','')
                    if "\t" in text:
                        text = text.replace('\t','')
                    if not text.startswith('rt') and not text.startswith('RT'):
                        #FileName.write("%s %s %s %s %s %s %s\n"%(created_at,',',screen_name,',',text,',',user_mentioned))
                        cubs_tweet.append({'created_at' : str(created_at), 'text': tweet['text'], 'screen_name': tweet['user']['screen_name'], 'user_mentioned': tweet['entities']['user_mentions']})
                #addCount+=1
            b.append(tweet['id']) ## append tweet id's
    #tweetCount+=1

    #print("Downloaded {0} tweets".format(tweetCount))
    #print ("Downloaded {0} tweets, Saved to {1}".format(addCount, FileName.name))
        elif request.status_code == 88:
            continue
        else:
            print (screen_name)
            print ( sys.stderr, 'Got error:\n', request.text, '\nsleeping for 15 minutes.')
            sys.stderr.flush()
            time.sleep(61 * 15)

    return cubs_tweet

# To check if user information is protected!
def get_users_status(screen_name):
    request = twitter.request('users/lookup',{'screen_name':screen_name})
    for tweet in request:
        return tweet['protected']

# fatch friends of given screen_name
def fatch_friends(screen_name):
    #print(screen_name)
    request = twitter.request('friends/ids',{'screen_name':screen_name, 'count':5000})
    friends = []
    if request.status_code==200:
        for r in request:
            friends.append(r)
    else:
        print('Got error %s \nsleeping for 15 minutes.' % request.text)
        sys.stderr.flush()
        time.sleep(61 * 15)
    
    return sorted(friends)

#Get the list of accounts of each user's friends.
def add_all_friends(users, friends):
    for u in users:
        print(u)
        status = get_users_status(u)
        if status == True:
            print("User information is protected!!")
        else:
            f = fatch_friends(u)
            if f!= []:
                friends[u] = f

def get_tweets(q):
    tweets = []
    b=[]
    for i in range(0, 15):
        if i==0:
            request = twitter.request('search/tweets', {'q': q, 'lang':'en', 'count': '500', 'result_type':'mixed' })
        else:
            request = twitter.request('search/tweets', {'q': q, 'lang':'en', 'count': '500', 'result_type':'mixed', 'max_id' : b[-1]})
        if request.status_code == 200:
            for tweet in request:
                text = tweet['text']
                if not text.startswith('rt') and not text.startswith('RT'):
                    tweets.append(text)
                b.append(tweet['id'])
    return tweets


def findNodes(Ftweets):
    # will take pair of user and mentioned user from tweets
    mentioned_list = []
    for i in Ftweets:
        user_mention = i['user_mentioned']
        if user_mention != '[]':
            for j in user_mention:
                x = (i['screen_name'],j['screen_name'])
        mentioned_list.append(x)
    d = defaultdict(list)
    for k, v in mentioned_list:
        d[k].append(v)
    finaldict ={}
    for k,v in d.items():
        setV = set()
        for vi in v:
            setV.add(vi)
        finaldict[k]=vi
    node=set()
    values=[]
    keys=[]
    for k,v in finaldict.items():
        keys.append(k)
        values.append(v)
    for k,v in finaldict.items():
        node.add(k)
        node.add(v)
    c1 = Counter()
    c1.update(values)
#print(c1)
    FinalNodes = set()
    fnodes = []
    for cVal in c1:
        if(c1[cVal])>1:
            FinalNodes.add(cVal)
        fnodes.append(cVal)
    n = len(FinalNodes)
    if n<10:
        for x in fnodes:
            FinalNodes.add(x)
            n+=1
            if n==10:
                break

    return node,FinalNodes

def store_file(data,path):
    outF = open(path, 'wt')
    json.dump(data , outF, indent=4)
    outF.close()

def main():
    #Collect tweets
    Ftuples=fatch_available_tweets_cubs("Cubs")
    # Run this code to load Final initial nodes
    # all data already dumpled in pickle file
    pickle.dump(Ftuples, open( "DataStore/sorted_all_tweetsMixedF.p", "wb" ))
    Ftweets = pickle.load(open('DataStore/sorted_all_tweetsMixedF.p', 'rb'))
    store_file(Ftweets,'DataStore/datafromTwitter.txt')
    Fnodes, nodes = findNodes(Ftweets)
    #print(Fnodes)
    #print(nodes)
    pickle.dump(nodes, open( "DataStore/nodes.p", "wb" ))
    nodes = pickle.load(open('DataStore/nodes.p', 'rb'))
    n = open('DataStore/Nodes.txt', 'w')
    for k in nodes:
        n.write(k+"\n")
    n.close()
    friends = {}
    add_all_friends(nodes, friends)
    pickle.dump(friends, open( "DataStore/NodeFriends.p", "wb" ))
    frnds = pickle.load(open('DataStore/NodeFriends.p', 'rb'))
    store_file(frnds,'DataStore/FriendsNodes.txt')
    tweets = get_tweets("Cubs")
    #Stored in pickle file
    pickle.dump(tweets, open( "DataStore/tweets.p", "wb" ))
    tweets = pickle.load(open('DataStore/tweets.p', 'rb'))
    store_file(tweets,'DataStore/Tweets.txt')
    collectResult={}
    collectResult['totalUser'] = len(nodes)
    pickle.dump(collectResult, open( "DataStore/collectResult.p", "wb" ))

if __name__ == '__main__':
    main()

