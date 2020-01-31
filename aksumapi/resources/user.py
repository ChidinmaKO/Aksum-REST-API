from typing import Optional

from flask_restful import Resource, reqparse

from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user:
            return {"message": f"A user with the username {username} already exists"}, 400

        user = UserModel(**data)

        try:
            user.save_user_to_db()
        except:
            return {"message": f"An error occurred! 😞"}, 500

        return {"message": "User created successfully!"}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json()

        return {'message': 'User not found'}, 404

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_user()
            return {'message': 'User deleted'}

        return {'message': 'User not found.'}, 404


class UserList(Resource):
    def get(self):
        users = UserModel.find_all()
        return {'users': [user.json() for user in users]}
