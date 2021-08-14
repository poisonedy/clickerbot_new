import requests
import bs4  
import sqlite3
from concurrent.futures import ThreadPoolExecutor, wait
from requests.exceptions import Timeout
from datetime import datetime
# Import math Library
import math 
import hashlib
import json
import re


def clicker_worker(proxy):
        proxy_string = proxy[1].lower() + "://" + proxy[2] + ":" + proxy[3]

        proxy_string = "socks5:127.0.0.1:9050"

        proxies = {
            "http" : proxy_string,
            "https" : proxy_string}

        session = requests.Session()
        session.headers.update({ "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0" })
        base_url = "https://coinhunt.cc"

        #print("Connecting to page via ProxyID " + str(proxy[0]) + " " + proxy_string)
        try:
                text = session.get(base_url,proxies=proxies, timeout=5).text
        except Timeout:
                print("get: ProxyID " + str(proxy[0]) + " The request timed out")
                return 1


        soup = bs4.BeautifulSoup(text, features='html.parser')
        scripts = soup.find_all('script')
        srcs = [link['src'] for link in scripts if 'src' in link.attrs]
        #print(srcs)

        for link in srcs:
                if "main" in link:
                        #print(link)
                        text = requests.get(base_url + link).text
                        #print(text)
                        match = re.search(r'randomKey=\"(.*?)\"', text, re.MULTILINE | re.DOTALL)
                        if match:
                                randomkey = match.group(1)
                                print("RandomKey:" + randomkey)
                                millisec = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)
                                print("Millisec: " + str(millisec))
                                r = math.trunc(millisec / 10000)
                                r = 162209775
                                print("r: " + str(r))
                                string = str(randomkey) + str(r)
                                #print(string)
                                token = hashlib.sha256(string.encode('utf-8')).hexdigest()
                                #token = "376784f1dfb88a3a3c393d871c692529dd0359fe6b6afd3bec621b1f8a5c61e7"

                                headers = {
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
                                    'Accept': 'application/json, text/plain, */*',
                                    'Accept-Language': 'en-US,en;q=0.5',
                                    'Referer': 'https://coinhunt.cc/',
                                    'Origin': 'https://coinhunt.cc',
                                    'Connection': 'keep-alive',
                                    'Pragma': 'no-cache',
                                    'Cache-Control': 'no-cache',
                                }

                                print("Token: " + token)
                                id = "1179153820"
                                try:
                                        response = requests.post("https://api.cnhnt.cc/public/vote/" +id+ "?token=" + str(token), headers=headers,proxies=proxies, timeout=5)
                                except Timeout:
                                        print("get: ProxyID " + str(proxy[0]) + " The request timed out")
                                        return 1
                                print("proxyID: " + str(proxy[0]) +" " + response.text)


## SQLite connection
conn = sqlite3.connect('./data/proxies.db')
cursor = conn.cursor()
cursor.execute("SELECT ProxyId, Type, Ip, Port from Proxies WHERE IsActive = 1")

threat_num = 100
futures = []

i = 1

while True:
    #Fetching 1st row from the table
    result = cursor.fetchmany(threat_num)

    if not result:
        break
    else:
        with ThreadPoolExecutor() as executor:
            for proxy in result:
                #print("for--------")
                #futures.append(executor.submit(coinhunt_worker, proxy, 180, 1, 15))
                futures.append(executor.submit(clicker_worker, proxy))

    wait(futures)

#Closing the connection
conn.close()
