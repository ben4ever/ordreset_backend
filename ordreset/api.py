from flask import request
from flask_restful import Resource

from ordreset import api
from ordreset.db import interface


class Orders(Resource):
    def get(self):
        return interface.get_orders()


class Order(Resource):
    def get(self, order_id):
        return interface.get_order(order_id)

    def put(self, order_id):
        data = request.get_json()
        fields = {'xml': None, 'resubmit': False, 'cancel': False}
        for key in fields.keys():
            if key in data:
                fields[key] = data[key]

        return interface.update_order(
                id_=order_id, **fields)


api.add_resource(Orders, '/orders')
api.add_resource(Order, '/orders/<order_id>')
