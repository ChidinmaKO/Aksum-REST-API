from typing import Optional

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_raw_jwt,
    jwt_optional,
    jwt_refresh_token_required,
    jwt_required
)
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp

from blacklist import BLACKLIST
from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                            type = str,
                            required = True,
                            help="This field cannot be left blank!"
                        )
_user_parser.add_argument('password',
                            type=str,
                            required=True,
                            help="This field cannot be left blank!"
                        )


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user:
            return {"message": f"A user with the username {username} already exists"}, 400

        user = UserModel(**data)

        try:
            user.save_user_to_db()
        except:
            return {"message": f"An error occurred! 😞"}, 500

        return {"message": "User created successfully! 💃🏿"}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json()

        return {'message': 'User not found'}, 404

    @classmethod
    @jwt_required
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_user()
            return {'message': 'User deleted'}

        return {'message': 'User not found.'}, 404


class UserList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        users = [user.json() for user in UserModel.find_all()]
        user_names = [user['username'] for user in users]

        if user_id:
            return {'users': users}, 200
        return {
            'user names': user_names,
            'message': 'More data available if you log in.'
        }, 200


class UserLogin(Resource):
    def post(self):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if(user and safe_str_cmp(user.password, data['password'])):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'Invalid Credentials! 😐'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti'] #jti == JWT ID
        print(jti)
        BLACKLIST.add(jti)
        print(len(BLACKLIST))
        return {'message': 'Successfully logged out ✌🏿'}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access token': new_token}, 200