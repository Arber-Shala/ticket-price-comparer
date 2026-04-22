'''This script gathers username and password credentials for user to login into created database'''
import json
from dotenv import load_dotenv
import os

# get username and password for user login
username = input("username: ")
password = input("password: ")
port_number = input("port number: ") 

# define login credentials dictionary as head of any login information for this app
login_credentials = dict()

# store data in a dictionary
data = {"username": username, "password": password, "port_number": port_number}

# add data to "login" section of .json file
login_credentials["ticket-price-comparer"] = data

# get default credentials from .env file to connect to postgres database
username = os.getenv("DB_DEFAULT_USERNAME")
password = os.getenv("DB_DEFAULT_PASSWORD")
port = os.getenv("DB_DEFAULT_PORT")
data = {"username": username, "password": password, port: port}
login_credentials["default"] = data

# dump data dict into settings.json file
with open("settings.json", "w") as file:
    json.dump(login_credentials, file)