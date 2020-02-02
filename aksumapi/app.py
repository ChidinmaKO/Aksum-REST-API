from datetime import timedelta

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from blacklist import BLACKLIST
from db import db
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import (
    TokenRefresh,
    User,
    UserList,
    UserLogin,
    UserLogout,
    UserRegister
)


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "c933ac116227737997d2e27a6d4cd6bf0d3bac640a5ec422c1d203ac58df1487"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
api = Api(app)

jwt = JWTManager(app)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=600)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(seconds=1800)

@jwt.user_claims_loader
def user_claims_callback(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blacklist_loader
def token_in_blacklist_callback(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired. 💀',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error: str):
    return jsonify({
        'description': 'Invalid JWT. 🤖',
        'error': 'invalid_token'
    }), 422

@jwt.unauthorized_loader
def unauthorized_callback(error: str):
    return jsonify({
        'description': 'JWT can\'t be found. 👻',
        'error': 'authorization required'
    }), 401

@jwt.needs_fresh_token_loader
def needs_fresh_token_callback():
    return jsonify({
        'description': 'Fresh token required. 🤓',
        'error': 'authorization_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked. 😈',
        'error': 'token_revoked'
    }), 401

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserList, '/users')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=3000, debug=True)


# TODO: RESTRUCTURE ENTIRE PACKAGE STRUCTURE