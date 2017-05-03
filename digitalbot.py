#!/usr/bin/env python
# coding: utf-8

import tweepy
import random, time, re
from keys import keys
from data import MESSAGELIST, MESSAGELIST2, IGNORED

import sys
reload( sys )
sys.setdefaultencoding( 'utf-8' )

def printhelp():
    print sys.argv[0], " : utilisation"
    print "\t sans argument : chercher les tweets et répondre à tous"
    print "\t -id/--id/id <TWEET ID> : répondre à un tweet en particulier"
    print "\t -sd/--since/s <TWEET ID> : lancer la boucle à partir d'un tweet en particulier"
    return    

def randommessage( messages ):
    return random.choice( messages )

def isinurl( txt ) :
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', txt)
    for u in urls:
        if "digita" in u:
            return True
    return False

def authentication( keys ):
    CONSUMER_KEY = keys['consumer_key']
    CONSUMER_SECRET = keys['consumer_secret']
    ACCESS_TOKEN = keys['access_token']
    ACCESS_TOKEN_SECRET = keys['access_token_secret']
    
    auth = tweepy.OAuthHandler( CONSUMER_KEY, CONSUMER_SECRET )
    auth.set_access_token( ACCESS_TOKEN, ACCESS_TOKEN_SECRET )
    api = tweepy.API( auth )
    return api

def replyto( api, tweet, messages ):
    #  print tweet.user.screen_name, ": ", "[", tweet.created_at, "]" , tweet.text
    try: # on ne répond pas aux RT
        rt = tweet.retweeted_status
    except AttributeError:
        pass
    else:
        return tweet.id
    text = "@" + tweet.user.screen_name + " " + randommessage( messages )
    print text
    try:
        s = api.update_status( text, in_reply_to_status_id = tweet.id )
    except tweepy.error.TweepError:
        pass
    return tweet.id
    
def searchAndReply( api, sleeptime=60, maxid=0 ):
    tweets = api.search( q="digital lang:fr" ) + api.search( q="digitaux lang:fr" ) + api.search( q="digitalisation lang:fr" )
    tweets2 = api.search( q="digitale lang:fr" ) + api.search( q="digitales lang:fr" )

    while( True ):
    
        if len( tweets ) != 0:
            for tweet in tweets:
                if tweet.lang == "fr" and tweet.user.screen_name not in IGNORED and not isinurl( tweet.text ):
                    tid = replyto( api, tweet, MESSAGELIST )
                    maxid = max( tid, maxid )

        if len( tweets2 ) != 0:
            for tweet in tweets2:
                if tweet.lang == "fr" and tweet.user.screen_name not in IGNORED and not isinurl( tweet.text ):
                    tid = replyto( api, tweet, MESSAGELIST + MESSAGELIST2 )
                    maxid = max( tid, maxid )

                    
        print "Max id: ", maxid
        time.sleep( sleeptime )
        tweets = api.search( q="digital lang:fr since_id:" + str( maxid+1 ) )

    return # should never happen

def parsearguments( api ):
    if( sys.argv[1] in [ "h", "-h", "--help" ]  ):
        printhelp()
    if( sys.argv[1] in [ "-id", "--id", "id" ] ):
        if '2.3' == tweepy.__version__:
            print "not available with this version of Tweepy"
            return
        tweet = api.statuses_lookup( [ int( sys.argv[2] ) ] )
        print tweet[0].text
        replyto( api, tweet[0], MESSAGELIST )
    if( sys.argv[1] in ["s", "-s", "--since" ] ):
        maxid = int( sys.argv[2] )
        searchAndReply( api, maxid = maxid )        
    return

def main():
    SLEEPTIME = 60 

    api = authentication( keys )
    if( 1 == len( sys.argv ) ):
        searchAndReply( api, SLEEPTIME )
    else:
        parsearguments( api )
    
if "__main__" == __name__:
    main()
    
