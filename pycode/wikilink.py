#!/usr/bin/python

import urllib
import simplejson
import sys
from xml.dom.minidom import parseString

FORMAT="xml" # or "json"
LIMIT = 5

def searchWiki(prevlinks, des_title):
    print "-----src: "+prevlinks[-1]+"-----"
    print "des: "+des_title+"\nprev: "
    print prevlinks


    src_url = prevlinks[-1].strip('"').replace(' ','%20')
    des_url = des_title.strip('"').replace(' ','%20')
    out_link = ("http://en.wikipedia.org/w/api.php?"
                  "format=%s"
                  "&action=query"
                    "&titles=%s"
                    "&prop=links|categories"
                    "&pllimit=500" % (FORMAT, src_url))
    in_link = ("http://en.wikipedia.org/w/api.php?"
                  "format=%s"
                  "&action=query"
                    "&list=backlinks"
                    "&bltitle=%s"
                    "&bllimit=500" % (FORMAT, des_url))

    retstr = urllib.urlopen(out_link.encode('utf-8'))
    links = []

    #############################
    # Extract links in the page #
    #############################
    if FORMAT == "json":
        cate = []
        data = simplejson.loads(retstr.read())
        retstr.close()
        for k, v in data["query"]["pages"].items():
            print "Page ID %s: " % k
            for link in v["links"]:
                links.append(link["title"])
            for cat in v["categories"]:
                cate.append(cat["title"])

    else: #FORMAT == "xml"
        dom = parseString(retstr.read())
        pls = dom.getElementsByTagName('pl')
        for pl in pls:
            if(pl.getAttribute('ns') == '0'):
                links.append(pl.getAttribute('title'))

    #########################################
    # recursively search for the dest topic #
    #########################################
    if des_title in links:
        result = "The link is found!\n  "
        for l in prevlinks:
            result += "[%s]-->" % l
        result += '['+des_title+']'
        print result
        return True

    elif len(prevlinks) < LIMIT:
        for link in links:
            if link in prevlinks:
                continue
            templist = prevlinks+[link]
            if searchWiki(templist,des_title):
                return True
        return False



if __name__ == '__main__':
    prev = []
    prev.append(sys.argv[1])
    searchWiki(prev, sys.argv[2])

