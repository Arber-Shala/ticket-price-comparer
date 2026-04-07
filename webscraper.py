from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import random
import undetected_chromedriver as uc
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import os
from fake_useragent import UserAgent # https://pypi.org/project/fake-useragent/
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys

class ScrapePrices():
    '''
    Scrapes price data from websites
    Input: url
    Output: price data
    '''
    def __init__(self, url):
        '''Initializes vaiables to be used in the class'''
        self.driver = ''
        self.list_of_urls = []
        self.website_url = url
        self.path = os.path.dirname(os.path.realpath(__file__)) # current path of folder
    
    def getProxies(self):
        '''gets a list of proxies to access the websites with'''
        # get request from proxies website
        r = requests.get('https://free-proxy-list.net/', verify=True)
        # get HTML soup and search for table
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('tbody')
        total_rows = len(table)
        # get each row of the table and add elite proxies to a proxies.txt file
        with open("proxies.txt", 'w') as file:
            for i, row in enumerate(table):
                if row.find_all('td')[4].text == 'elite proxy' and row.find_all('td')[5].text == 'yes':
                    proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
                    file.write(proxy)
                    # only add newspace if its not the last line 
                    if i < total_rows - 1:
                        file.write('\n')
    
    def setupDriver(self):
        '''creates user agents using proxy ip addresses saved in .txt files'''
        # get list of proxies to use
        proxies = []
        # selenium Options() function used to customize browser behaviour
        options = Options()
        # create user agent
        user_agent = UserAgent() 
        user_string = user_agent.random # creates a random browser
        
        with open("proxies.txt", 'r') as file:
            for line in file:
                proxies.append(line)
                # add proxy IP to the selenium driver
                options.add_argument(f'--proxy-server={line}')
        # enables webscraping without GUI opening
        options.add_argument('--headless')

        # get a random proxy
        random_proxy = random.choice(proxies)

        # define selenium options
        seleniumwire_options = {
            'proxy': {
                'http': f'{random_proxy}',
                'https': f'{random_proxy}',
                'verify_ss1': False
            }
        }
        # define options for google chrome webdriver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'--user-agent={user_string}')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.headless = True

        # add data to final driver to be used
        self.driver = uc.Chrome(options=chrome_options, seleniumwire_options=seleniumwire_options)

    def run(self):
        '''runs functions of ScrapePrices() class'''
        self.getProxies()
        self.setupDriver()
    
if __name__ == "__main__":
    scrape = ScrapePrices("wfwe")

    scrape.run()