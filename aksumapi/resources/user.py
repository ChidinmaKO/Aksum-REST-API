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
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)

        try:
            user.save_user_to_db()
        except:
            return {"message": f"An error occurred! 😞"}, 500
        
        return {"message": "User created successfully!"}, 201        
