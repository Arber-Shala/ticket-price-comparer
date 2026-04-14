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
        # self.driver = webdriver.Chrome(options=opts)
        self.driver = uc.Chrome(options=opts) # use undetected_chromedriver because google blocks default selenium headless

    def getFlights(self):
        '''get each flight from the website'''
       
        self.driver.get('https://www.google.com/travel/flights/search?tfs=CBwQAhooEgoyMDI2LTEyLTIwagwIAhIIL20vMG5saDdyDAgDEggvbS8wamJzNRooEgoyMDI2LTEyLTMxagwIAxIIL20vMGpiczVyDAgCEggvbS8wbmxoN0ABSAFwAYIBCwj___________8BmAEB&tfu=EgoIABABGAAgAigL&hl=en&gl=ca&curr=CAD')
        time.sleep(5)  # let it settle
        #==================================================================
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        print("Page title:", self.driver.title)
        print("CAD in page:", "CAD" in self.driver.page_source)
        print("Total <li> tags:", len(soup.find_all("li")))
        print("Total <div> tags:", len(soup.find_all("div")))
         #==================================================================
        try:
            # wait until page finishes opening before scraping
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "li.pIav2d"))
            )
            time.sleep(5)  # let remaining results render

            # scroll to trigger lazy-loaded results
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # parse the HTML code of the site
            soup = BeautifulSoup(self.driver.page_source, "html.parser")

            # Google Flights wraps each result in a <li> inside ul.Rk10dc
            result_items = soup.select("ul.Rk10dc li")      
              
            # create list of flight dictionaries
            flights = list()
            
            for item in result_items:
                try:
                    flight = {}

                    # Price — typically inside a div with class YMlIz or FpEdX
                    price_el = item.select_one("div.YMlIz span, div.FpEdX span")
                    flight["price"] = price_el.get_text(strip=True) if price_el else "N/A"

                    # Airline name
                    airline_el = item.select_one("div.sSHqwe span, span.h1fkLb")
                    flight["airline"] = airline_el.get_text(strip=True) if airline_el else "N/A"

                    # Departure and arrival times
                    times = item.select("span.mv1WYe span[jscontroller]")
                    if len(times) >= 2:
                        flight["departure"] = times[0].get_text(strip=True)
                        flight["arrival"] = times[1].get_text(strip=True)
                    else:
                        flight["departure"] = flight["arrival"] = "N/A"

                    # Duration
                    duration_el = item.select_one("div.Ak5kof div, span.pIgMWd")
                    flight["duration"] = duration_el.get_text(strip=True) if duration_el else "N/A"

                    # Stops
                    stops_el = item.select_one("div.EfT7Ae span, span.ogfYpf")
                    flight["stops"] = stops_el.get_text(strip=True) if stops_el else "N/A"

                    # Only append if we found at least a price
                    if flight["price"] != "N/A":
                        flights.append(flight)

                except Exception as e:
                    print(f"Skipping a result due to parse error: {e}")
                    continue

                return flights

        except:
            # DEBUG: save screenshot and page source to inspect what loaded (CLAUDE)
            print("Timed out waiting for results. Page may not have loaded.")
            self.driver.save_screenshot("debug.png")

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
        flights = self.getFlights()

        return flights
    
if __name__ == "__main__":
    scrape = ScrapePrices("wfwe")

    flights = scrape.run()

    # printing flight info
    for i, f in enumerate(flights, 1):
        print(f"[{i}] {f['airline']} | {f['price']} | "
              f"{f['departure']} → {f['arrival']} | "
              f"{f['duration']} | {f['stops']}")    