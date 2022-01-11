from configparser import Error
import os
import mysql.connector
from dotenv import load_dotenv
import mysql.connector

load_dotenv()


def flatten_list(input_list):
    return [item for sublist in input_list for item in sublist]


class DatabaseConnection():
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host=os.environ.get("HOST"),
                user=os.environ.get("DB_USERNAME"),
                password=os.environ.get("PASSWORD"),
                connect_timeout=28800,
            )
        except Error:
            print(Error)
            exit(1)

    def create_db(self, db_name):
        cursor = self.connection.cursor()
        cursor.execute("SHOW DATABASES")
        if db_name not in flatten_list(cursor):
            cursor.execute(f"CREATE DATABASE {db_name}")
        else:
            print("DB already exists")
        cursor.close()

    def create_table(self, table_name):
        cursor = self.connection.cursor()
        cursor.execute("USE applehealthreport")
        try:
            create_statement = f"CREATE TABLE {table_name} (creation_date DATETIME, start_date DATETIME, end_date DATETIME, value FLOAT)"
            cursor.execute(create_statement)
        except mysql.connector.ProgrammingError as err:
            if err.errno == 1050:
                print(f"Error: {table_name} already exsists!")
            else:
                print(err)
        finally:
            cursor.close()

    def insert_data(self, data, table_name):
        cursor = self.connection.cursor()
        try:
            insert_statement = f"INSERT INTO {table_name} (creation_date, start_date, end_date, value) VALUES (%s, %s, %s, %s)"
            cursor.executemany(insert_statement, data)
            self.connection.commit()
        except mysql.connector.ProgrammingError as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
