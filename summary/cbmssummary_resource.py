from flask import request
from flask_restful import Resource
import cbmssummary_service as cs

class CBMSSummary(Resource):
    def get(self):
        return cs.get_cbms_summary()
