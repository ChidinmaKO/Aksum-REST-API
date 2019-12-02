from typing import List, Union, Optional

from flask import Flask, request, render_template
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "c933ac116227737997d2e27a6d4cd6bf0d3bac640a5ec422c1d203ac58df1487"
api = Api(app)

jwt = JWT(app, authenticate, identity) #creates a new endpoint called '/auth'


items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )


    # GET /items
    def get(self, name: str)-> Optional[dict]:
        item = next(filter(lambda item: item['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    # POST /item/<string:name>
    @jwt_required()
    def post(self, name: str)-> List[dict]:
        # if there's already an item matching the name, just return a message
        item = next(filter(lambda item: item['name'] == name, items), None)
        if item:
            return {'message': f"An item with the name {item['name']} already exists!"}, 400

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return items, 201

    # DELETE /item/<string:name>
    @jwt_required()  
    def delete(self, name: str):
        global items
        items = list(filter(lambda item: item['name'] != name, items))
        return {'message': 'Item Deleted'}

    # PUT /item/<string:name>
    @jwt_required()
    def put(self, name: str):
        data = Item.parser.parse_args()

        # check if item exists already
        item = next(filter(lambda item: item['name'] == name, items), None)
        if item:
            item.update(data)
        else:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        return item

# FIXME: Note that PUT & DELETE are idempotent requests. 
# A request is Idempotent when the effects of calling it once is the same as calling it several times. 
# Choose PUT IFF the endpoint must be idempotent and if the URI must be the address to the resource being updated.


class ItemList(Resource):
    # GET /items
    def get(self)-> List:
        return {'items': items}

    
api.add_resource(Item, '/item/<string:name>') #http://127.0.0.1:3000/item/book
api.add_resource(ItemList, '/items') #http://127.0.0.1:3000/items


if __name__ == '__main__':
    app.run(port=3000, debug=True)