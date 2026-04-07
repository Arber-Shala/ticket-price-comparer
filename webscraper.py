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
from fake_useragent import UserAgent
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
        r = requests.get('https://free-proxy-list.net/', verify=True)
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('tbody')
        total_rows = len(table)
        with open("proxies.txt", 'w') as file:
            for i, row in enumerate(table):
                if row.find_all('td')[4].text == 'elite proxy' and row.find_all('td')[5].text == 'yes':
                    proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
                    file.write(proxy)
                    if i < total_rows - 1:
                        file.write('\n')
    
    def run(self):
        '''runs functions of ScrapePrices() class'''
        self.getProxies()
    
if __name__ == "__main__":
    scrape = ScrapePrices("wfwe")

    scrape.run()