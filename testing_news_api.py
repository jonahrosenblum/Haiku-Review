from newsapi import NewsApiClient
import requests
import api_key
newsapi = NewsApiClient(api_key=api_key.key)
writeFile = open('output2.txt', 'w')
newsSources = 'abc-news, al-jazeera-english, associated-press, bbc-news, \
               bleacher-report, bloomberg, business-insider, buzzfeed, \
               cbs-news, cnbc, cnn, daily-mail, espn, financial-times, \
               fox-news, msnbc, national-geographic, nbc-news, politico, \
               reuters, the-economist, the-new-york-times, the-huffington-post, \
               the-washington-post, the-wall-street-journal, time, usa-today, \
               wired'
topHeadlines = newsapi.get_top_headlines(sources=newsSources)
for article in topHeadlines['articles']:
    writeFile.write(str(article) + '\n')
