from typing import List, Union, Optional

from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    fresh_jwt_required, 
    get_jwt_claims, 
    get_jwt_identity, 
    jwt_optional, 
    jwt_required
)

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

    @jwt_required
    def get(self, name: str):
        item = ItemModel.find_by_itemname(name)
    
        if item:
            return item.json()
        return {'message': f"Item with name '{name}' not found"}, 404

    @fresh_jwt_required
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

    @fresh_jwt_required
    def delete(self, name: str):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privileges required.'}, 401

        item = ItemModel.find_by_itemname(name)

        if item:
            item.delete_item()
            return {'message': 'Item Deleted.'}

        return {'message': 'Item not found.'}, 404

    @fresh_jwt_required
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
    @jwt_optional
    def get(self)-> List:
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        item_name = [item['name'] for item in items]
        
        if user_id:
            return {'items': items}, 200
        return {
            'item names': item_name,
            'message': 'More data available if you log in.'
        }, 200