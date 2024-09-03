import db_connector
from queries import create_tables


def main():
    connection = db_connector.create_connection()
    create_tables(connection)





if __name__ == "__main__":
    main()
