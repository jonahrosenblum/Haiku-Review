class Article:
    # Public methods
    def __init__(self, sourceName, title, url):
        """
        Requires: sourceName, title, and url are strings
        Effects: creates new instance of article
        """
        self.sourceName = sourceName
        self.title = title
        self.url = url

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
        Requires:
        Effects: returns a list of template objects, each containing the data to a valid sentence
        """

    def generateValidDictionaries(self, templates):
        """
        Requires: none
        Effects: returns list of valid dictionaries
        """


    def generateValidPhrases(self, templateDictionary, syllables):
        """
        Requires: 
        Effects
        """

    def countSyllables(self, word):
        """
        Requires: words is a string (can be a hyphenated word)
        Effects: returns number of syllables in word
        """

