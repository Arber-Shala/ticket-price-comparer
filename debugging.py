'''This script finds candidate HTML containers in the Google Flights website in case the container changes in the future'''

from bs4 import BeautifulSoup
import requests

url = 'https://www.google.com/travel/flights/search?tfs=CBwQAhooEgoyMDI2LTEyLTIwagwIAhIIL20vMG5saDdyDAgDEggvbS8wamJzNRooEgoyMDI2LTEyLTMxagwIAxIIL20vMGpiczVyDAgCEggvbS8wbmxoN0ABSAFwAYIBCwj___________8BmAEB&tfu=EgoIABABGAAgAigL&hl=en&gl=ca&curr=CAD'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

result_items = soup.select("li[data-id]")
# If that's empty too, try these fallbacks in order:
if not result_items:
    result_items = soup.select("li.pIav2d")
if not result_items:
    result_items = soup.select('[jsname="IWWDBc"] li')
if not result_items:
    result_items = soup.select("ol li")  # Google sometimes uses ol not ul

# Check what list containers exist on the page
for tag in ["ul", "ol"]:
    lists = soup.find_all(tag)
    for l in lists:
        classes = l.get("class", [])
        children = len(l.find_all("li"))
        if children > 2:  # likely a results list, not a nav menu
            print(f"<{tag}> class={classes} → {children} <li> children")    