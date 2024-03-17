import pyodbc
from typing import Any, Dict
from imports.config import *


class Users:

    def __init__(self):
        self.users_database_name = 'EnergoMerchBot'
        self.users_table_name = 'users'
        self.server = 'tcp:servicesrv.energo.local'
        self.connect_string = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=' + self.server + \
                              ';DATABASE=' + self.users_database_name + ';ENCRYPT=no;UID=' + \
                              MSSQL_DB_USER_NAME + ';PWD=' + MSSQL_PASSWORD

    def get_telegram_id_by_phone_number(self, phone_number: str) -> int:
        select_query = f'SELECT id as Numeric FROM {self.users_table_name} where phone_number LIKE \'%{phone_number}\';'
        result = self.execute_query(select_query)
        if len(result) > 0:
            return result[0][0]
        return -1
    def get_link_by_telegram_id(self, telegram_id: int) -> str:
        select_query = f'SELECT link FROM {self.users_table_name} where id={telegram_id};'
        result = self.execute_query(select_query)
        return result[0][0]

    def is_phone_number_exists(self, phone_number: str) -> bool:
        select_query = f'SELECT * FROM {self.users_table_name} where phone_number LIKE \'%{phone_number}\';'
        result = self.execute_query(select_query)
        if len(result) > 0:
            return True
        return False

    def is_telegram_id_exists(self, telegram_id: int) -> bool:
        select_query = f'SELECT * FROM {self.users_table_name} where id=\'{telegram_id}\';'
        result = self.execute_query(select_query)
        if len(result) > 0:
            return True
        return False

    def list_database(self):
        select_query = f'SELECT * FROM {self.users_table_name};'
        return list(self.execute_query(select_query))

    def insert_number(self, phone_number: str) -> None:
        insert_query = 'INSERT INTO Users (phone_number) VALUES (?)'
        self.execute_query_with_commit(insert_query, phone_number)

    def insert_number_and_link(self, phone_number: str, link: str) -> None:
        insert_query = 'INSERT INTO Users (phone_number,link) VALUES (?,?)'
        self.execute_query_with_commit(insert_query, phone_number, link)

    def update_telegram_id(self, phone_number: str, telegram_id: int) -> None:
        update_query = f'UPDATE {self.users_table_name} ' \
                       f'SET id={telegram_id} WHERE phone_number LIKE \'%{phone_number}\';'
        self.execute_query_with_commit(update_query)

    def update_link(self, phone_number: str, link: str) -> None:
        update_query = f'UPDATE {self.users_table_name} ' \
                              f'SET link=(?) WHERE phone_number LIKE \'%{phone_number}\';'
        print(link)
        self.execute_query_with_commit(update_query, link)

    def execute_query(self, query: str) -> Any:
        result = ''
        database = pyodbc.connect(self.connect_string)
        try:
            cursor = database.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
        except pyodbc.Error as error:
            print(error)
        finally:
            database.close()
            return result

    def execute_query_with_commit(self, query: str, *args) -> None:
        database = pyodbc.connect(self.connect_string)
        try:
            cursor = database.cursor()
            cursor.execute(query, *args)
            database.commit()
            cursor.close()
        except pyodbc.Error as error:
            print(error)
        finally:
            database.close()


if __name__ == '__main__':
    pass


