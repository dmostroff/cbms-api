from flask import request
from flask_restful import Resource
import creditcards.cc_company_service as cs
from creditcards.creditcards_transform import CcCompanyModelJsonToModel

class CcCompanies(Resource):
    def get(self):
        return cs.get_cc_companies()

class CcCompany(Resource):
    def get(self, id):
        return cs.get_cc_company(id)

    def post( self):
        cc_company = CcCompanyModelJsonToModel(request.get_json())
        return cs.post_cc_company( cc_company)

class CcCompanyPost(Resource):
    def post(self):
        cc_company = CcCompanyModelJsonToModel(request.get_json())
        return cs.post_cc_company( cc_company)
