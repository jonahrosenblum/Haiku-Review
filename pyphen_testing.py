# import pyphen
# import time
# import spacy
# from article import Article
# from itertools import chain, combinations
# from nltk.corpus import cmudict
from textblob import TextBlob
# cmudic = cmudict.dict()
# pyphendic = pyphen.Pyphen(lang='en')
# spacyNLP = spacy.load('en_core_web_sm')
# loadedDictionaries = {'cmudic':cmudic, 'pyphendic':pyphendic, 'spacyNLP':spacyNLP}

# # stackoverflow.com/questions/405161
# def countSyllabels(word):
#     try:
#         return [len(list(y for y in x if y[-1].isdigit())) for x in cmudic[word.lower()]][0]
#     except:
#         syllabels = 0
#         for word in word.split('-'):
#             syllabels += pydic.inserted(word).count('-') + 1
#         return syllabels


# # abbreviatedSentences = getAbbreviatedSentences(inputSentence, getPatterns())
# # getAllSentencePermutations(abbreviatedSentences)
# # for sentence in abbreviatedSentences:
# #     print(sentence)
# articleTest = Article('ruter', 'California Sea Lions Keep Getting Shot by Fishermen', 'www.urmom', loadedDictionaries)
# print(articleTest.titleDependencies)
# #print(articleTest.generateValidDictionaries(articleTest.generateTemplates()))
# #print(articleTest.generateValidPhrases(articleTest.generateValidDictionaries(articleTest.generateTemplates()), 5))
# # print(articleTest.getBest(5))

readFile = open('input.txt','r')
writeFile = open('sentTesting.txt','w')
dicts_from_file = []
with open('input.txt','r') as inf:
    for line in inf:
        dicts_from_file.append(eval(line))  
for article in dicts_from_file:
    articleTitle = article['title']
    analysis = TextBlob(articleTitle)
    writeFile.write(articleTitle + '\n' + str(analysis.sentiment) + '\n\n')
