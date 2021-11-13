
from db import db


class ItemModel(db.Model):
    # table name
    __tablename__ = 'items'
    # columns for the table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    # connecting store id to the items
    # every item has a store
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        # select * from items where name=name
        # returns back the first item
        # .query.filter_by comes form SQLAlchemy = db.Model
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        # insert into database or update into datbase
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
