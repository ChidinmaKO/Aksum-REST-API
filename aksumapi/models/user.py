from typing import Optional

from db import db

class UserModel(db.Model):
    _table_name = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __init__(self, id_, username, password):
        self.id = id_
        self.username = username
        self.password = password

    def __repr__(self):
        return f"UserModel('{self.username}')"

    @classmethod
    def find_by_username(cls, username: str):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id_):
        return cls.query.filter_by(id=id_).first()