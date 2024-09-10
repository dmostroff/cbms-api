import common.base_service as bs
from common.common_service import extract_card_info
import clients.checking_repository as cr
from models.CheckingModel import CheckingModel

#--------------------
# checking
#--------------------

@bs.repository_call
def get_checkings ():
    return cr.get_checkings()

# @bs.repository_call
# def get_checking_by_checking_id (checking_id):
#     return cr.get_checking_by_checking_id(checking_id)

@bs.repository_call_single_row
def get_checking_by_id (id):
    df = cr.get_checking_by_id(id)
    extract_card_info(df, 'debit_card_info', ['debit_card_num', 'debit_card_exp', 'debit_card_cvv', 'debit_card_pin'])
    return df

@bs.repository_call_data
def get_checking_by_client_id ( client_id):
    df = cr.get_checking_by_client_id(client_id)
    extract_card_info(df, 'debit_card_info', ['debit_card_num', 'debit_card_exp', 'debit_card_cvv', 'debit_card_pin'])
    return df

def post_checking( in_data: dict):
    return bs.post( in_data, CheckingModel,  cr.upsert_checking, get_checking_by_id)

def delete_checking_by_id( id):
    return bs.delete( id, 'checking', cr.delete_checking_by_id)
