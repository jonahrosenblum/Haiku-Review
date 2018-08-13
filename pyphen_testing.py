import pyphen
import time
import spacy
from itertools import chain, combinations
from nltk.corpus import cmudict

cmudic = cmudict.dict()
pydic = pyphen.Pyphen(lang='en')
nlp = spacy.load('en_core_web_sm')

# stackoverflow.com/questions/405161
def countSyllabels(word):
    try:
        return [len(list(y for y in x if y[-1].isdigit())) for x in cmudic[word.lower()]][0]
    except:
        syllabels = 0
        for word in word.split('-'):
            syllabels += pydic.inserted(word).count('-') + 1
        return syllabels

def isHaiku(sentence):
    syllabels = 0
    for word in sentence.split(' '):
        syllabels += countSyllabels(word)
    if syllabels == 5:
        return 5
    elif syllabels == 7:
        return 7
    else:
        return 0

def getPatterns():
    firstPattern = ['nsubj']
    secondPattern = ['ccomp', 'pcomp', 'ROOT']
    thirdPattern = ['dobj', 'pobj']
    patterns = []
    for p1 in firstPattern:
        for p2 in secondPattern:
            for p3 in thirdPattern:
                patterns.append([p1, p2, p3])
    return patterns


inputSentence = 'Brad Pitt says he loaned $8 million to Angelina Jolie, paid $1.3 million in child support'

def getAbbreviatedSentences(sentence, patterns):
    doc = nlp(sentence)
    sentenceText = [token.text for token in doc]
    sentenceDependencies = [token.dep_ for token in doc]
    sentencePOS = [token.pos_ for token in doc]
    # print(sentenceText)
    # print(sentenceDependencies)
    # print(sentencePOS)
    newSentences = []
    for pattern in patterns:
        newSentence = []
        for dep in pattern:
            if dep in sentenceDependencies:
                firstCompound = sentenceDependencies.index(dep)
                lastCompound = firstCompound
                while lastCompound > -1 and sentenceDependencies[lastCompound - 1] == 'compound':
                    lastCompound -= 1
                for compound in sentenceText[lastCompound:firstCompound]:
                    newSentence.append((compound, 'compound'))
                newSentence.append((sentenceText[sentenceDependencies.index(dep)], dep))
            else:
                break
        if len(newSentence) >= 3:
            newSentences.append(newSentence)
    return newSentences

def getCompounds(abbreviatedSentences):
    compounds = []
    for sentence in abbreviatedSentences:
        for word in sentence:
            if word[1] == 'compound' and word[0] not in compounds:
                compounds.append(word[0])
    return compounds


def findPowerSet(abbreviatedSentences):
    xs = list(abbreviatedSentences)
    return list(chain.from_iterable(combinations(xs,n) for n in range(len(xs)+1)))

def getAllSentencePermutations(abbreviatedSentences):
    newPermutations = []
    compoundsPowerSet = findPowerSet(getCompounds(abbreviatedSentences))
    for sentence in abbreviatedSentences:
        for compoundsSet in compoundsPowerSet:
            print(compoundsSet)
            for compound in compoundsSet:
                print(compound)


abbreviatedSentences = getAbbreviatedSentences(inputSentence, getPatterns())
getAllSentencePermutations(abbreviatedSentences)
# for sentence in abbreviatedSentences:
#     print(sentence)
