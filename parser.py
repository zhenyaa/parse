from bs4 import BeautifulSoup
import re
from lxml import etree
import sys
import itertools
# print(sys.argv[1:])

def xpath_soup(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:  # type: bs4.element.Tag
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name if 1 == len(siblings) else '%s[%d]' % (
                child.name,
                next(i for i, s in enumerate(siblings, 1) if s is child)
                )
            )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)

class PatternHTML(object):
    _patternID = "make-everything-ok-button"
    _patternText = ''
    _patternElem = 0
    _patternAttrsDickt =  dict()
    _htmlTitle = BeautifulSoup(open("sample-0-origin.html"), 'html.parser')

    def __init__(self, patternID=None, htmladre=None):
        self._htmlTitle = BeautifulSoup(open(htmladre), 'html.parser')
        self._patternID = patternID

    def setPatternIDElem(self):
        try:
            self._patternElem = self._htmlTitle.find("a", { "id" : self._patternID})
            self._patternText = self._htmlTitle.find("a", { "id" : self._patternID}).text
        except:
            return "Elem by id not found"

    def setPatternAttrs(self):
        self._patternAttrsDickt = self._patternElem.attrs

class TestingHTML(object):
    _namePattern = re.compile('Make Everything OK Area')
    _testdata = re.compile('Make everything OK')
    _htmlPatch = "sample-1-evil-gemini.html"
    _testingHTML = BeautifulSoup(open(_htmlPatch), 'html.parser')
    _listOfMatch = list()
    _listOfAttrs = list()
    _parentObj = object

    def __init__(self, htmlAddr=None, parentObj=None):
        if htmlAddr is not None:
            self._htmlPatch = htmlAddr
            self._testingHTML = BeautifulSoup(open(htmlAddr), 'html.parser')
            self._parentObj = parentObj

    def getTest(self):
        c = 0
        c = self._testingHTML.find('a', text=self._testdata, attrs=self._parentObj._patternAttrsDickt)
        if not c:
            c =  self._testingHTML.find('a', text=self._testdata)
        if not c:
            self._testingHTML.find('a', attrs=self._parentObj._patternAttrsDickt)
        return c

# patternHTML = PatternHTML()
# patternHTML.setPatternIDElem()
# patternHTML.setPatternAttrs()

c = ['sample-0-origin.html', 'sample-1-evil-gemini.html', 'sample-2-container-and-clone.html', 'sample-3-the-escape.html', 'sample-4-the-mash.html' ]



# for x in c:
#     testHTML = TestingHTML(x, patternHTML)
#     print(xpath_soup(testHTML.getTest()))

patternHtml = PatternHTML(patternID=None, htmladre=sys.argv[1])
patternHtml.setPatternIDElem()
patternHtml.setPatternAttrs()
testingHtml = TestingHTML(htmlAddr=sys.argv[2], parentObj=patternHtml)


print(xpath_soup(testingHtml.getTest()))