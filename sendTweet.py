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
    print("--- %s seconds ---" % (time.time() - start_time))
    print(tweet)
    if input('tweet?\n>') == 'y':
        tweepyAPI.update_status(tweet)
    else:
        file = open('recentlyUsedLinks.txt','r')
        recentlyUsedLinks = eval(file.read())
        print(recentlyUsedLinks)
        linesToKeep = str(input('lines to keep\n>'))
        for line in sorted(linesToKeep, reverse = True):
            recentlyUsedLinks.pop(int(line) - 1)
        file.close()
        open("recentlyUsedLinks.txt",'w').close()
        file = open("recentlyUsedLinks.txt",'w')
        file.write(str(recentlyUsedLinks))
        file.close()

        
    # Print to console the time it took to run
    


sendTweet()
