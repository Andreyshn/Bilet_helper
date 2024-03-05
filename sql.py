'''
#sqllite server, easy deployment, no need to run nothing
import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("connection success")
    except Error as e:
        print(f'Error {e} is occurred')
    return connection

create_connection("server.sqlite")'''

'''#mysql connecting, creating database, requires mysql server running
#to connect needs to add name in connect 
from mysql.connector import Error,connect
from getpass import getpass
def create_connection(host_name):
    connection = None
    try:
        with connect(
            host=host_name,
            user=input("Enter username: "),
            password= input("Enter password: ")
        ) as connection:
            create_db_query = "SHOW DATABASES"
            with connection.cursor() as cursor:
                cursor.execute(create_db_query)
                for db in cursor:
                    print(db)
            print(connection)
        print("Connected succesfully")
    except Error as e:
        print(f'error {e} is occurred')
    return connection
'''


#create_connection("localhost")


