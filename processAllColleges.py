#This script is meant to fetch the founding year of US colleges from the US News and World Report list of best colleges
#Ted Golfinopoulos, 26 Apr 2015
import urllib
from HTMLParser import HTMLParser
import re #Import regular expressions

url = "http://colleges.usnews.rankingsandreviews.com/best-colleges/sitemap"

collegeUrls=list() #Create an empty list object.
class MyHtmlParser(HTMLParser) :
    def handle_starttag(self, tag, attrs) :
        if(tag=="a") : #If link encountered
            if(attrs[0][0]=="href") : #Make sure this is a link
                thisUrl=attrs[0][1] #URL
                if(re.match("/best-colleges/",thisUrl) \
                   and re.match(".*\d{1,5}",thisUrl)) : #If link is to a college, keep
#                    print("url="+thisUrl)
                    collegeUrls.append(thisUrl) #Keep the link

parser=MyHtmlParser()
#parser.feed(urllib.urlopen(url,'r').read())
parser.feed(open('collegeSiteMap.txt','r').read().decode('UTF-8'))

print("---------------------------------")
print("Done: found " + str(len(collegeUrls)) + " links")

#Now, access each link and fetch the name of the university, the location, and the year founded
class MyCollegeParser(HTMLParser) :
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

    def handle_data(self,data) :
        global currentTag
        global yearFoundedFlag
        global collegeName, yearFounded,state,tuition
        #Look for year founded - if find, record
        if( re.match('\s*Year founded\s*',data) ) :
            yearFoundedFlag=True
        elif(currentTag=='span' and re.match('\s*\d{4,4}\s*',data) and yearFoundedFlag) :
            yearFounded=re.findall('\d{4,4}',data)[0]
            yearFoundedFlag=False
        elif( currentTag=='span' and re.match('[A-Z]{2,2}$',data) ) :
            state=str(data)
        elif( currentTag=='span' and re.match('\$\d{1,2},\d{3,3}',data) ) :
            tuition=str(data)
        elif( currentTag=='title' and re.match('(.+) | Best College | US News',data) ) :
            collegeName=re.split('\s\|\s',data)[0]

    def handle_endtag(self, tag) :
        global yearFoundedFlag
        #Negate flag after first span domain is completed.
        if(currentTag=='span') :
            yearFoundedFlag=False
            
    def getData(self) :
        global collegeName, yearFounded,state,tuition
        return (collegeName,yearFounded,state,tuition)

baseUrl='http://colleges.usnews.rankingsandreviews.com'
myParser=MyCollegeParser()
outputFile=open('allCollegesData3.txt','w') #Output file in which to store data, csv.
outputStr="College Name,Year Founded,State,Max. Tuition" #Record order of data.
outputFile.write(outputStr+'\n')
print(outputStr)    

for thisUrl in collegeUrls :
    try :
        myParser.feed(urllib.urlopen(baseUrl+thisUrl,'r').read().decode('UTF-8'))
        myData=myParser.getData()
        collegeName=myData[0]
        yearFounded=myData[1]
        state=myData[2]
        tuition=myData[3]
        outputStr=collegeName+","+yearFounded+","+state+","+re.sub(',','',tuition)
        outputFile.write(outputStr+'\n') #Write data to file
        print(outputStr) #Write to standard out, too.
    except :
        print("Could not handle "+str(thisUrl)+" --- skipping")

outputFile.close()

print("---------------------------------")
print("Done processing colleges")
