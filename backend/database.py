# database.py

'''
MySQL workbench:

CREATE DATABASE excel_management;
USE excel_management;

'''
import mysql.connector
from config import DB_CONFIG

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def save_to_db(table_name, data):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Check if table exists, if not create it
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    result = cursor.fetchone()
    if not result:
        # Table doesn't exist, create it
        if table_name == 'invites_table':
            query = '''
                CREATE TABLE excel_management.invites_table (
                    `Name` VARCHAR(255),
                    `Email` VARCHAR(255),
                    `Test name` VARCHAR(255),
                    `Invites Time` VARCHAR(255),
                    `Appeared in test` VARCHAR(255),
                );
            '''
        elif table_name == 'test_table':
            query = '''
                CREATE TABLE excel_management.test_table (
                    `Name` VARCHAR(255),
                    `Email` VARCHAR(255),
                    `Mobile` VARCHAR(15),
                    `Test name` VARCHAR(255),
                    `Test status` VARCHAR(255),
                    `Submitted time` VARCHAR(255),
                    `Submitted reason` VARCHAR(255),
                    `CN rating` FLOAT
                );
            '''
        elif table_name == 'consolidated_table':
            query = '''
                CREATE TABLE excel_management.consolidated_table (
                    `Name` VARCHAR(255),
                    `Email` VARCHAR(255),
                    `Mobile` VARCHAR(15),
                    `Test name` VARCHAR(255),
                    `Invited` INT,
                    `Not Appeared` INT,
                    `Appeared` INT,
                    `Lowest Score` FLOAT,
                    `Highest Score` FLOAT
                );
            '''
        elif table_name == 'batch_information':
            query = '''
                CREATE TABLE excel_management.batch_information (
                    `email` VARCHAR(255),
                    `batch` VARCHAR(50)
                );
            '''
        else:
            raise ValueError("Unknown table name")

        cursor.execute(query)
        connection.commit()

    columns = ', '.join(f'`{col}`' for col in data[0].keys())
    placeholders = ', '.join(['%s'] * len(data[0]))
    query = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"

    values = [tuple(row.values()) for row in data]

    try:
        cursor.executemany(query, values)
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()



