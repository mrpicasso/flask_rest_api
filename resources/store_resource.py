
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store_models import StoreModel


class Store(Resource):
    # only creating get, post, and delete endpoints

    def get(self, name):
        # find the store
        store = StoreModel.find_by_name(name)
        # if store is found then return it
        if store:
            return store.json()
        # if store is not found - then return message with status error code
        return {'message': 'store not found'}, 404

    def post(self, name):
        # check to see if the store already exists
        if StoreModel.find_by_name(name):
            return {"message": "A store with name '{}' already exists".format(name)}
        # create new store since it does not exists
        store = StoreModel(name)
        try:
            # save new store to the database
            store.save_to_db()
        except:
            return {'Message': 'An error occurred inserting the item'}, 500
        return store.json(), 201

    # send a delete http request to delete a store

    def delete(self, name):
        # find the store
        store = StoreModel.find_by_name(name)
        # if store exists then delete it from the database
        if store:
            store.delete_from_db()

        return {
            'message': 'Store has been deleted'
        }

# retrieve all the stores with a get http request


class StoreList(Resource):
    def get(self):
        return {
            'stores': [store.json() for store in StoreModel.query.all()]
        }
