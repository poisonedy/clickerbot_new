import requests
import re
from bs4 import BeautifulSoup
import json
import plugins


class hydemi(plugins.ProxyBotPlugin):

    def __init__(self, url = "https://hidemy.name/", suburl = "de/proxy-list/", headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',}):
        self.url = url
        self.headers = headers
        self.session = requests.session()
        self.suburl = suburl
        self.proxyPages = []
        self.proxyList = []
        self.getProxyPages()
        self.fillProxyListWithProxyPages()

    def getProxyPages (self):
        self.myurlis = self.url + self.suburl
        self.tempProxyPages=[]
        self.r = self.session.get(self.myurlis, headers=self.headers)
        self.soup = BeautifulSoup(self.r.text, "html.parser")
        #print ("Getting pages list... hold on")
        
        for link in self.soup.find_all('a'):
            self.linkget = link.get('href')
            if self.linkget not in self.proxyPages:
                if '/de/proxy-list/' in self.linkget and 'countries' not in self.linkget and '#list' in self.linkget:
                
                    self.tempProxyPages.append(self.linkget)
                    #print(linkget)
        self.lastpages = []
        self.tempProxyPages = list(set(self.tempProxyPages))
        #print (mylist)
        for item in self.tempProxyPages:
            self.mynum = re.findall(r'/de/proxy-list/start=(.*?)#list',item)
            if self.mynum != []:
                if self.mynum[0] not in self.lastpages:
                    self.lastpages.append(int(self.mynum[0]))
            
        #print (self.lastpages)

        self.maxpage = 0
        for page in self.lastpages:
            if page > self.maxpage:
                self.maxpage = page
        
        start = 64
        while start != self.maxpage:
            self.proxyPages.append('/de/proxy-list/?start=' + str(start))
            start = start + 64
        self.proxyPages.append('/de/proxy-list/')
        #print ("Process finished.")
        return 0
            

    def printProxyPages (self):
        print (self.proxyPages)

    def printProxyList (self):
        return json.dumps(self.proxyList, indent=4)

    def getProxiesFromPage ( self, suburl):
        self.suburl = suburl
        self.myurrl = self.url + self.suburl

        
        
        self.res = self.session.get(self.myurrl, headers=self.headers)
        self.soupz = BeautifulSoup(self.res.text, "html.parser")
        oneproxyavoid = 0
        for oneproxy in self.soupz.find_all('tr'):
            if oneproxyavoid > 0:
                 #print (oneproxy)
                counter = 0
                self.ip = 0
                for td in oneproxy.find('td').parent.find_all('td'):
                    if counter == 0 and "IP" not in td.text:
                        self.ip = td.text
                    elif counter == 1:
                        self.port = td.text
                    elif counter == 4:
                        self.type = td.text
                    
                    counter = counter + 1
                    #print(counter)
                #print ("Proxy added. Ip is:", self.ip, "port is:" , self.port, "Type is:", self.type)
                self.proxyList.append({"ip": self.ip, "port" : self.port, "type": self.type})


            
            oneproxyavoid = oneproxyavoid + 1
        #return self.proxyTempList[0]
                
        
    def fillProxyListWithProxyPages(self):
        #print ("getting proxies for each page")
        for proxypage in self.proxyPages:
            proxiesDump = self.getProxiesFromPage(proxypage)
            if proxiesDump != None:
                self.proxyList.append (proxiesDump)

        
    def countHowMuchProxies (self):
        counter = 0
        for item in self.proxyList:
            counter = counter + 1
        
        print (counter)

           

