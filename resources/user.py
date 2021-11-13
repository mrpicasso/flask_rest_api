import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank"
                        )

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="this filed cannot be blank"
                        )

    def post(self):
        # getting the arguements from the http post request
        data = UserRegister.parser.parse_args()

        # verifying if user already exists
        if UserModel.find_by_username(data['username']):
            return {"Message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully"}, 201
