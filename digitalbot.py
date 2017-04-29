#!/usr/bin/env python
# coding: utf-8

import tweepy
import datetime, random, time
from keys import keys

import sys
reload( sys )
sys.setdefaultencoding( 'utf-8' )


def randommessage( messages ):
    return random.choice( messages )

def authentication( keys ):
    CONSUMER_KEY = keys['consumer_key']
    CONSUMER_SECRET = keys['consumer_secret']
    ACCESS_TOKEN = keys['access_token']
    ACCESS_TOKEN_SECRET = keys['access_token_secret']
    
    auth = tweepy.OAuthHandler( CONSUMER_KEY, CONSUMER_SECRET )
    auth.set_access_token( ACCESS_TOKEN, ACCESS_TOKEN_SECRET )
    api = tweepy.API( auth )
    return api

def searchAndReply( api, messages, sleeptime ):
    tweets = api.search( q="digital lang:fr" )

    if len( tweets ) != 0:
        for tweet in tweets:
            if (datetime.datetime.now() - tweet.created_at).seconds < sleeptime:
                if tweet.lang == "fr":
                    #            print tweet.user.screen_name, ": ", "[", tweet.created_at, "]" , tweet.text
                    text = "@" + tweet.user.screen_name + " " + randommessage( messages )
                    print text
                    s = api.update_status( text, tweet.id )
    time.sleep( sleeptime )

                    

def main():
    SLEEPTIME = 36000 #900 # 15 minutes
    MESSAGELIST = [ "Numérique bordel !",
                    "Avé les doigts ?",
                    "Numérique rique rique..." ]

    api = authentication( keys )
    searchAndReply( api, MESSAGELIST, SLEEPTIME )
    
if "__main__" == __name__:
    main()
    
