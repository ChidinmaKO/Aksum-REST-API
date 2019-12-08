from typing import List, Union, Optional

import sqlite3

class ItemModel:
    TABLE_NAME = 'items'

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_itemname(cls, name: str):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = f"SELECT * FROM {cls.TABLE_NAME} items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        connection.close()
        
        if row:
            item = cls(*row)
            return item
        else:
            item = None
        
        return item

    def insert_item(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = f"INSERT INTO {self.TABLE_NAME} VALUES (?, ?)"
        cursor.execute(query, (self.name, self.price))

        connection.commit()
        connection.close()

    def update_item(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = f"UPDATE {self.TABLE_NAME} SET price=? WHERE name=?"
        cursor.execute(query, (self.price, self.name))

        connection.commit()
        connection.close()
