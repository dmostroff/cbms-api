import numpy as np
import creditcards.cc_card_repository as cr
import common.base_service as bs

from models.CcCardModel import CcCardModel



#--------------------
# cc_card
#--------------------

@bs.repository_call
def get_cc_cards ():
    return cr.get_cc_cards()

# @bs.repository_call
# def get_cc_card_by_cc_card_id (cc_card_id):
#     return cr.get_cc_card_by_cc_card_id(cc_card_id)

@bs.repository_call_single_row
def get_cc_card (id):
    return cr.get_cc_card_by_id(id)

@bs.repository_call_single_row
def post_cc_card ( cc_card:CcCardModel):
    return cr.upsert_cc_card(cc_card)
    # id = np.int64(df['cc_card_id'].values[0]).item()
    # return get_cc_card_by_id(id)

