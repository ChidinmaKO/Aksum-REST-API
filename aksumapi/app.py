from datetime import timedelta

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import User, UserList, UserLogin, UserRegister


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "c933ac116227737997d2e27a6d4cd6bf0d3bac640a5ec422c1d203ac58df1487"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

jwt = JWTManager(app) 
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=1200) # This configures the access token to expire in 20 minutes.
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(seconds=1000) # This configures the refresh token to expire in 20 minutes.

# handle JWT errors
def jwt_error_handler(error):
    return jsonify({
        'message': error.description,
        'code': error.status_code,
    }), error.status_code


@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Item, '/item/<string:name>') #http://127.0.0.1:3000/item/book
api.add_resource(ItemList, '/items') #http://127.0.0.1:3000/items
api.add_resource(Store, '/store/<string:name>') #http://127.0.0.1:3000/store/diamond
api.add_resource(StoreList, '/stores') #http://127.0.0.1:3000/stores
api.add_resource(User, '/user/<int:user_id>') #http://127.0.0.1:3000/user/1
api.add_resource(UserList, '/users') #http://127.0.0.1:3000/users
api.add_resource(UserLogin, '/login') #http://127.0.0.1:3000/login
api.add_resource(UserRegister, '/register') #http://127.0.0.1:3000/register

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=3000, debug=True)


# TODO: RESTRUCTURE ENTIRE PACKAGE STRUCTURE