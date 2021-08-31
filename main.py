
from scrapinghelp import htmlhelper
import json
from Extract_Data import crawlData
import xlrd
import requests
import json
from datetime import datetime
from scrapinghelp import htmlhelper
import os
import xml.etree.cElementTree as ET
from xml.dom import minidom
import requests
import hashlib
last_updated_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


from multiprocessing.pool import ThreadPool as Pool


if __name__ == "__main__":
      count=10
      mylist=[]

      while(count<=7890):


            #https://www.hkma.gov.hk/eng/news-and-media/press-releases/api?pagesize=100&currentcount=10&year=&month=&categories%5B%5D=all


            url="https://www.hkma.gov.hk/eng/news-and-media/press-releases/api?pagesize=100&currentcount="+str(count)+"&year=&month=&categories%5B%5D=all"

            res=requests.get(url)
            print(res,"--",url)
            mydata=res.json()


            for ele in mydata["data"]:
                  list = {
                        "url": "",
                        "date": "",
                        "title": "",
                        "group_name":""
                  }
                  try:
                        list["date"]=ele["publish_date"]

                  except:
                        pass

                  try:
                        list["title"]=ele["title"]
                  except:
                        pass
                  try:
                        list["url"]="https://www.hkma.gov.hk"+ele["url"]

                  except:
                        pass
                  try:
                        list["group_name"]=ele['group'][0]['name']

                  except:
                        pass

                  try:
                        mylist.append(list)
                  except:
                        pass

            count+=100

      crawlData.crawling(mylist)

      try:
            with open('my_list.json', 'w', encoding="utf-8") as file:
                  json.dump(mylist, file, ensure_ascii=False, indent=4)
      except:
            pass



      filename = "my_list.json"
      file = open(filename, encoding="utf8")
      jsondata = file.read()
      obj = json.loads(jsondata)



      pool_size = 100
      count=1
      pool = Pool(pool_size)
      for check in obj:
            pool.apply_async(crawlData.crawling,(obj,count,check))
            count+=1
      pool.close()
      pool.join()

      tree = ET.ElementTree(file="hongkong_consolidated.xml")
      root = tree.getroot()

      for child in root:
            print(child.tag)
            if child.tag=="INDIVIDUALS":
                  mylist = []
                  for ele in child:
                        d = {
                              "name": "",
                              "uid": "",
                              "alias_name": [],
                              "country": [],
                              "comments": "",
                              "address": [
                                    {
                                          "complete_address": "",
                                          "state": "",
                                          "city": "",
                                          "country": ""
                                    }
                              ],
                              "list_type": "individual",
                              "nns_status": "False",
                              "last_updated": last_updated_string,
                              "individual_details": {
                                    "gender": "",
                                    "date_of_birth": [],
                                    "organisation": ""
                              },
                              "documents": {
                                    "passport": "",
                                    "ssn": ""
                              }
                        }

                        sanction_list = {
                              "sl_authority": "United Nations",
                              "watch_list": "OSFI - United Nations Act Sanctions",
                              "sl_url": "https://www.un.org/securitycouncil/content/un-sc-consolidated-list",
                              "sl_host_country": "United Nation",
                              "sl_type": "Sanction",
                              "sl_source": "United Nations Security Council Consolidated List",
                              "sl_description": "United Nations Security Council Consolidated List"
                        }
                        d["sanction_list"] = sanction_list
                        for findchild in ele:
                              try:
                                    if findchild.tag=="FIRST_NAME":
                                          getfirstname=findchild.text
                                          if getfirstname!="":
                                                d['name']=getfirstname+" "
                                          print('jm')
                              except:
                                    pass

                              try:
                                    if findchild.tag=="SECOND_NAME":
                                          getsecondname=findchild.text
                                          if getsecondname!="":
                                                d['name']=d['name']+getsecondname+" "

                              except:
                                    pass



                              try:
                                    if findchild.tag == "THIRD_NAME":
                                          getthirdname = findchild.text
                                          if getthirdname != "":
                                                d['name'] = d['name'] + getthirdname+" "

                              except:
                                    pass
                              try:
                                    if findchild.tag == "FOURTH_NAME":
                                          getfourthname = findchild.text
                                          if getfourthname != None:
                                                d['name'] = d['name'] + getfourthname+" "

                              except:
                                    pass

                              try:
                                    if findchild.tag=='COMMENTS1':
                                          mycomment=findchild.text
                                          if mycomment!=None:
                                                d["comments"]=mycomment
                              except:
                                    pass

                              try:
                                    if findchild.tag=='INDIVIDUAL_ALIAS':
                                          for go in findchild:
                                                if go.tag=='ALIAS_NAME':
                                                      print("j")
                                                      getalias=go.text
                                                      if getalias!=None:
                                                            d["alias_name"].append(getalias)
                              except:
                                    pass

                              try:
                                    if findchild.tag=="INDIVIDUAL_DOCUMENT":
                                          for aa in findchild:
                                                if aa.tag=='NUMBER':
                                                      getpassnumber=aa.text
                                                      if getpassnumber!="":
                                                            d["documents"]["passport"]=getpassnumber
                              except:
                                    pass

                              try:
                                    if findchild.tag=='INDIVIDUAL_ADDRESS':
                                          for pp in findchild:
                                                if pp.tag=='COUNTRY':
                                                      getcountry=pp.text

                                                      if getcountry!=None:
                                                            d['address'][0]["country"]=getcountry
                              except:
                                    pass


                              try:
                                    if findchild.tag=='DESIGNATION':
                                          for cc in findchild:
                                                if cc.tag=='VALUE':
                                                      getdesig=cc.text
                                                      if getdesig!=None:
                                                            d["individual_details"]["organisation"]=getdesig
                              except:
                                    pass


                              try:
                                    if findchild.tag=='INDIVIDUAL_DATE_OF_BIRTH':
                                          for ddd in findchild:
                                                if ddd.tag=='DATE':
                                                      getdob=ddd.text
                                                      if getdob!=None:
                                                            d["individual_details"]["date_of_birth"].append(getdob)
                              except:
                                    pass
                              try:
                                    if d["address"][0]["complete_address"]=="":
                                          if d['address'][0]["country"]!="":
                                                d["address"][0]["complete_address"]=d['address'][0]["country"]
                                                d['country'].append(d['address'][0]["country"])



                              except:
                                    pass

                              try:
                                    d["uid"] = d["uid"] = hashlib.sha256(
                                          ((d["name"] + d["sanction_list"]["sl_type"]).lower()).encode()).hexdigest()
                              except:
                                    pass

                        try:
                              mylist.append(d)
                              print("kh")
                        except:
                              pass

                  try:
                        with open('hongkong_UN_Individual_list.json', 'w', encoding="utf-8") as file:
                              json.dump(mylist, file, ensure_ascii=False, indent=4)
                  except:
                        pass

            else:
                  mylist = []
                  for check in child:
                        d = {
                              "name": "",
                              "uid": "",
                              "comments": "",
                              "country": [
                                "United Nation"
                              ],
                              "address": [
                                    {
                                          "complete_address": "",
                                          "state": "",
                                          "city": "",
                                          "country": ""
                                    }
                              ],
                              "list_type": "Entity",
                              "nns_status": "False",
                              "last_updated": last_updated_string,
                              "documents": {
                                    "CIN": ""
                              },
                        }

                        sanction_list = {
                              "sl_authority": "United Nations",
                              "sl_url": "https://www.un.org/securitycouncil/content/un-sc-consolidated-list",
                              "sl_host_country": "United Nation",
                              "watch_list": "OSFI - United Nations Act Sanctions",
                              "sl_type": "Sanction",
                              "sl_source": "United Nations Security Council Consolidated List",
                              "sl_description": "United Nations Security Council Consolidated List"
                        }
                        d["sanction_list"] = sanction_list

                        for gochild in check:
                              try:
                                    if gochild.tag=='FIRST_NAME':
                                          getname=gochild.text
                                          if getname!=None:
                                                d['name']=getname
                              except:
                                    pass

                              try:
                                    if gochild.tag == 'COMMENTS1':
                                          mycomment = gochild.text
                                          if mycomment != None:
                                                d["comments"] = mycomment
                              except:
                                    pass

                              try:
                                    if gochild.tag=='ENTITY_ADDRESS':
                                          for gocity in gochild:
                                                if gocity.tag=='CITY':
                                                      getcity=gocity.text
                                                      if getcity!=None:
                                                            d["address"][0]['city']=getcity
                                                            d["address"][0]["complete_address"]=getcity
                                                if gocity.tag=='COUNTRY':
                                                      getcountry=gocity.text
                                                      if getcountry!=None:
                                                            d['address'][0]["country"]=getcountry
                                                            d["address"][0]["complete_address"]=d["address"][0]["complete_address"]+","+getcountry


                              except:
                                    pass

                              try:
                                    if d["address"][0]["complete_address"]=="":
                                          d["address"][0]["complete_address"]="United Nation"

                              except:
                                    pass


                              try:
                                    d["uid"] = d["uid"] = hashlib.sha256(
                                          ((d["name"] + d["sanction_list"]["sl_type"]).lower()).encode()).hexdigest()
                              except:
                                    pass

                        try:
                              mylist.append(d)

                        except:
                              pass
                  try:
                        with open('hongkong_UN_Entity_list.json', 'w', encoding="utf-8") as file:
                              json.dump(mylist, file, ensure_ascii=False, indent=4)
                  except:
                        pass



















































