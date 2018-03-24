#This script is meant to fetch the founding year of US colleges from the US News and World Report list of best colleges
#Ted Golfinopoulos, 22 Apr 2015
import urllib
from lxml import html
from HTMLParser import HTMLParser
import re #Import regular expressions

url = "http://colleges.usnews.rankingsandreviews.com/best-colleges/sitemap"
page = html.fromstring(urllib.urlopen(url).read())

#for link in page.xpath("//a"):
#    print "Name", link.text, "URL", link.get("href")

#for link in page.get_element_by_id("article").xpath("//a") :
#    try:
#        print("Name=" + link.text + ", URL="+link.get("href"))
#    except :
#        print("skipping")
        
#for elem in page.get_element_by_id("article") :
#    for link in elem.xpath("//a") :
#        print(link.text_content())

collegeUrls=list() #Create an empty list object.
class MyHtmlParser(HTMLParser) :
    def handle_starttag(self, tag, attrs) :
        if(tag=="a") : #If link encountered
            if(attrs[0][0]=="href") : #Make sure this is a link
                thisUrl=attrs[0][1] #URL
#                if(re.match("/best-colleges/",thisUrl) \
#                   and re.match("\d{1,5}",thisUrl)) : #If link is to a college, keep
                if(re.match("/best-colleges/",thisUrl) and re.match(".*\d{1,5}",thisUrl)) :
                    print("url="+thisUrl)
                    collegeUrls.append(thisUrl) #Keep the link

parser=MyHtmlParser()
parser.feed(urllib.urlopen(url).read())

print("---------------------------------")
print("Done: found " + str(len(collegeUrls)) + " links")

#Now, access each link and fetch the name of the university, the location, and the year founded
baseUrl='http://colleges.usnews.rankingsandreviews.com'
#for thisUrl in collegeUrls :
#    page = html.fromstring(urllib.urlopen(baseUrl+thisUrl).read()) #Open the new page
    

#class MyHTMLParser(HTMLParser):
#    def handle_starttag(self, tag, attrs):
#        print "Start tag:", tag
#        for attr in attrs:
#            print "     attr:", attr
#    def handle_endtag(self, tag):
#        print "End tag  :", tag
#    def handle_data(self, data):
#        print "Data     :", data
#    def handle_comment(self, data):
#        print "Comment  :", data
#    def handle_entityref(self, name):
#        c = unichr(name2codepoint[name])
#        print "Named ent:", c
#    def handle_charref(self, name):
#        if name.startswith('x'):
#            c = unichr(int(name[1:], 16))
#        else:
#            c = unichr(int(name))
#        print "Num ent  :", c
#    def handle_decl(self, data):
#        print "Decl     :", data
        
#class MyHtmlParser2(HTMLParser) :
#    def handle_starttag(self, tag, attrs) :
#        if( str(tag)=="div" and str(attr[0](0))=="id" and str(attr[0](1))=="article" ) :
#            print(attr[0](0))
#            print(attr[0](1))

#parser = MyHTMLParser()
#parser=MyHtmlParser2()

#parser.feed(urllib.urlopen(url).read())
#parser.feed(page.toString())
