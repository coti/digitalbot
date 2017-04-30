#!/usr/bin/env python
# coding: utf-8

import tweepy
import random, time
from keys import keys

import sys
reload( sys )
sys.setdefaultencoding( 'utf-8' )

def printhelp():
    print sys.argv[0], " : utilisation"
    print "\t sans argument : chercher les tweets et répondre à tous"
    print "\t -id <TWEET ID> : répondre à un tweet en particulier"
    print "\t -sd/--since/s <TWEET ID> : lancer la boucle à partir d'un tweet en particulier"
    return    

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
    
def searchAndReply( api, messages, sleeptime=60, maxid=0 ):
    tweets = api.search( q="digital lang:fr" )

    while( True ):
    
        if len( tweets ) != 0:
            for tweet in tweets:
                if tweet.lang == "fr" and not tweet.user.screen_name == "liberezledoigt":
                    tid = replyto( api, tweet, messages )
                    maxid = max( tid, maxid )

        print "Max id: ", maxid
        time.sleep( sleeptime )
        tweets = api.search( q="digital lang:fr since_id:" + str( maxid ) )

    return # should never happen

def parsearguments( api, messages ):
    if( sys.argv[1] in [ "h", "-h", "--help" ]  ):
        printhelp()
    if( sys.argv[1] == "-id" ):
        tweet = api.statuses_lookup( [ int( sys.argv[2] ) ] )
        print tweet[0].text
        replyto( api, tweet[0], messages )
    if( sys.argv[1] in ["s", "-s", "--since" ] ):
        maxid = int( sys.argv[2] )
        searchAndReply( api, messages, maxid = maxid )        
    return

def main():
    SLEEPTIME = 60 
    MESSAGELIST = [ "Numérique bordel !",
                    "Avé les doigts ?",
                    "Numérique rique rique...",
                    "Comme dans \"orgasme digital\" ?",
                    "Je préfère Numérique Hunter à Digital Capone",
                    "Numérique ta mère !",
                    "D'après l'Académie Française, tu parles de doigts. http://www.academie-francaise.fr/digital",
                    "Il n'ya que deux métiers dans le digital : proctologue et pianiste",
                    "Les orteils sont-ils des doigts ?"]

    api = authentication( keys )
    if( 1 == len( sys.argv ) ):
        searchAndReply( api, MESSAGELIST, SLEEPTIME )
    else:
        parsearguments( api, MESSAGELIST )
    
if "__main__" == __name__:
    main()
    
