from typing import Optional

from flask_restful import Api, Resource, reqparse
import sqlite3

class User:
    TABLE_NAME = 'users'

    def __init__(self, id_, username, password):
        self.id = id_
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username: str):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE username=?"
        result = cursor.execute(query, (username,))

        row = result.fetchone()
        if row:
            # user = User(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None

        # always remember to close the connection before returning.
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, id_):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE id=?"
        result = cursor.execute(query, (id_,))

        row = result.fetchone()
        if row:
            # user = cls(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None

        # always remember to close the connection before returning.
        connection.close()
        return user

class UserRegister(Resource):
    TABLE_NAME = 'users'

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

        if User.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = f"INSERT INTO {self.TABLE_NAME} VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User created successfully!"}, 201
