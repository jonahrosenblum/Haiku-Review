from newsapi import NewsApiClient
from apiKey import newsAPIKey
from article import Article
from haiku import Haiku
import newsapi
import pyphen
import spacy
from nltk.corpus import cmudict

def loadObjects():
    """
    Requires: none
    Effects: Returns a dictionary of complex objects from nltk, spacy, and 
    pyphen holding data that allows us to process data.
    """
    cmudic = cmudict.dict()
    pyphendic = pyphen.Pyphen(lang='en')
    spaCyNLP = spacy.load('en_core_web_sm')
    return {'cmudic':cmudic, 'pyphendic':pyphendic, 'spaCyNLP':spaCyNLP}

def getHaikuLines(loadedObjects):
    """
    Requires: loadedObjects contains a dictionary with a nltk dictionary,
    a pyphen dictionary, and a spaCy NLP object all properly named in
    accordance with the Article class.
    Effects: Returns a dictionary containing two lists containing news headlines
    of lengths 5 and 7 syllables long.
    """
    newsApi = newsapi.NewsApiClient(api_key=newsAPIKey)
    # A list of all news sources we get our headlines from, subject to change
    newsSources = ['abc-news', 'al-jazeera-english', 'associated-press', 
                   'bbc-news', 'bleacher-report', 'bloomberg', 
                   'business-insider', 'cbs-news', 'cnbc', 'cnn', 'espn', 
                   'financial-times', 'fox-news', 'msnbc', 'national-geographic', 
                   'nbc-news', 'politico', 'reuters', 'the-economist', 
                   'the-new-york-times', 'the-huffington-post', 
                   'the-washington-post', 'the-wall-street-journal', 'time', 
                   'usa-today', 'wired']
    # The lists that will hold all 5 and 7 syllable news headlines
    fiveSyllableLines = []
    sevenSyllableLines = []
    # Iterate through each news source in the list to get all headlines
    for newsSource in newsSources:
        # Getting the top headlines for a particular news source
        topHeadlines = newsApi.get_top_headlines(sources=newsSource, page_size=100)
        # Go through all the article dictionaries in the list of top headlines
        # and extract information about each article.
        for articleInfo in topHeadlines['articles']:
            # Instantiation of an article object
            article = Article(articleInfo['title'], loadedObjects)
            # Gets the best 5 and 7 syllable lines respectively
            fiveSyllableLine = article.getBest(5)
            sevenSyllableLine = article.getBest(7)
            # If there is a 'best' five syllable line, add it to the list of
            # headlines, same for the seven syllable line.
            if fiveSyllableLine:
                # Makes sure that the first letter of each word is capitalized
                fiveSyllableLine = [word.title() for word in fiveSyllableLine]
                # Add a dictionary to the list containing info about the line
                fiveSyllableLines.append({
                                          'title':fiveSyllableLine, 
                                          'url':articleInfo['url'], 
                                          'source':articleInfo['source']['name'], 
                                          'entCount':article.totalEntities(fiveSyllableLine)
                                          })
            if sevenSyllableLine:
                # Makes sure that the first letter of each word is capitalized
                sevenSyllableLine = [word.title() for word in sevenSyllableLine]
                # Add a dictionary to the list containing info about the line
                sevenSyllableLines.append({
                                           'title':sevenSyllableLine, 
                                           'url':articleInfo['url'], 
                                           'source':articleInfo['source']['name'], 
                                           'entCount':article.totalEntities(sevenSyllableLine)
                                           })
    return {
            'fiveSyllableLines':fiveSyllableLines,
            'sevenSyllableLines':sevenSyllableLines
            }

def generateBestHaiku(headlines):
    """
    Requires: headlines is a dictionary containing two lists, one that has all
    viable 5 syllable headlines, and one that has all 7 syllable headlines
    Effects: Returns a string with the 'best' haiku in it.
    """
    linksFile = open('recentlyUsedLinks.txt','r')
    recentlyUsedLinks = eval(linksFile.read())
    # Assume the baseline best score is 0 meaning that there are no 'errors'
    # with the haiku, but it likely isn't very interesting.
    bestHaikuScore = 0
    # Although it doesn't necesarily make sense to keep track of ALL haiku
    # objects that are 'best' at some point, this helps massively with debugging
    bestHaikus = []
    # This is not elegant or efficient at all, but it gets the job done and
    # we are not too concerned about how fast this code runs.
    # Gets the first line of the haiku from the list of 5 syllable phrases
    for firstLine in headlines['fiveSyllableLines']:
        # Gets the second line of the haiku from the list of 7 syllable phrases
        for secondLine in headlines['sevenSyllableLines']:
            # Gets the third line of the haiku from the list of 5 syllable phrases
            for thirdLine in headlines['fiveSyllableLines']:
                # Instantiation of a haiku object
                haiku = Haiku(firstLine, secondLine, thirdLine, recentlyUsedLinks)
                # Calculates the 'score' of the haiku, see class documentation
                haikuScore = haiku.getScore()
                # Checks if this haiku has a better score than the current best
                if haikuScore > bestHaikuScore:
                    # This haiku is now the best, add to list and update score
                    bestHaikus.append(haiku)
                    bestHaikuScore = haikuScore
    # Returns last haiku in the list with the highest score as a string
    return bestHaikus[-1]

def updateRecentlyUsedLinks(bestHaiku):
    file = open('recentlyUsedLinks.txt','r+')
    recentlyUsedLinks = ([bestHaiku.lineOneUrl, bestHaiku.lineTwoUrl, bestHaiku.lineThreeUrl] + eval(file.read()))[:12]
    file.seek(0)
    file.write(str(recentlyUsedLinks))
    file.close()

def createHaiku():
    bestHaiku = generateBestHaiku(getHaikuLines(loadObjects()))
    updateRecentlyUsedLinks(bestHaiku)
    return bestHaiku