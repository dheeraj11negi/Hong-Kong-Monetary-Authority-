from scrapinghelp import htmlhelper
import requests
import re
import json
import hashlib
from multiprocessing.pool import ThreadPool as Pool
global newlist
newlist=[]
class crawlData:
    def crawling(mylist,count,check):
        d = {
            "Title": "",
            "Source": "https://www.justice.gov/news",
            "publishedAt": "",
            "URL": "",
            "query": "",
            "uid": "",
            "Content": ""
        }
        newurl=check["url"]
        res=requests.get(newurl)
        print(res,"--",newurl)
        source=htmlhelper.returnformatedhtml(res.text)

        try:
            d["URL"]=newurl
        except:
            pass
        try:
            d["query"]=check["group_name"]
        except:
            pass

        try:

            get_content=htmlhelper.returnvalue(source,"<div class=\"template-content-area\">","</div")
            getarr = htmlhelper.collecturl(get_content, "<p", "</p>")
            mystring = ""

            for tag in getarr:
                cleanr = re.compile('<.*?>')
                cleantext = re.sub(cleanr, '', tag)
                mystring = mystring + cleantext + " "

            if mystring != "":
                mystring = mystring.replace('align=\"justify\">', "").replace('align=\"center\">', "").replace(
                    'align=\"right\">', '')
                mystring = mystring.replace('align=\"justify\"', '').replace('class=\"head\">', '').replace(
                    'align=\"left\"', '').replace('>', '').replace('<', '')
                d["Content"] = mystring

        except:
            pass

        try:
            d["Title"]=check['title']
        except:
            pass

        try:
            d["publishedAt"]=check['date']
        except:
            pass

        try:
            d["uid"] = hashlib.sha256(((d["URL"] + d["Title"]).lower()).encode()).hexdigest()
        except:
            pass
        try:
            newlist.append(d)
            print("------",count)
        except:
            pass

        try:
            if count>=7883:
                with open('hong_kong_news_list.json', 'w', encoding="utf-8") as file:
                    json.dump(newlist, file, ensure_ascii=False, indent=4)
        except:
            pass






