import mysql.connector
from mysql.connector import Error
import configparser

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    db_config = {
        'host': config.get('mysql', 'host'),
        'port': config.getint('mysql', 'port'),
        'database': config.get('mysql', 'database'),
        'user': config.get('mysql', 'user'),
        'password': config.get('mysql', 'password')
    }
    return db_config

def create_connection():
    connection = None
    try:
        db_config = load_config()
        connection = mysql.connector.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password']
        )

        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def create_database(connection,database):
    try:
        cur = connection.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        cur.execute(f"USE {database}")
        print("Successfully connected to the database and ensured it exists.")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def close_connection(connection):
    if connection is not None and connection.is_connected():
        connection.close()
        print("Database connection closed.")
