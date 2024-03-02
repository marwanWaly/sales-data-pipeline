import pandas as pd
import sqlite3
from sqlite3 import Error
import os


def create_connection(path_to_db: str):
    conn = None
    try:
        conn = sqlite3.connect(path_to_db)
    except Error as e:
        print(e)
    return conn


def create_tables(db_creation_path: str, conn):
    with open(db_creation_path, 'r') as sql_file:
        sql_script = sql_file.read()

    cursor = conn.cursor()
    cursor.executescript(sql_script)
    conn.commit()
    print("DB is created")


def get_db_connection(path_to_db: str, path_to_creation_file: str):
    # Convert path to list to prevent '/' and '\' issue
    # different OS are using different separator
    path_as_list = path_to_db.split("/")
    path_to_db = os.path.join(os.path.dirname(__file__), *path_as_list)

    # Convert path to list to prevent '/' and '\' issue
    # different OS are using different separator
    path_as_list = path_to_creation_file.split("/")
    path_to_creation_file = os.path.join(os.path.dirname(__file__), *path_as_list)

    db_exists = os.path.exists(path_to_db)

    conn = create_connection(path_to_db)

    if conn and not db_exists:
        create_tables(path_to_creation_file, conn)

    return conn


def load_data(data: pd.DataFrame, table_name: str, con) -> bool:
    try:
        data.to_sql(table_name, con, if_exists='append', index=False)
    except Exception as e:
        print(f"Error: cannot load {table_name} to DB:\n{str(e)}")
        return False

    return True
