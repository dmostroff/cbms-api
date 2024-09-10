import common.base_service as bs
from common.common_service import extract_card_info
import clients.cc_account_repository as car
from models.CcAccountModel import CcAccountModel


#--------------------
# cc_account
#--------------------

@bs.repository_call
def get_cc_account ():
    df = car.get_cc_account()
    extract_card_info(df, 'cc_card_info', ['card_num', 'card_exp', 'card_cvv', 'card_pin'])
    return df

@bs.repository_call
def get_cc_account_by_client_id (client_id):
    df = car.get_cc_account_by_client_id(client_id)
    extract_card_info(df, 'cc_card_info', ['card_num', 'card_exp', 'card_cvv', 'card_pin'])
    return df

@bs.repository_call_data
def get_cc_account_data_by_client (client_id):
    df = car.get_cc_account_by_client_id(client_id)
    extract_card_info(df, 'cc_card_info', ['card_num', 'card_exp', 'card_cvv', 'card_pin'])
    return df

@bs.repository_call_single_row
def get_cc_account_by_id (id):
    df = car.get_cc_account_by_id(id)
    extract_card_info(df, 'cc_card_info', ['card_num', 'card_exp', 'card_cvv', 'card_pin'])
    return df

def post_cc_account ( in_data:dict):
    return bs.post( in_data, CcAccountModel,  car.upsert_cc_account, get_cc_account_by_id)

def delete_client_cc_account_by_id( id):
    return bs.delete( id, 'cc_account', car.delete_cc_account_by_id)
#--------------------
# cc_account_promo
#--------------------
# from CcAccountPromoModel import CcAccountPromoModel

# @bs.repository_call
# def get_cc_account_promo ():
#     return car.get_cc_account_promo()

# @bs.repository_call
# def get_cc_account_promo_by_cc_account_id (cc_account_id):
#     return car.get_cc_account_promo_by_cc_account_id(cc_account_id)

# @bs.repository_call
# def get_cc_account_promo_by_id (id):
#     return car.get_cc_account_promo_by_id(id)

# @bs.repository_call
# def post_cc_account_promo ( cc_account_promo:CcAccountPromoModel):
#     return car.upsert_cc_account_promo(cc_account_promo)

# @bs.repository_call
# def put_cc_account_promo (cc_account_promo:CcAccountPromoModel):
#     return car.insert_cc_account_promo(cc_account_promo)


