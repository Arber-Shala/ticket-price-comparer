from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import random
import undetected_chromedriver as uc
# from seleniumwire import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import os
from fake_useragent import UserAgent # https://pypi.org/project/fake-useragent/
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager
from selenium.webdriver.chrome.service import Service
import re

class ScrapePrices():
    '''
    Scrapes price data from websites
    Input: url
    Output: price data
    '''
    def __init__(self, url):
        '''Initializes vaiables to be used in the class'''
        self.driver = ''
        self.proxies = list()
        self.website_url = url
        self.path = os.path.dirname(os.path.realpath(__file__)) # current path of folder
    
    def getProxies(self):
        '''gets a list of proxies to access the websites with'''
        # get request from proxies website
        r = requests.get('https://free-proxy-list.net/', verify=True)
        # get HTML soup and search for table
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('tbody')
        # get each row of the table and add elite proxies to a proxies.txt file
        for i, row in enumerate(table):
            if row.find_all('td')[4].text == 'elite proxy' and row.find_all('td')[5].text == 'yes':
                proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
                self.proxies.append(proxy)
        

    
    def setupDriver(self):
        '''Uses user agents to run a driver on the target url'''
        # create user agent to mimic a web browser
        user_agent = UserAgent() 
        user_string = user_agent.random # creates a random browser

        # get a random proxy
        random_proxy = random.choice(self.proxies)

        opts = Options()
        opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--window-size=1920,1080")
        # opts.add_argument(f"--proxy-server={random_proxy}") # ** using proxy makes scraping much slower
        opts.add_argument(
            f"user-agent={user_string}"
        )
        self.driver = webdriver.Chrome(options=opts)
    def getFlights(self):
        '''get each flight from the website'''
       
        self.driver.get('https://www.google.com/travel/flights/search?tfs=CBwQAhooEgoyMDI2LTEyLTIwagwIAhIIL20vMG5saDdyDAgDEggvbS8wamJzNRooEgoyMDI2LTEyLTMxagwIAxIIL20vMGpiczVyDAgCEggvbS8wbmxoN0ABSAFwAYIBCwj___________8BmAEB&tfu=EgoIABABGAAgAigL&hl=en&gl=ca&curr=CAD')
        time.sleep(5)  # let it settle
        try:
            print("works")

        except:
            # DEBUG: save screenshot and page source to inspect what loaded (CLAUDE)
            self.driver.save_screenshot("debug.png")
            with open("debug.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)

            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "[data-test-id='offer-listing']")
                )
            )
        finally:
            self.driver.close()
    
    def run(self):
        '''runs functions of ScrapePrices() class'''
        self.getProxies()
        self.setupDriver()
        self.getFlights()
 
    
if __name__ == "__main__":
    scrape = ScrapePrices("wfwe")

    results = scrape.run()