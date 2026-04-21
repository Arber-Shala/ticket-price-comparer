'''This script gathers username and password credentials for user to login into created database'''
import json

# define login credentials dictionary as head of login part of .json file
login_credentials = dict()

# get user name and password
username = input("username: ")
password = input("password: ")
port_number = input("port number: ") 

# store data in a dictionary
data = {"username": username, "password": password, "port_number": port_number}

# add data to "login" section of .json file
login_credentials["login"] = data

# dump data dict into settings.json file
with open("settings.json", "w") as file:
    json.dump(login_credentials, file)