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
import base64
import re
from urllib.parse import urlparse, parse_qs

class ScrapeFlights():
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
        #self.driver = uc.Chrome(options=opts) # use undetected_chromedriver because google blocks default selenium headless


    def extractDatesFromUrl(self, url: str) -> dict:
        """Decodes departure and return dates from the Google Flights tfs parameter."""
        dates = {"outbound": "N/A", "return": "N/A"}
        try:
            params = parse_qs(urlparse(url).query)
            tfs_b64 = params.get("tfs", [""])[0]
            # Pad and decode base64
            padded = tfs_b64 + "=" * (-len(tfs_b64) % 4)
            decoded = base64.urlsafe_b64decode(padded).decode("latin-1")
            # Dates are embedded as YYYY-MM-DD strings
            found = re.findall(r"(\d{4}-\d{2}-\d{2})", decoded)
            if len(found) >= 1:
                dates["outbound"] = found[0]
            if len(found) >= 2:
                dates["return"] = found[1]
        except Exception as e:
            print(f"Could not decode dates from URL: {e}")
        return dates
    
    def getFlights(self):
        '''get each flight from the website'''
        self.driver.get(self.website_url)
        time.sleep(5)  # let it settle
        #==================================================================
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        # print("Page title:", self.driver.title)
        # print("CAD in page:", "CAD" in self.driver.page_source)
        # print("Total <li> tags:", len(soup.find_all("li")))
        # print("Total <div> tags:", len(soup.find_all("div")))
         #==================================================================
        try:
            # wait until page finishes opening before scraping
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "li.pIav2d"))
            )

            #scroll to trigger lazy-loaded results
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # parse the HTML code of the site
            soup = BeautifulSoup(self.driver.page_source, "html.parser")

            # Google Flights wraps each result in a <li> inside ul.Rk10dc
            result_items = soup.select("ul.Rk10dc li")      
    
            # get departure and return dates
            dates = self.extractDatesFromUrl(self.website_url)

            # create list of flight dictionaries
            flights = list()
            
            for item in result_items:
                try:
                    flight = {}

                    flight["title"] = self.driver.title
                    # Price — typically inside a div with class YMlIz or FpEdX
                    price_el = (
                        item.select_one("span[aria-label*='CAD']") or
                        item.select_one("div.FpEdX") or
                        item.select_one("div.YMlIz") or
                        item.select_one("[data-gs] span")
                    )
                    flight["price"] = price_el.get_text(strip=True) if price_el else "N/A"

                    # Airline name
                    airline_el = item.select_one("div.sSHqwe span, span.h1fkLb")
                    flight["airline"] = airline_el.get_text(strip=True) if airline_el else "N/A"

                    # Departure and return dates
                    flight["departure_date"] = dates["outbound"]  # e.g. "2026-12-20"
                    flight["return_date"] = dates["return"] 

                    # Departure and arrival times
                    dep_el = item.select_one("span[aria-label*='Departure time']")
                    arr_el = item.select_one("span[aria-label*='Arrival time']")
                    flight["departure_time"] = dep_el.get_text(strip=True) if dep_el else "N/A"
                    flight["arrival_time"] = arr_el.get_text(strip=True) if arr_el else "N/A"
                    # times = item.select("span.mv1WYe span[jscontroller]")
                    # if len(times) >= 2:
                    #     flight["departure"] = times[0].get_text(strip=True)
                    #     flight["arrival"] = times[1].get_text(strip=True)
                    # else:
                    #     flight["departure"] = flight["arrival"] = "N/A"

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
            self.driver.save_screenshot("debug/debug.png")

            WebDriverWait(self.driver, 5).until(
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
    # pass in URL
    scrape = ScrapeFlights('https://www.google.com/travel/flights/search?tfs=CBwQAhooEgoyMDI2LTEyLTIwagwIAhIIL20vMG5saDdyDAgDEggvbS8wamJzNRooEgoyMDI2LTEyLTMxagwIAxIIL20vMGpiczVyDAgCEggvbS8wbmxoN0ABSAFwAYIBCwj___________8BmAEB&tfu=EgoIABABGAAgAigL&hl=en&gl=ca&curr=CAD')

    flights = scrape.run()
    # printing flight info
    # for i, f in enumerate(flights):
    #     print(f"[{i}] {f['title']} | {f['airline']} | {f['price']} | "
    #           f"{f['departure_date']} → {f['return_date']} | "
    #           f"{f['departure_time']} → {f['arrival_time']} | "
    #           f"{f['duration']} | {f['stops']}")  
    print('title', flights[0]['title'])  
    print('airline', flights[0]['airline'])
    print('price', flights[0]['price'])
    print('departure_date', flights[0]['departure_date'])
    print('return_date', flights[0]['return_date'])
    print('departure_time', flights[0]['departure_time'])
    print('arrival_time', flights[0]['arrival_time'])
    print('duration', flights[0]['duration'])
    print('stops', flights[0]['stops'])

    
    