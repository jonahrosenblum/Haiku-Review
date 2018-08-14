class Article(object):
    # Public methods
    def __init__(self, sourceName, title, url, loadedDictionaries):
        """
        Requires: sourceName, title, and url are strings
        Effects: creates new instance of article
        """
        # Initalizing member variables
        self.sourceName = sourceName
        self.title = title
        self.url = url
        # Initalizing dictionaries for nltk, pyphen, and spaCy
        self.cmudic = loadedDictionaries['cmudic']
        self.pyphendic = loadedDictionaries['pyphendic']
        self.spacyNLP = loadedDictionaries['spacyNLP']
        # Creating text and dependency lists
        doc = self.spacyNLP(title)
        self.titleText = [token.text for token in doc]
        self.titleDependencies = [token.dep_ for token in doc]

    def getBest(self, syllables):
        """
        Requires: syllables is an integer
        Effects: returns either
                  - the "best" phrase containing the specified number of syllables
                  - an empty list
        """
        possiblePhrases = self.generateValidPhrases(self.generateValidDictionaries(self.generateTemplates()), syllables)

    # Private methods
    def generateTemplates(self):
        """
        Requires: none
        Effects: returns list of template objects, each containing the data to a valid sentence
        """
        firstPattern = ['nsubj']
        secondPattern = ['ccomp', 'pcomp', 'ROOT']
        thirdPattern = ['dobj', 'pobj']
        templates = []
        # Creates every possible arrangement of the patterns
        for p1 in firstPattern:
            for p2 in secondPattern:
                for p3 in thirdPattern:
                    templates.append([p1, p2, p3])
        return templates

    def generateValidDictionaries(self, templates):
        """
        Requires: none
        Effects: returns list of valid template dictionaries
        """
        templateDictionaries = []
        for template in templates:
            templateDictionary = {}
            for dep in template:
                if dep in self.titleDependencies:
                    depText = self.titleText[self.titleDependencies.index(dep)]
                    templateDictionary[dep] = {'text':depText,
                                               'syllables':self.countSyllables(depText),
                                               'compounds':{}}
                    firstCompound = self.titleDependencies.index(dep)
                    lastCompound = firstCompound
                    while lastCompound > -1 and self.titleDependencies[lastCompound - 1] == 'compound':
                        lastCompound -= 1
                    for compound in self.titleText[lastCompound:firstCompound]:
                        templateDictionary[dep]['compounds'] = {compound:self.countSyllables(compound)}
                else:
                    break
            if len(templateDictionary) == 3:
                templateDictionaries.append(templateDictionary)
        return templateDictionaries
        #     if len(newSentence) >= 3:
        #         newSentences.append(newSentence)
        # return newSentences


    def generateValidPhrases(self, templateDictionary, syllables):
        """
        Requires: syllables is an integer
        Effects: returns all valid phrases with specified number of syllables
        """

    def countSyllables(self, word):
        """
        Requires: word is a string (can be a hyphenated word)
        Effects: returns number of syllables in word
        """
        try:
            return [len(list(y for y in x if y[-1].isdigit())) for x in self.cmudic[word.lower()]][0]
        except:
            syllabels = 0
            for word in word.split('-'):
                syllabels += self.pyphendic.inserted(word).count('-') + 1
            return syllabels
