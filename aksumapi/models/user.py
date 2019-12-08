from typing import Optional

import sqlite3

class UserModel:
    TABLE_NAME = 'users'

    def __init__(self, id_, username, password):
        self.id = id_
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username: str):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE username=?"
        result = cursor.execute(query, (username,))

        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        # always remember to close the connection before returning.
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, id_):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE id=?"
        result = cursor.execute(query, (id_,))

        row = result.fetchone()
        if row:
            # user = cls(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None

        # always remember to close the connection before returning.
        connection.close()
        return user