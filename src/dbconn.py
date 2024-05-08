"""
Database configuration and connection
"""
# importing necessary packages

import psycopg2 as db
import configparser
import pandas as pd
import sys
sys.path.append('../src/')
# read configuration file
config = configparser.ConfigParser()
config.read('/home/berna/playground/kifiya_ai/telecom-analysis/config.ini')

# Get the details
dbname = config.get('database', 'dbname')
user = config.get('database', 'user')
password = config.get('database', 'password')
host = config.get('database', 'host')


class DbDriver:
    """
    To connect and fetch data
    convert the data to pandas dataframe object
    """

    def __init__(self):
        # connect database
        try:
            self.conn = db.connect(
                dbname=dbname,
                user=user,
                host=host,
                password=password
            )
            self.cur = self.conn.cursor()
            print(f"Database connected")
        except Exception as e:
            print(f"DbDriver Error: {e}")

    def query_excute(self, query):
        self.cur.execute(query)
        records = self.cur.fetchall()
        return pd.DataFrame(records, columns=[desc[0] for desc in self.cur.description])

    def close_connection(self):
        self.cur.close()
        self.conn.close()

