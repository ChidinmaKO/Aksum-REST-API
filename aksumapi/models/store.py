from typing import List, Union, Optional

from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        items = [item.json() for item in self.items.all()]
        return {
            'id': self.id,
            'name': self.name, 
            'items': items
        }

    def __repr__(self):
        items = [item.json() for item in self.items.all()]
        return f"StoreModel('{self.name}': '{items}')"

    @classmethod
    def find_by_storename(cls, name: str):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_store_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_store(self):
        db.session.delete(self)
        db.session.commit()
