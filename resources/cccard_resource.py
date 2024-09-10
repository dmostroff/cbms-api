from flask import request
from flask_restful import Resource
import creditcards.cc_card_service as cs
from creditcards.creditcards_transform import CcCardModelJsonToModel

class CcCards(Resource):
    def get(self):
        return cs.get_cc_cards()

class CcCard(Resource):
    def get(self, card_name):
        return cs.get_cc_card(card_name)

# class CcCardPost(Resource):
#     def post(self, id):
#         cc_card = CcCardModelJsonToModel(request.get_json())
#         return cs.post_cc_card( cc_card )