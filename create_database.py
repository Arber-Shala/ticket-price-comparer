'''This script creates a postgreSQL database to hold the price data'''
import psycopg2
import json

# fetch information with login credentials from .json file
with open('settings.json', 'r') as file:
    data = json.load(file)

# access login credentials section of .json file
try:
    credentials = data["login"]

    # get username and password
    username = credentials["username"]
    password = credentials["password"]
    port_number = credentials["port_number"]
except:
    print("No login credentials, please login first")

# connect to postgreSQL database
conn = psycopg2.connect(
   database = "ticket-price-comparer",
    user = username,
    password = password,
    host = 'localhost',
    port = port_number
)