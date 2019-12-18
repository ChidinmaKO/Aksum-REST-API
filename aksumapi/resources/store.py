from typing import List, Union, Optional

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.store import StoreModel

class Store(Resource):
    parser = reqparse.RequestParser()

    # GET /store/<string:name>
    def get(self, name: str):
        store = StoreModel.find_by_storename(name)

        if store:
            return store.json()

        return {'message': f"Store with name '{name}' not found."}, 404

    # POST /store/<string:name>
    @jwt_required()
    def post(self, name: str):
        store = StoreModel.find_by_storename(name)

        if store:
            return {'message': f"A store with the name {name} already exists!"}, 400
        
        store = StoreModel(name)
        try:
            store.save_store_to_db()
        except:
            return {'message': f"An error occurred whilst inserting the store 😞"}, 500

        return store.json(), 201

    # DELETE /store/<string:name>
    @jwt_required()
    def delete(self, name: str):
        store = StoreModel.find_by_storename(name)

        if store:
            store.delete_store()
            return {'message': 'Store Deleted.'}

        return {'message': 'Store not found.'}, 404


class StoreList(Resource):
    # GET /stores
    def get(self):
        stores = StoreModel.query.all()
        return {'stores': [store.json() for store in stores]}
