class Haiku(object):
    # Public methods
    def __init__(self, lineOne, lineTwo, lineThree):
        """
        Requires: lineOne, lineTwo, and lineThree are all arrays of strings
        Effects: creates new instance of a haiku
        """
        # Initalizing member variables
        self.lineOneTitle = lineOne['title']
        self.lineTwoTitle = lineTwo['title']
        self.lineThreeTitle = lineThree['title']

        self.lineOneUrl = lineOne['url']
        self.lineTwoUrl = lineTwo['url']
        self.lineThreeUrl = lineThree['url']

    def getScore(self):
        """
        Requires: none
        Effects: returns a score associated with 
        """
        return self.isSameArticle() + self.similarWords()
        
    def getHaiku(self):
        return (' '.join(self.lineOneTitle) + '\n' + ' '.join(self.lineTwoTitle) 
        + '\n' + ' '.join(self.lineThreeTitle) + '\n' + self.lineOneUrl + '\n' 
        + self.lineTwoUrl + '\n' + self.lineThreeUrl + '\n\n')

    # Private methods
    def isSameArticle(self):
        # If any of the articles are the same, we don't want the haiku
        if self.lineOneUrl == self.lineTwoUrl or self.lineOneUrl == self.lineThreeUrl or self.lineTwoUrl == self.lineThreeUrl:
            return -1000
        # If none are the same that's expected, so worth nothing
        return 0
    
    def similarWords(self):
        # Convert the titles to sets
        lineOneSet = set(self.lineOneTitle)
        lineTwoSet = set(self.lineTwoTitle)
        lineThreeSet = set(self.lineThreeTitle)
        # Determines if any words in the lines are the same, adds up the total 
        # and squares it to find the similar words score
        return -(len(lineOneSet & lineTwoSet) + len(lineOneSet & lineThreeSet) + len(lineTwoSet & lineThreeSet))**2