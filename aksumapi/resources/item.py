from typing import List, Union, Optional

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    # GET /items
    def get(self, name: str):
        item = ItemModel.find_by_itemname(name)
    
        if item:
            return item.json()
        return {'message': f"Item with name {name} not found"}, 404

    # POST /item/<string:name>
    @jwt_required()
    def post(self, name):
        item = ItemModel.find_by_itemname(name)
        if item:
            return {'message': f"An item with the name {name} already exists!"}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'])

        try:
            item.insert_item()
        except:
            return {'message': f"An error occurred inserting the item 😞"}, 500

        return item.json(), 201

    # DELETE /item/<string:name>
    @jwt_required()
    def delete(self, name: str):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = f"DELETE FROM {ItemModel.TABLE_NAME} WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item Deleted'}

    # PUT /item/<string:name>
    @jwt_required()
    def put(self, name: str):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_itemname(name)
        updated_item = ItemModel(name, data['price'])

        if item:
            try:
                updated_item.update_item()
            except:
                return {'message': f"An error occurred updating this item"}, 500
        else:
            try:
                updated_item.insert_item()
            except:
                return {'message': f"An error occurred inserting this item"}, 500
        return updated_item.json()


class ItemList(Resource):
    TABLE_NAME = 'items'
    # GET /items
    def get(self)-> List:
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = f"SELECT * FROM {ItemModel.TABLE_NAME}"
        result = cursor.execute(query)
        items = []

        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        
        connection.close()

        return {'items': items}