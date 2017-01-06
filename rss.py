import feedparser

class NewsRSS(object):
    
    rss_url = ""
    
    fp = None
    
    def __init__(self,url):
        self.rss_url = url
        self.fp = feedparser.parse(url)
        #print fp
    
    def getHeadlines(self):
        hline = []
        for itm in self.fp.entries:
            hline.append(itm.title)
        
        return hline
    
    def findByHeadline(self,headline):
        
        for itm in self.fp.entries:
            if(headline == itm.title):
                return itm
        return None
    

if __name__ == "__main__":
    nrss = NewsRSS("http://rssfeeds.courierpress.com/courierpress/business&x=1")
    print nrss.getHeadlines()
    print nrss.findByHeadline("Crossroads IGA on North Green River opens Jan. 5")