class Haiku(object):
    # Public methods
    def __init__(self, lineOne, lineTwo, lineThree, recentlyUsedLinks):
        """
        Requires: lineOne, lineTwo, and lineThree are all arrays of strings
        Effects: creates new instance of a Haiku
        """
        # Initalizing member variables
        # A list of all urls of recently tweeted Haikus
        self.recentlyUsedLinks = recentlyUsedLinks
        # The sentence itself, all lists of strings
        self.lineOneTitle = lineOne['title']
        self.lineTwoTitle = lineTwo['title']
        self.lineThreeTitle = lineThree['title']
        # The urls the article comes from as a string
        self.lineOneUrl = lineOne['url']
        self.lineTwoUrl = lineTwo['url']
        self.lineThreeUrl = lineThree['url']
        # The name of the news source that the article comes from as a string
        self.lineOneSource = lineOne['source']
        self.lineTwoSource = lineTwo['source']
        self.lineThreeSource = lineThree['source']
        # The number of recognized entities in the sentence as an int
        self.lineOneEntCount = lineOne['entCount']
        self.lineTwoEntCount = lineTwo['entCount']
        self.lineThreeEntCount = lineThree['entCount']

    def getScore(self):
        """
        Requires: none
        Effects: returns a score associated with the Haiku that considers
        how similar the lines are, where the source is from, if the article has 
        been tweeted recently,and how many entities are found.
        """
        return (self.isUnique() + self.similarWords() 
                + self.similarSources() + self.countEntities())

    def getHaikuText(self):
        """
        Requires: none
        Effects: returns a string containing lots of information about the Haiku
        for debugging purposes
        """
        return (' '.join(self.lineOneTitle).title() + '\n' + ' '.join(self.lineTwoTitle).title()
        + '\n' + ' '.join(self.lineThreeTitle).title() + '\n\n' + self.lineOneUrl + '\n' 
        + self.lineTwoUrl + '\n' + self.lineThreeUrl)
        
    def debugHaiku(self):
        """
        Requires: none
        Effects: returns a string containing lots of information about the Haiku
        for debugging purposes
        """
        return (' '.join(self.lineOneTitle).title() + '\n' + ' '.join(self.lineTwoTitle).title()
        + '\n' + ' '.join(self.lineThreeTitle).title() + '\n' + self.lineOneUrl + '\n' 
        + self.lineTwoUrl + '\n' + self.lineThreeUrl + '\n' + 
        'sameArticle Score: ' + str(self.isUnique()) + '\n' +
        'similarWords Score: ' + str(self.similarWords()) + '\n' +
        'similarSources Score: ' + str(self.similarSources()) + '\n' +
        'countEntitites: ' + str(self.countEntities()) + '\n' +
        'lineOne Count: ' + str(self.lineOneEntCount) + '\n' +
        'lineTwo Count: ' + str(self.lineTwoEntCount) + '\n' +
        'lineThree Count: ' + str(self.lineThreeEntCount) + '\n' +
        'TOTAL SCORE: ' + str(self.getScore()) + '\n\n')

    # Private methods
    def isUnique(self):
        """
        Requires: none
        Effects: Checks the 'uniqueness' of the haiku. A Haiku is unique if:
        - None of the lines in the Haiku come from the same article (same url)
        - None of the lines in the Haiku come from a recently used article,
        meaning that another Haiku that was recently tweeted used the same article
        If both of those conditions are met, it returns 0, because this is
        what we expect in a good Haiku. If they are not met, -1000 is returned
        because we do not want this Haiku ever.
        """
        currentSources = [self.lineOneUrl, self.lineTwoUrl, self.lineThreeUrl]
        # If any of the articles are the same, we don't want the Haiku
        if (len(set(currentSources)) < len(currentSources) or any(source in self.recentlyUsedLinks for source in currentSources)):
            # This is basically adding 'negative infinity' to the score
            return -1000
        # If none are the same that's expected, so add 0 to the score
        return 0
    
    def similarWords(self):
        """
        Requires: none
        Effects: turns each headline into a set, and checks for intersections
        between all headlines. We ideally want three headlines about different
        things, so if story topics are repeated we dock that Haiku. The result
        is squared to reflect that a lot of similar words is extremely bad
        whereas one is not ideal but allowable.
        """
        # Convert the titles to sets
        lineOneSet = set(self.lineOneTitle)
        lineTwoSet = set(self.lineTwoTitle)
        lineThreeSet = set(self.lineThreeTitle)
        # Determines if any words in the lines are the same, adds up the total 
        # and squares it to find the similar words score
        return -(len(lineOneSet & lineTwoSet) + len(lineOneSet & lineThreeSet) + len(lineTwoSet & lineThreeSet)) ** 2
    
    def similarSources(self):
        """
        Requires: none
        Effects: Checks if the headlines are from the same news source and 
        returns a negative number that reflects that overlap. We want a variety 
        of news sources and stories so this docks points from Haikus that use 
        the same source.
        """
        # Count how many sources are the same, square that result and make it negative
        return -((self.lineOneSource == self.lineTwoSource) + (self.lineOneSource == self.lineThreeSource) + (self.lineTwoSource == self.lineThreeSource)) * 5

    
    def countEntities(self):
        """
        Requires: none
        Effects: Returns the number of entities together in a compiled score that
        tells us how much 'stuff' is happening in the news headlines. Shorter
        syllable headlines have fewer words on average so them having more
        'stuff' is important, thus the score for them is doubled.
        """
        return ((2 * self.lineOneEntCount) + self.lineTwoEntCount + (2 * self.lineThreeEntCount)) 
        
            