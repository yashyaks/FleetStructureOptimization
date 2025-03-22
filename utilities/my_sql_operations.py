import mysql.connector
import os
from sqlalchemy import create_engine
import pandas as pd
        
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
    
    def table_exists(self, table_name):
        connection = self.create_connection('fleet-data')
        cursor = connection.cursor()
        query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = '{table_name}');"
        cursor.execute(query)
        exists = cursor.fetchone()[0]  # Returns 1 if table exists, 0 otherwise
        cursor.close()
        return exists
    
    def push_input_data(self, data, table_name):
        connection_string = os.getenv('INPUT_STRING')
        engine = self.create_sqlalchemy_engine(connection_string)
        data.to_sql(table_name, con=engine, if_exists='replace')
        
    
    def push_output_data(self, data, table_name):
        connection_string = os.getenv('OUTPUT_STRING')
        engine = self.create_sqlalchemy_engine(connection_string)
        data.to_sql(table_name, con=engine, if_exists='replace')
        
    def fetch_input_data(self, table_name):
        connection = self.create_connection('input')
        cursor = connection.cursor()
        query = f"""SELECT * FROM {table_name};"""
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(data, columns=columns)
        cursor.close()
        connection.close()
        return df