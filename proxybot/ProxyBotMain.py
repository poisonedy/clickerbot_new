# Starts the ClickerBotEngine
import json

from plugins import ProxyBotPlugin

# initDB - you only have to to this once
db = ProxyBotPlugin.plugins['storeSQLite']("./data/proxies.db")
db.initDB()

hidemiScrap = ProxyBotPlugin.plugins['hidemi']()
proxyObjJson = json.loads(hidemiScrap.printProxyList())

for item in  proxyObjJson:

    print ("adding proxy: " + item['type'] +" " + item['ip'] +" " + item['port'])
    db.addProxy(item['type'], item['ip'], item['port'], "nowhere:D", 1)


