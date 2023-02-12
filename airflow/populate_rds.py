import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def populate_rds():

    # initialize RDS Postgres connection
    engine = psycopg2.connect(
        user=os.environ.get("AWS_DB_USER"),
        password=os.environ.get("AWS_DB_PASSWORD"),
        host=os.environ.get("AWS_DB_URL"),
        port='5432'
    )
    engine.autocommit = True
    cursor = engine.cursor()

    # read normalized csv file
    healthdata = pd.read_csv('normalized.csv', usecols=[
                             'name', 'units', 'date', 'qty'])
    table_names = healthdata.name.unique()
    print(table_names)

    # create a seperate table for each health metric
    for table in table_names:
        create_table_sql = f"""CREATE TABLE IF NOT EXISTS {table} (
                            id serial NOT NULL,
                            datetime date NOT NULL,
                            units varchar(45) NOT NULL,
                            quantity decimal NOT NULL,
                            PRIMARY KEY (id))"""

        cursor.execute(create_table_sql)

    # insert values into the database
    for row in healthdata.itertuples(index=False):
        postgres_insert_query = f"""INSERT INTO {row.name} (units, datetime, quantity) VALUES (%s,%s,%s)"""
        cursor.execute(postgres_insert_query, (row.units, row.date, row.qty))


populate_rds()
