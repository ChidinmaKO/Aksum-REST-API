from typing import List, Union, Optional

from db import db


class ItemModel(db.Model):
    _table_name = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    def __repr__(self):
        return f"ItemModel('{self.name}', '{self.price}')"

    @classmethod
    def find_by_itemname(cls, name: str):
        return cls.query.filter_by(name=name).first()

    def save_item_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_item(self):
        db.session.delete(self)
        db.session.commit()
