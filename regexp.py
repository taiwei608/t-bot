import re

class REMatcher(object):
    def __init__(self, matchstring):
        self.matchstring = matchstring

    def match(self,regexp):
     
        try:
            self.rematch = re.match(regexp, self.matchstring, re.I)
            return bool(self.rematch)
        except Exception, e:
            print "Regex has error"
            print e
    def finditer(self,regexp):

        try:
            self.refinditer = re.finditer(regexp, self.matchstring, re.I)
            return self.refinditer
        except Exception, e:
            print "Regex has error"
            print e

    def group(self,i):
        return self.rematch.group(i)
