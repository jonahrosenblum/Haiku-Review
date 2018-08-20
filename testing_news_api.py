from newsapi import NewsApiClient
import api_key
from article import Article
from haiku import Haiku
from random import choice
import pyphen
import spacy
from itertools import chain, combinations
from nltk.corpus import cmudict

cmudic = cmudict.dict()
pyphendic = pyphen.Pyphen(lang='en')
spacyNLP = spacy.load('en_core_web_sm')
loadedDictionaries = {'cmudic':cmudic, 'pyphendic':pyphendic, 'spacyNLP':spacyNLP}

newsapi = NewsApiClient(api_key=api_key.key)
# writeFile3 = open('input.txt', 'w')
randomHaikus = open('randomHaikus3.txt','w')
newsSources = 'abc-news, al-jazeera-english, associated-press, bbc-news, \
               bleacher-report, bloomberg, business-insider, \
               cbs-news, cnbc, cnn, espn, financial-times, \
               fox-news, msnbc, national-geographic, nbc-news, politico, \
               reuters, the-economist, the-new-york-times, the-huffington-post, \
               the-washington-post, the-wall-street-journal, time, usa-today, \
               wired'

best5lines = []
best7lines = []
for source in newsSources.split(', '):
    topHeadlines = newsapi.get_top_headlines(sources=source)
    for articleInfo in topHeadlines['articles']:
        # writeFile3.write(str(articleInfo) + '\n')
        article = Article(articleInfo['source']['name'], articleInfo['title'], articleInfo['url'], loadedDictionaries)
        haikuLine5 = article.getBest(5)
        haikuLine7 = article.getBest(7)
        if haikuLine5:
            best5lines.append({'title':haikuLine5, 'url':article.url, 'source':article.sourceName})
        if haikuLine7:
            best7lines.append({'title':haikuLine7, 'url':article.url, 'source':article.sourceName})

bestHaikuScore = -5
for randomIteration in range(100):
    haiku = Haiku(choice(best5lines), choice(best7lines), choice(best5lines))
    if (haiku.getScore() > bestHaikuScore):
        randomHaikus.write(haiku.getHaiku())
    else:
        print(haiku.getHaiku())
    
