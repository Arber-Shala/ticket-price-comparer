'''This script imports raw data from webscraper into database'''
import psycopg2
import json
from create_database import connect_to_server, get_credentials
from webscraper import ScrapeFlights

# username, password, port = get_credentials("ticket-price-comparer")
username, password, port = get_credentials() # use default login for now until webapp is ready to get users properly

# connect to the ticket_price_comparer database
connection = connect_to_server(username, password, port, "ticket_price_comparer")

cursor = connection.cursor()
connection.autocommit = True
