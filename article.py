class Article(object):
    # Public methods
    def __init__(self, title, loadedObjects):
        """
        Requires: sourceName, title, and url are strings
        Effects: creates new instance of article
        """
        # Initalizing member variables
        self.title = title
        # Initalizing dictionaries for nltk, pyphen, and spaCy
        self.cmudic = loadedObjects['cmudic']
        self.pyphendic = loadedObjects['pyphendic']
        self.spaCyNLP = loadedObjects['spaCyNLP']
        # Creating text and dependency lists
        phrase = self.spaCyNLP(title)
        self.titleText = [token.text for token in phrase]
        self.titleDependencies = [token.dep_ for token in phrase]

    def getBest(self, syllables):
        """
        Requires: syllables is an integer
        Effects: returns either
                  - the "best" phrase containing the specified number of syllables
                  - an empty list
        """
        # Get all possible phrases that have the specified number of syllables
        possiblePhrases = self.generateValidPhrases(self.generateValidDictionaries(self.generateTemplates()), syllables)
        # Words we don't want in titles because they don't make a lot of sense
        badWords = ['say', 'says', 'you', '#', 'we']
        # Goes through each possible phrase, to find the one with the most words
        bestPhrase = []
        for phrase in possiblePhrases:
            # If phrase has more words, make it the best phrase
            if len(phrase) > len(bestPhrase):
                bestPhrase = phrase
        # Gets the deps of the 'best' phrase
        bestPhraseDependencies = [token.dep_ for token in self.spaCyNLP(' '.join(bestPhrase))]
        # We don't want phrases that don't end in direct objects, this checks that
        # but it needs every word to be lower case for it to work
        bestPhrase = [word.lower() for word in bestPhrase]
        if (bestPhraseDependencies and bestPhraseDependencies[-1] == 'dobj' 
           and not any(badWord in bestPhrase for badWord in badWords)):
            return bestPhrase
        # Otherwise return an empty list
        return []
        
    def totalEntities(self, haikuLine):
        """
        Requires: haikuLine is a list of strings
        Effects: returns total amount of entities of line        
        """   
        return len(self.spaCyNLP(' '.join(haikuLine)).ents)

    # Private methods
    def generateTemplates(self):
        """
        Requires: none
        Effects: returns list of template lists, each containing the 
        dependencies that make up a "valid" sentence.
        Notes: The function operates like this because we wanted a customizable
        set of patterns that we could change at any time by altering the lists
        of first, second, and third patterns. Right now it seems dumb to do it 
        this way, but it alllows for easier change in the future.
        """
        firstPattern = ['nsubj']
        secondPattern = ['pcomp','ccomp', 'ROOT']
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
        # Holds all the template dictionaries that will be returned
        templateDictionaries = []
        # List of dependencies that modify words (we look for these)
        compoundDeps = ['compound', 'amod', 'appos', 'nmod', 'partmod']
        # Iterate through each generated template
        for template in templates:
            # This is a specific dictionary type for our purposes, see README 
            # for better layout explanation
            templateDictionary = {}
            # Iterate through each dependency in the dictionary
            for dep in template:
                # Checks to see if the dependency is in the list of dependencies 
                # in the title
                if dep in self.titleDependencies:
                    # depText is the word associated with the dependency
                    depText = self.titleText[self.titleDependencies.index(dep)]
                    # Creates the basic outline of the templateDictionary
                    templateDictionary[dep] = {'text':depText,
                                               'syllables':self.countSyllables(depText),
                                               'compounds':[]}
                    # The first 'compound' is the index of the dependency
                    firstCompound = self.titleDependencies.index(dep)
                    # Start the last compound index at the first compound
                    lastCompound = firstCompound
                    # Finds the last 'compound' word attached to a key 
                    # dependency in the sentence
                    while lastCompound > -1 and self.titleDependencies[lastCompound - 1] in compoundDeps:
                        lastCompound -= 1
                    # Adds each compound in the list to the template dictionary 
                    # under the dependency they modify
                    for compound in self.titleText[lastCompound:firstCompound]:
                        templateDictionary[dep]['compounds'].append((compound, self.countSyllables(compound)))
                # If one of the dependencies in the template isn't in the sentence, 
                # the template doesn't match so break
                else:
                    break
            # If all three dependencies are in the template, add it to the 
            # list of dictionaries
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
                            # Checks to make sure that the word you are trying 
                            # to add comes after the firstCompound in the list
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
        # This checks to see if a word is a acronym like MLK, NASA, etc.
        if not (word.isupper() and len(word) > 1):
            # Check if the word is in the cmudic from nltk
            try:
                # https://stackoverflow.com/questions/405161/
                return [len(list(y for y in x if y[-1].isdigit())) for x in self.cmudic[word.lower()]][0]
            # If it's not in the cmu dic, use the pyphen library instead
            except:
                syllables = 0
                # This accounts for hyphenated words
                for word in word.split('-'):
                    syllables += self.pyphendic.inserted(word).count('-') + 1
                return syllables
        else:
            # If it's a acronym, syllables are the same as the number of chars
            return len(word)
    
    def countPhraseSyllables(self, sentence):
        """
        Requires: sentence is a list of tuples where the second value in the 
        pair is an integer
        Effects: returns total amount of entities of line 
        """
        return sum([word[1] for word in sentence])