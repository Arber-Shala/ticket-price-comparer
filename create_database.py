'''This script creates a postgreSQL database to hold the price data'''
import psycopg2
import json

def get_credentials(database_name = "default"):
    # fetch information with login credentials from .json file
    with open('settings.json', 'r') as file:
        data = json.load(file)

    # access login credentials section of .json file
    try:
        credentials = data[database_name]
    
        # get username and password
        username = credentials["username"]
        password = credentials["password"]
        port_number = credentials["port_number"]
    except:
        print("No login credentials, please login first")
    return username, password, port_number

def connect_to_server(username, password, port_number, db_name = "postgres"):
    # Connect to postgreSQL database
    connection = psycopg2.connect(
        host="localhost",
        port=port_number,
        dbname=db_name,       # connect to default db to create a new one
        user=username,
        password=password
    )

    return connection

if __name__ == "__main__":
    # get credentials and create connection
    username, password, port_number = get_credentials()
    connection = connect_to_server(username, password, port_number)

    # create the database
    cursor = connection.cursor()
    connection.autocommit = True
    try:
        cursor.execute(
        "CREATE DATABASE ticket_price_comparer;")
    except:
        print("'ticket_price_comparer' database already exists")

    cursor.close()
    connection.close()
