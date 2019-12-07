from typing import List, Union, Optional

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

class Item(Resource):
    TABLE_NAME = 'items'

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @classmethod
    def find_by_itemname(cls, name: str):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = f"SELECT * FROM {cls.TABLE_NAME} items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        connection.close()
        
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    @classmethod
    def insert_item(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = f"INSERT INTO {cls.TABLE_NAME} VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

        return item

    @classmethod
    def update_item(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = f"UPDATE {cls.TABLE_NAME} SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

        return item

    # GET /items
    def get(self, name: str):
        item = Item.find_by_itemname(name)
    
        if item:
            return item
        return {'message': f"Item with name {name} not found"}, 404

    # POST /item/<string:name>
    @jwt_required()
    def post(self, name):
        item = Item.find_by_itemname(name)
        if item:
            return {'message': f"An item with the name {name} already exists!"}, 400

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}

        try:
            Item.insert_item(item)
        except:
            return {'message': f"An error occurred inserting the item 😞"}, 500

        return item, 201

    # DELETE /item/<string:name>
    @jwt_required()
    def delete(self, name: str):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = f"DELETE FROM {self.TABLE_NAME} WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item Deleted'}

    # PUT /item/<string:name>
    @jwt_required()
    def put(self, name: str):
        data = Item.parser.parse_args()

        item = Item.find_by_itemname(name)
        updated_item = {'name': name, 'price': data['price']}

        if item:
            try:
                Item.update_item(updated_item)
            except:
                raise
                return {'message': f"An error occurred updating this item"}, 500
        else:
            try:
                Item.insert_item(updated_item)
            except:
                return {'message': f"An error occurred inserting this item"}, 500
        
        return updated_item


# FIXME: Note that PUT & DELETE are idempotent requests. 
# A request is Idempotent when the effects of calling it once is the same as calling it several times. 
# Choose PUT IFF the endpoint must be idempotent and if the URI must be the address to the resource being updated.

class ItemList(Resource):
    TABLE_NAME = 'items'
    # GET /items
    def get(self)-> List:
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = f"SELECT * FROM {self.TABLE_NAME}"
        result = cursor.execute(query)
        items = []

        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        
        connection.close()

        return {'items': items}

