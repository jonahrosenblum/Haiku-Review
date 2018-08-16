from newsapi import NewsApiClient
import requests
import api_key
from article import Article
import pyphen
import time
import spacy
from itertools import chain, combinations
from nltk.corpus import cmudict

cmudic = cmudict.dict()
pyphendic = pyphen.Pyphen(lang='en')
spacyNLP = spacy.load('en_core_web_sm')
loadedDictionaries = {'cmudic':cmudic, 'pyphendic':pyphendic, 'spacyNLP':spacyNLP}

newsapi = NewsApiClient(api_key=api_key.key)
writeFile1 = open('output5lines.txt', 'w')
writeFile2= open('output7lines.txt', 'w')
newsSources = 'abc-news, al-jazeera-english, associated-press, bbc-news, \
               bleacher-report, bloomberg, business-insider, buzzfeed, \
               cbs-news, cnbc, cnn, daily-mail, espn, financial-times, \
               fox-news, msnbc, national-geographic, nbc-news, politico, \
               reuters, the-economist, the-new-york-times, the-huffington-post, \
               the-washington-post, the-wall-street-journal, time, usa-today, \
               wired'

best5lines = []
best7lines = []
for source in newsSources.split(', '):
    topHeadlines = newsapi.get_top_headlines(sources=source)
    for article in topHeadlines['articles']:
        articleTest = Article(article['source']['name'], article['title'], article['url'], loadedDictionaries)
        #print(articleTest.titleDependencies)
        #print(articleTest.generateValidDictionaries(articleTest.generateTemplates()))
        haikuLine5 = articleTest.getBest(5)
        haikuLine7 = articleTest.getBest(7)
        if haikuLine5:
            best5lines.append((haikuLine5, articleTest.url))
        if haikuLine7:
            best7lines.append((haikuLine7, articleTest.url))
      
for line in best5lines:
    writeFile1.write(' '.join(line[0]) + '\n')
    writeFile1.write(line[1] + '\n')
for line in best7lines:
    writeFile2.write(' '.join(line[0]) + '\n')
    writeFile2.write(line[1] + '\n')
