import sqlite3
from typing import Any, Dict


class Users:

    def __init__(self):
        self.users_database_name = 'users.db'
        self.users_table_name = 'users'

    def create_database(self):
        sqlite_create_table_query = f'''CREATE TABLE {self.users_table_name} (
                                                id INTEGER,
                                                phone_number TEXT PRIMARY KEY
                                                );'''
        self.execute_query_with_commit(sqlite_create_table_query)

    def list_database(self):
        sqlite_select_query = f'SELECT * FROM {self.users_table_name};'
        return [x for x in self.execute_query(sqlite_select_query)]

    def is_phone_number_exists(self, phone_number: str) -> bool:
        sqlite_select_query = f'SELECT * FROM {self.users_table_name} where phone_number LIKE \'%{phone_number}\';'
        result = self.execute_query(sqlite_select_query)
        if len(result) > 0:
            return True
        return False

    def is_telegram_id_exists(self, telegram_id: int) -> bool:
        sqlite_select_query = f'SELECT * FROM {self.users_table_name} where id=\'{telegram_id}\';'
        result = self.execute_query(sqlite_select_query)
        if len(result) > 0:
            return True
        return False

    def update_telegram_id(self, phone_number: str, telegram_id: int) -> None:
        sqlite_update_query = f'UPDATE {self.users_table_name} ' \
                              f'SET id={telegram_id} WHERE phone_number LIKE \'%{phone_number}\';'
        self.execute_query_with_commit(sqlite_update_query)



    def insert_number(self, phone_number: str) -> None:
        sqlite_insert_query = f'''INSERT INTO {self.users_table_name}
        (phone_number)
        VALUES (\'{phone_number}\');
        '''
        self.execute_query_with_commit(sqlite_insert_query)

    def execute_query(self, query: str) -> Any:
        result = ''
        database = sqlite3.connect(self.users_database_name)
        try:
            cursor = database.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
        except sqlite3.Error as error:
            print(error)
        finally:
            database.close()
            return result

    def execute_query_with_commit(self, query: str) -> None:
        database = sqlite3.connect(self.users_database_name)
        try:
            cursor = database.cursor()
            cursor.execute(query)
            database.commit()
            cursor.close()
        except sqlite3.Error as error:
            print(error)
        finally:
            database.close()


if __name__ == '__main__':
    base = Users()
    base.users_database_name = '..\\users.db'
    #base.create_database()
    #base.insert_number('')
    base.list_database()
    #print(base.is_phone_number_exists())