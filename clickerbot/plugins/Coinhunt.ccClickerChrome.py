import plugins
import sys
import time
import datetime
import logging

# Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CoinhuntChromePlugin(plugins.ClickerBotPlugin):
    def __init__(self):
        self.logger = logging.getLogger('Coinhunt.cc-module')
        self.logger.error("creating an instance of CoinhuntChromePlugin")

    def click(self, proxy, timeout = 60, no_images = 1, visability_timer = 1):
        self.logger = logging.getLogger('Coinhunt.cc-module')

        click_success = False
        proxy_string = proxy[1].lower() + "://" + proxy[2] + ":" + proxy[3]

        #proxy_string = "socks5://127.0.0.1:9050"
       # proxy_string = "socks5://127.0.0.1:8888"

        self.logger.info("Coinhunt.cc Plugin: Clicking with ProxyID " + str(proxy[0]) + " URL: " + proxy_string)

        # initialize Selenium Chrome options
        chrome_options = webdriver.ChromeOptions()

        # Set proxy
        chrome_options.add_argument('--proxy-server=%s' % proxy_string)

        if no_images == 1:
            # Disable image loading for more speed
            prefs = {"profile.managed_default_content_settings.images": 2}
            chrome_options.add_experimental_option("prefs",prefs)
        
        if visability_timer <= 1:
            # use chrome headless
            chrome_options.add_argument("--headless")

        # Start the driver
        with webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=chrome_options) as driver:
            # Open URL
            driver.get("https://coinhunt.cc")

            # Setup wait timer
            wait = WebDriverWait(driver, timeout)

            # Initial loading of the page and waiting for the search button
            # check how log it takes until button appears
            start_time = datetime.datetime.now()
            wait.until(EC.presence_of_element_located((By.XPATH, "(//button[@type=\'button\'])[7]")))
            elapsed_time = datetime.datetime.now() - start_time
            self.logger.info("Approximate latency in ms: " + str(elapsed_time.microseconds / 1000))
            driver.find_element(By.XPATH, "(//button[@type=\'button\'])[7]").click()

            # Wait until search field apprears, click into it and type "sweets"
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fade:nth-child(2) .form-control")))
            driver.find_element(By.CSS_SELECTOR, ".fade:nth-child(2) .form-control").click()
            driver.find_element(By.CSS_SELECTOR, ".fade:nth-child(2) .form-control").send_keys("sweets")

            # check and click vote button
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fade:nth-child(2) .Landing_VoteIcon__11KB_")))

            current_button_color = driver.find_element(By.CSS_SELECTOR, ".fade:nth-child(2) .Landing_VoteButton__2MKx0").value_of_css_property("background-color")
            self.logger.debug(current_button_color)
            self.before_png = driver.get_screenshot_as_png() # save before screenshot

            if current_button_color == "rgba(0, 0, 0, 0)":
                self.logger.debug("Vote button not yet clicked")
                driver.find_element(By.CSS_SELECTOR, ".fade:nth-child(2) .Landing_VoteIcon__11KB_").click()
                #time.sleep(30)
                self.after_png = driver.get_screenshot_as_png()
                current_button_color = driver.find_element(By.CSS_SELECTOR, ".fade:nth-child(2) .Landing_VoteButton__2MKx0").value_of_css_property("background-color")
                self.logger.debug(current_button_color)

                if current_button_color != "rgba(rgba(0, 0, 0, 0)":
                    self.logger.info("Vote button click successful")
                    click_success = True
                else:
                    self.logger.info("Vote button click *not* successful")
            else:
                self.logger.info("Vote button already clicked")
                #time.sleep(30)

        # keep windows open if visability timer is larger than 1
        if visability_timer >= 1:
            time.sleep(visability_timer)