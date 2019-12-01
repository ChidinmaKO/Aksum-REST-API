from typing import List, Union, Optional

from flask import Flask, request, render_template
from flask_restful import Resource, Api
from flask_jwt import JWT

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "c933ac116227737997d2e27a6d4cd6bf0d3bac640a5ec422c1d203ac58df1487"
api = Api(app)

jwt = JWT(app, authenticate, identity)


items = []

class Item(Resource):
    # GET /items
    def get(self, name: str)-> Optional[dict]:
        item = next(filter(lambda item: item['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    # POST /item/<string:name>
    def post(self, name: str)-> List[dict]:
        # if there's already an item matching the name, just return a message
        item = next(filter(lambda item: item['name'] == name, items), None)
        if item:
            return {'message': f"An item with the name {item['name']} already exists!"}, 400
        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return items, 201


class ItemList(Resource):
    # GET /items
    def get(self)-> List:
        return {'items': items}

    # DELETE /item/<string:name>  
    # def delete(self, name: str):
    #     return
    #     pass

    # PUT /item/<string:name>
    # def put(self, name: str):
    #     return
    #     pass

    
api.add_resource(Item, '/item/<string:name>') #http://127.0.0.1:3000/item/book
api.add_resource(ItemList, '/items') #http://127.0.0.1:3000/items


if __name__ == '__main__':
    app.run(port=3000, debug=True)