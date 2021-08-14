Hi, i separated some. That doesnt mean we cannot pick others tasks.. just for reflect some progress.

Todo(common)
Todo(gscholli)
Todo(poisonedy)
Done(common)


Todo(common):
# add logging
# improve module loading
# improve the errorhandling (esp. main: we have to check if sql works before connecting)



Todo(gscholli):
# improve the errorhandling within the clicker. I'd add a function called proxyinfo or something and then count the time between clicks and write this into the sqliite file and if the proxy times out i'd set him inactive and update the latency as well.. (later the proxychecker script must then check the isactive = 0 proxies
# try to add some usefull loggin
# find the best way to store pics
# improve click detection !!!! (sometimes we unclick the button)
                # //try to do some sleep (microseconds) or try negation. 
# Store clicks in the database

Todo(Poisonedy):
# test proxies as part of the proxy gathering script
# search for a or multiple good list(s) for proxies
Get more proxies :D ( more scrap scripts)
Develop a check proxy function(life, latency/ping, etc)
Database proxy Duplicity handling
# try to scrape or download the proxies (i have added a test cvs-file you can use as framework # we can can manually add the proxies to the database until the scraper is working)


#Done
(done in proxybot, but you can copy to click bot the code if you like it, of course)
Now we call plugins for its name:
hidemiScrap = ProxyBotPlugin.plugins['hidemi']()
(i.e. the file is hidemi.py)
would be good to find generic names as possible, hidemi may be not but instead storeSQLite.py we can name database.py, that would be:
database = ProxyBotPlugin.plugins['database']()

Added some functions to storeSQLite.py:
add data
see all data

now proxybot when run, fills the db. Don't do as it will duplicate registers.




