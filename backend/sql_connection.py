import mysql.connector
from mysql.connector import Error

__cnx = None

def get_sql_connection():
    global __cnx
    if __cnx is None:
        try:
            # Create and assign the connection to the global variable
            __cnx = mysql.connector.connect(user="root", password="ashmit10",
                                            host="127.0.0.1",
                                            database="gs")
            print("Connection established.")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            __cnx = None

    return __cnx
