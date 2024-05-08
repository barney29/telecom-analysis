"""
dedicated unit test for db connection using psycpg2
"""
import pytest
import configparser
import psycopg2 as db
import os

os.chdir('..')
config = configparser.ConfigParser()
config.read('config.ini')

# Get the details
dbname = config.get('database', 'dbname')
user = config.get('database', 'user')
password = config.get('database', 'password')
host = config.get('database', 'host')


class TestConnection:
    @pytest.fixture(scope='class')
    def db_conn(self):
        conn = db.connect(
            dbname=dbname,
            user=user,
            host=host,
            password=password
        )
        yield conn
        conn.close()

    def test_connection(self, db_conn):
        assert db_conn is not None

    def test_fetch_all(self, db_conn):
        cursor = db_conn.cursor()
        cursor.execute('SELECT * FROM public.xdr_data')
        result = cursor.fetchall()
        assert result is not None
        cursor.close()
