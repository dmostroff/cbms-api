from flask import request
from flask_restful import Resource
import clients.client_israel_service as cis

class Banks(Resource):
    def get(self):
        return cis.get_bank_names()
