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

try: 
    cursor.execute( 
        """ 
            INSERT INTO flights (title, airline, price, departure_date, return_date, departure_time, arrival_time, duration, stops)
            VALUES (flights[0]['title'], flights[0]['airline']), flights[0]['price'], flights[0]['departure_date'], )
        """
    )
except Exception as error:
    print(f"Error while fetching data: {error}")

finally:
    # close the cursor and connection when done
    if cursor:
        cursor.close()
    if connection:
        connection.close()

'''
    print('title', flights[0]['title'])  
    print('airline', flights[0]['airline'])
    print('price', flights[0]['price'])
    print('departure_date', flights[0]['departure_date'])
    print('return_date', flights[0]['return_date'])
    print('departure_time', flights[0]['departure_time'])
    print('arrival_time', flights[0]['arrival_time'])
    print('duration', flights[0]['duration'])
    print('stops', flights[0]['stops'])
'''