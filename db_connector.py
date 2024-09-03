import mysql.connector
from mysql.connector import Error
import configparser

def load_config():
    """Load database configuration from a config file."""
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
    """Create and return a database connection."""
    connection = None
    try:
        db_config = load_config()
        connection = mysql.connector.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        
        if connection.is_connected():
            print("Successfully connected to the database.")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def close_connection(connection):
    """Close the database connection."""
    if connection is not None and connection.is_connected():
        connection.close()
        print("Database connection closed.")
