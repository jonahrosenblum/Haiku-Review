# The Haiku Review

A twitter bot that tweets haikus of what's going on in the news.

## How it Works
- Uses the [newsapi-python](https://github.com/mattlisiv/newsapi-python) package
that utiilizes [an api](https://newsapi.org/docs/) that pulls from various major news sources
to get news headlines from lots of current articles.
- Finds the headlines which follow distinct predetermined grammatical patterns through *spaCy's* part of speech and dependency tagging and attempts to shorten sentences to their most basic form.
- Checks if the new shortened headlines have the correct number of syllables to fit in a haiku using *nltk* and *pyphen*.
- Generates thousands of possible haikus, and scores each one according to several metrics to find the best haiku that summarizes the news.
- Sends a tweet to [@haikureviewlive](https://twitter.com/haikureviewlive) through *tweepy*, twitter's api.

## Installation
To use this project: 
1. Clone it to your machine.
2. Download the necesary packages (versions listed below).
3. Get API keys for tweepy and newsapi and add them to a file you will create called apiKey.py, name the variables so that they line up with the code. We did not include out apiKey file for obvious reasons.
4. Run it in terminal with `python3 sendTweet.py` 

These are the currently used version of all requires packages:  
tweepy==3.6.0  
spacy==2.0.11  
nltk==3.3  
Pyphen==0.9.4  
newsapi-python==0.2.3

## Authors
Envisioned by Jonah Rosenblum and Dustin Brown  
Written and Developed by Jonah Rosenblum

## License
This project is licensed under the MIT License - see the LICENSE.md file for details

## Fair Warning
Sometimes, in an attempt to shorten a sentence, a resulting phrase that is tweeted out may convey a message that is untrue, inflamatory, or offensive to some. Please do not assume that any line of a tweeted haiku is a true statement and read all articles linked at the bottom of each tweet for more accurate details about each news story. This is an *unintended* effect of running the program, and anyone using this code should be aware of this and include a similar warning if they chose to use or alter this code.

