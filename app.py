
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT


from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store_resource import Store, StoreList

from db import db

app = Flask(__name__)
# our database file path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

# run this method before the first request
# no longer using creates_tables.py


@app.before_first_request
def create_tables():
    db.create_all()


'''
# creates new endpoint which is /auth we send over a username and password
# it is sendover to the authenticate function to find the correct user object using that username
# once user is validated - we receive a JWT token - which we use that JWT token to send in the next request
# When we send that JWT token, the JWT calles the identity() function and then it uses the JWT token to get the
user id and with that it gets the correct user for that user ID that the JWT token represents - which confirms that the user authenticated and that the JWT token is valid
'''
jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')  # http://localhost:8080/item
api.add_resource(StoreList, '/stores')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=8080, debug=True)
