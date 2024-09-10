from flask_restful import Resource
import clients.cc_account_service as cs

ccAccountPromo = {}
class CcAccountPromos(Resource):
    def get(self):
        return cs.get_cc_account_promo()

class CcAccountPromo(Resource):
    def get(self, id):
        return cs.get_cc_account_promo(id)

    def put(self, id):
        ccAccountPromo[id] = request.form['ccAccountPromo']
        return {ccAccountPromo_id: ccAccountPromo[id]}