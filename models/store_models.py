
from db import db


class StoreModel(db.Model):
    # table name
    __tablename__ = 'stores'
    # columns for the table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    # back refrence to store to ID
    # there could be more than one item related to one store
    # Many to one relationship
    # a store can have many items
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

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
