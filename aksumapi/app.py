from datetime import timedelta

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from flask_sqlalchemy import SQLAlchemy

from resources.item import Item, ItemList
from resources.user import UserRegister
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "c933ac116227737997d2e27a6d4cd6bf0d3bac640a5ec422c1d203ac58df1487"
api = Api(app)

# This changes the authentication endpoint from the default, '/auth' to '/login'. 
# It must be done before creating the JWT instance!
app.config['JWT_AUTH_URL_RULE'] = '/login' 
jwt = JWT(app, authenticate, identity) 
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1200) # This configures JWT to expire in 20 minutes.

# handle JWT errors
def jwt_error_handler(error):
    return jsonify({
        'message': error.description,
        'code': error.status_code,
    }), error.status_code


api.add_resource(Item, '/item/<string:name>') #http://127.0.0.1:3000/item/book
api.add_resource(ItemList, '/items') #http://127.0.0.1:3000/items
api.add_resource(UserRegister, '/register') #http://127.0.0.1:3000/register

if __name__ == '__main__':
    app.run(port=3000, debug=True)