import sqlite3
from db import db


class UserModel(db.Model):
    # table name where these Models are going to be stored
    __tablename__ = 'users'
    # what columns the table contains
    id = db.Column(db.Integer, primary_key=True)
    # username  and password column
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        # SELECT * FROM users WHERE username = username
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
