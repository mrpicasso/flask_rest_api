

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    # making sure we only get price attribute when we update existing Resource
    # parse the arguements that come through the json payload and put the valid ones in data
    # in this case we would only get 'price' arguements and not any other ones
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float, required=True,
                        help='This field cannot be left blank!'
                        )

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='Every item needs a store id.'
                        )

    # required a JWT Token
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'item not found'}, 404

    # creates a new resource
    def post(self, name):
        # check to see if the item is already exisiting
        if ItemModel.find_by_name(name):
            return {"message": "An item with name '{}' already exists".format(name)}, 400

        # get the pay load data from the client request
        # data = request.get_json()

        # getting the arguements from the http post request
        data = Item.parser.parse_args()
        # creating a item model instance
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"Message": "An error occurred inserting the item"}, 500

        return item.json(), 201

    # send a Delete HTTP request to delete an item
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    # can either update an exisiting resource or create one if it does not exist
    def put(self, name):
        # getting the arguments from the http put request
        data = Item.parser.parse_args()
        # checking to see if the item already exits
        item = ItemModel.find_by_name(name)
        # creating and updating a new ItemModel Instance

        # if item does not exist then lets create it
        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        # if item does exist then lets update it
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()


# retrieve all the items with a get http request
class ItemList(Resource):
    def get(self):
        return {
            # alternative way
            # list(map(lambda x: x.json(), ItemModel.query.all()))
            'items': [item.json() for item in ItemModel.query.all()]

        }
        '''
        understanding the List comprehension 
        this would be my way of doing it 
        item_list = []
        for item in ItemModel.query.all():
            item_list.append(item.json())

        '''
