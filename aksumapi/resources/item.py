from typing import List, Union, Optional

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="This field cannot be left blank - Every item needs a store id!"
    )

    # GET /item/<string:name>
    def get(self, name: str):
        item = ItemModel.find_by_itemname(name)
    
        if item:
            return item.json()
        return {'message': f"Item with name '{name}' not found"}, 404

    # POST /item/<string:name>
    @jwt_required()
    def post(self, name: str):
        item = ItemModel.find_by_itemname(name)
        if item:
            return {'message': f"An item with the name {name} already exists!"}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_item_to_db()
        except:
            return {'message': f"An error occurred whilst inserting the item 😞"}, 500

        return item.json(), 201

    # DELETE /item/<string:name>
    @jwt_required()
    def delete(self, name: str):
        item = ItemModel.find_by_itemname(name)

        if item:
            item.delete_item()
            return {'message': 'Item Deleted.'}

        return {'message': 'Item not found.'}, 404

    # PUT /item/<string:name>
    @jwt_required()
    def put(self, name: str):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_itemname(name)

        if item:
            try:
                item.price = data['price']
                item.save_item_to_db()
            except:
                return {'message': f"An error occurred updating this item"}, 500
        else:
            try:
                item = ItemModel(name, **data)
            except:
                return {'message': f"An error occurred inserting this item"}, 500

        return item.json()


class ItemList(Resource):
    # GET /items
    def get(self)-> List:
        items = ItemModel.find_all()
        return {'items': [item.json() for item in items]}