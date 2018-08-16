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
        if possiblePhrases:
            return possiblePhrases[0]
        return possiblePhrases

    # Private methods
    def generateTemplates(self):
        """
        Requires: none
        Effects: returns list of template objects, each containing the data to a valid sentence
        """
        firstPattern = ['nsubj']
        secondPattern = ['ccomp', 'pcomp']
        thirdPattern = ['dobj']
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
                                               'compounds':[]}
                    firstCompound = self.titleDependencies.index(dep)
                    lastCompound = firstCompound
                    while lastCompound > -1 and self.titleDependencies[lastCompound - 1] == 'compound':
                        lastCompound -= 1
                    for compound in self.titleText[lastCompound:firstCompound]:
                        templateDictionary[dep]['compounds'].append((compound, self.countSyllables(compound)))
                else:
                    break

            if len(templateDictionary) == 3:
                templateDictionaries.append(templateDictionary)
        return templateDictionaries


    def generateValidPhrases(self, templateDictionaries, validSyllables):
        """
        Requires: syllables is an integer
        Effects: returns all valid phrases with specified number of syllables
        """
        # This is going to be the array of valid phrases that is returned
        validPhrases = []
        # Go through each template dictionary and find all valid phrases in each
        for templateDictionary in templateDictionaries:
            # depPhrase is all the dependencies as a phrase
            depPhrase = []
            # Go through deps in the dictionary and adds text to potentialPhrase
            for dep in templateDictionary:
                depPhrase.append((templateDictionary[dep]['text'], templateDictionary[dep]['syllables']))
            # Checks if the phrase is already valid
            if self.countPhraseSyllables(depPhrase) == validSyllables:
                # If phrase is valid, add it to the list and go to the next dic
                validPhrases.append([phrase[0] for phrase in depPhrase])
                continue
            elif self.countPhraseSyllables(depPhrase) > validSyllables:
                # If phrase can never be valid, go to next dic
                continue
            # This int will keep track of which dependency the outer loop is on
            firstCount = 0
            # Go through each compound associated with dep terms
            for dep in templateDictionary:
                # Set the dep dictionary as a variable because it makes life easier
                depDictionary = templateDictionary[dep]
                # Get the text associated with the dep and the number of syllables as a tuple
                depTerm = (depDictionary['text'], depDictionary['syllables'])
                for firstCompound in depDictionary['compounds']:
                    firstCount += 1
                    potentialPhrase = depPhrase.copy()
                    potentialPhrase.insert(potentialPhrase.index(depTerm), firstCompound)
                    if self.countPhraseSyllables(potentialPhrase) == validSyllables:
                        # If phrase is valid, add it to the list and go to the next compound
                        validPhrases.append([phrase[0] for phrase in potentialPhrase])
                        continue
                    elif self.countPhraseSyllables(potentialPhrase) > validSyllables:
                        # If phrase can never be valid, go to next compound
                        continue
                    # This int will keep track of which dependency the inner loop is on
                    subsequentCount = 0
                    for depInner in templateDictionary:
                        # Set the dep dictionary as a variable because it makes life easier
                        depDictionaryInner = templateDictionary[depInner]
                        # Get the text associated with the dep and the number of syllables as a tuple
                        depTermInner = (depDictionaryInner['text'], depDictionaryInner['syllables'])
                        for subsequentCompound in depDictionaryInner['compounds']:
                            subsequentCount += 1
                            if subsequentCount > firstCount:
                                potentialPhrase.insert(potentialPhrase.index(depTermInner), subsequentCompound)
                                if self.countPhraseSyllables(potentialPhrase) == validSyllables:
                                    # If phrase is valid, add it to the list and go to the next compound
                                    validPhrases.append([phrase[0] for phrase in potentialPhrase])
                                    potentialPhrase.remove(subsequentCompound)
                                elif self.countPhraseSyllables(potentialPhrase) > validSyllables:
                                    # If phrase can never be valid, go to next compound
                                    potentialPhrase.remove(subsequentCompound)
        return validPhrases
        
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
    
    def countPhraseSyllables(self, sentence):
        return sum([word[1] for word in sentence])
