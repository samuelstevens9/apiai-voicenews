import requests
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print "Encountered a start tag:", tag, attrs

    def handle_endtag(self, tag):
        print "Encountered an end tag :", tag

    def handle_data(self, data):
        print "Encountered some data  :", data

#url = "http://www.courierpress.com/story/money/evansville-business-journal/2017/01/10/keeping-books-new-deadlines-out-employer-tax-reporting/95109076/"

def extractCPArticleText(url):

    r = requests.get(url)
    # role="main" itemprop="articleBody"

    #print r.text.encode("utf-8")
    cp_raw_text = r.text.encode("utf-8")
    #parser = MyHTMLParser()
    #parser.feed(cp_raw_text)
    soup = BeautifulSoup(cp_raw_text, 'html.parser')
    articleBody = soup.find(itemprop="articleBody")
    #print articleBody
    #remove div#inline-share-tools-asset
    shareTools = articleBody.find_all("div","inline-share-tools-asset")
    for st in shareTools:
        st.clear();
    scriptsTags = articleBody.find_all("script")
    for sct in scriptsTags:
        sct.clear()
    printTags = articleBody.find_all("div","article-print-url")
    for pt in printTags:
        pt.clear()
    #print articleBody
    return articleBody.get_text().encode("utf-8")

    