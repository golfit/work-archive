#Quick script to fetch year founded from data on the site
#Ted Golfinopoulos, 25 April 2015

import urllib
from HTMLParser import HTMLParser
import re #Import regular expressions

#url="http://colleges.usnews.rankingsandreviews.com/best-colleges/albion-college-2235"
url="http://colleges.usnews.rankingsandreviews.com/best-colleges/florida-hospital-college-31155"

class MyHtmlParser(HTMLParser) :
    global currentTag
    global yearFoundedFlag
    global collegeName, yearFounded,state,tuition
    currentTag='default'
    yearFoundedFlag=False
    yearFounded='-999'
    collegeName='-999'
    tuition='-999'
    state='-999'

    def handle_starttag(self, tag, attrs) :
        global currentTag
        currentTag=tag
#        if(tag=="span" and len(attrs)>0) : #Data seems to be under these kinds of tags
#            currentTag='span'
#            print("attrs[0]="+str(attrs[0]))
#            if(len(attrs)>=2) :
#                print("attrs[1]="+str(attrs[1]))
#        else :
#             currentTag='other'

    def handle_data(self,data) :
        global currentTag
        global yearFoundedFlag
        global collegeName, yearFounded,state,tuition
        #Look for year founded - if find, record
        if( re.match('\s*Year founded\s*',data) ) :
            yearFoundedFlag=True
        elif(currentTag=='span' and re.match('\s*\d{4,4}\s*',data) and yearFoundedFlag) :
            yearFounded=re.findall('\d{4,4}',data)[0]
#            print('data match, data='+yearFounded)
            yearFoundedFlag=False
        elif( currentTag=='span' and re.match('[A-Z]{2,2}$',data) ) :
            state=str(data)
#            print('state data='+state)
        elif( currentTag=='span' and re.match('\$\d{1,2},\d{3,3}',data) ) :
            tuition=str(data)
#            print('tuition data='+tuition)
        elif( currentTag=='title' and re.match('(.+) | Best College | US News',data) ) :
            collegeName=re.split('\s\|\s',data)[0]
#            print('collegeName='+collegeName)

    def handle_endtag(self, tag) :
        global yearFoundedFlag
        #Negate flag after first span domain is completed.
        if(currentTag=='span') :
            yearFoundedFlag=False
            
    def getData(self) :
        global collegeName, yearFounded,state,tuition
        return (collegeName,yearFounded,state,tuition)
        
myParser=MyHtmlParser()

#myParser.feed(urllib.urlopen(url).read())
#
#myParser.feed(open('albion.txt').read())
try :
    myParser.feed(open('abraham.txt').read().decode('UTF-8'))
except UnicodeDecodeError :
    print('gah')

print("--------------------------")
myData=myParser.getData()
collegeName=myData[0]
yearFounded=myData[1]
state=myData[2]
tuition=myData[3]
print(collegeName+","+yearFounded+","+state+","+re.sub(',','',tuition))

print("Done parsing college pages")



#        if(currentTag=='span') :
#            if(re.match('\s*\d{4,4}\s*',data)) :
#                print("currentTag=span, data="+str(data))
#            elif( re.match('\s*Year founded\s*',data)) :
#                print("yearFoundedFlag, data="+str(data))
#        print(data)
#        print("most recent tag="+str(self.get_starttag_text()))
#        if(self.get_starttag_text()=="span") :
#            print('data='+str(data))
#        print(data)
