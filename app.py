#!/usr/bin/env python

import urllib, json, os,re, random

from flask import Flask
from flask import request
from flask import make_response
from flask import Markup
from rss import NewsRSS
from crawler import extractCPArticleText
# Flask app should start in global layout
app = Flask(__name__)

@app.route("/",methods=['GET'])
def main():
    
    iframe = '<iframe width="350" height="430" src="https://console.api.ai/api-client/demo/embedded/thebible"></iframe>'
    return make_response('<!DOCTYPE html><html><head><title>The Bible</title></head><body>'+iframe+'</body></html>')

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))
    
    
    
    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    try:
        nrss = NewsRSS("http://rssfeeds.courierpress.com/courierpress/business&x=1")
        ai_action = req.get("result").get("action")
        if(ai_action == "read.headline_article"):
            headine = req.get("result").get("parameters").get("headline")
            itm = nrss.findByHeadline(headine)
            #summary_detail.value
            #summary
            articleText = extractCPArticleText(itm['link'])
            #cleanSummary = cleanPassage(itm['summary'])
            return makeDefaultResponse(articleText,headine)
        if(ai_action == "read.section_headlines"):
            headlines = nrss.getHeadlines()
            return makeDefaultResponse(headlines[0],headlines[0])
        #print nrss.findByHeadline("Crossroads IGA on North Green River opens Jan. 5")
        
        
        return makeDefaultResponse()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print "ERROR!",e
        print "FINISHED TASKS"
        return makeDefaultResponse()





        

def cleanPassage(passage_raw):
    passage_html = passage_raw.encode('ascii', 'ignore').decode('ascii')
    #remove the heading
    #print passage_html
    #heading_regex = r'<h3.*?>.*?</h3>'
    #passage_html = re.sub(heading_regex,"",passage_html,1)
    #print passage_html
    #remove first vers number 
    #verse_num_regex = r'<sup.*?>\d+</sup>'
    #passage_html = re.sub(verse_num_regex,"",passage_html,1)
    #print passage_html
    passage_txt = Markup(passage_html).striptags()
    return passage_txt

def makeDefaultResponse(other_resp=None,headline=None):
    if(not other_resp):
        other_resp = "I didn't understand."
    
    print (other_resp.encode("utf-8"))
    return {
        "speech": other_resp,
        "displayText": other_resp,
        # "data": data,
        "contextOut": [{"name":"reading_headlines", "lifespan":5, "parameters":{"headline":headline}}],
        "source": "apiai-voicenews"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
