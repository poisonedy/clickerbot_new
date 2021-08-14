# Starts the ClickerBotEngine

from plugins import ClickerBotPlugin
import sqlite3
import logging

# Image processing
from PIL import Image
from io import BytesIO

import concurrent.futures



def clicker_worker(plugin, proxy, timeout, no_images, visability_timer):
    logger.debug("entered worker")

    cw = ClickerBotPlugin.plugins[plugin]()
    cw.click(proxy, timeout, no_images, visability_timer)

    before_img = Image.open(BytesIO(cw.before_png)) # uses PIL library to open image in memory
    before_img.save("before-" + str(proxy[0]) + ".webp", optimize=True)
    after_img = Image.open(BytesIO(cw.after_png)) # uses PIL library to open image in memory
    after_img.save("after-" + str(proxy[0]) + ".webp", optimize=True)


logger = logging.getLogger("ClickerBotMain")
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler("./clickerbot/logs/clicker2.log")
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


# 'application' code
# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warn message')
# logger.error('error message')
# logger.critical('critical message')

## SQLite connection
conn = sqlite3.connect('../clickerbot/data/proxies.db')
cursor = conn.cursor()
cursor.execute("SELECT ProxyId, Type, Ip, Port from Proxies WHERE IsActive =1")

threat_num = 5


result = cursor.fetchall()


with concurrent.futures.ThreadPoolExecutor(max_workers=threat_num) as executor:
    for proxy in result:
        future_to_cc = {executor.submit(clicker_worker, "Coinhunt.ccClickerChrome", proxy, 180, 1, 15)}
    for future in concurrent.futures.as_completed(future_to_cc):
        proxy = future_to_cc[future]
        try:
            data = future.result()
        except Exception as exc:

            print('%r generated an exception: %s' % (proxy, exc))
        else:
            print('%r page is %d bytes' % (proxy, len(data)))
    #wait(futures)

#Closing the connection
conn.close()