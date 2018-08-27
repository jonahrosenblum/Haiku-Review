from haikuCreation import *
from apiKey import *
import tweepy
import time

def sendTweet():
    # Start the time so that we can time how long it takes to run
    start_time = time.time()
    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)

    # Using authentication to create tweepy API
    tweepyAPI = tweepy.API(auth)

    
    # Create a good haiku and convert it to a text form, then tweet it out.
    tweet = createHaiku().getHaikuText()
    tweepyAPI.update_status(tweet)
        
    # Print to console the time it took to run
    print("--- %s seconds ---" % (time.time() - start_time))

sendTweet()
