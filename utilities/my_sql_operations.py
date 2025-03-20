import mysql.connector
import os
from sqlalchemy import create_engine
        
from dotenv import load_dotenv
load_dotenv(override=True)

class MySQLOperations:
    def __init__(self):
        """
        Set MySQL connection parameters using environment variables
        """
        self.host = os.getenv('MYSQL_HOST')
        self.port = os.getenv('MYSQL_PORT')
        self.user = os.getenv('MYSQL_USER')
        self.password = os.getenv('MYSQL_PASSWORD')

    def create_connection(self, database):
        """
        Connect to the MySQL database
        Args:
            database (str): name of the database to connect to.
        Returns:
            mysql.connector.connection.MySQLConnection: connection object to the specified MySQL database.
        """
        
        connection = mysql.connector.connect(
            host = self.host,
            user = self.user ,
            password = self.password,
            database = database, 
            port = self.port
        )
        return connection
    
    def create_sqlalchemy_engine(self, connection_string):
        engine = create_engine(connection_string, echo=False)
        
        return engine
        
    def fetch_data(self, query):
        """
        Fetch data from the MySQL database
        Args:
            query (str): SQL query to fetch data from the MySQL database.
        Returns:
            list: list of tuples containing the fetched data.
            list: list of column names
        """
        connection = self.create_connection('fleet-data')
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        connection.close()
        return data, columns