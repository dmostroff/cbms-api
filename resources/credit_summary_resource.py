from flask import current_app
from flask import request
from flask_restful import Resource

import clients.client_service as cs

class ClientCreditSummary(Resource):
    def get(self, id):
        return cs.get_client_credit_summary_by_client (id)

class CreditSummary(Resource):
    def get(self):
        return cs.get_client_credit_summary()

