from flask import current_app
import traceback
import numpy as np
import common.base_service as bs
import clients.credit_line_history_repository as clhr
from  models.CreditLineHistoryModel import CreditLineHistoryModel


#--------------------
# credit_line_history
#--------------------

@bs.repository_call
def get_credit_line_histories ():
    return clhr.get_credit_line_histories()

@bs.repository_call_data
def get_credit_line_history_by_client_id (client_id):
    return clhr.get_credit_line_history_by_client_id(client_id)

@bs.repository_call_data
def get_credit_line_history_by_card_id (card_id):
    return clhr.get_credit_line_history_by_card_id(card_id)

@bs.repository_call_single_row
def get_credit_line_history_by_id (id):
    return clhr.get_credit_line_history_by_id(id)

def post_credit_line_history( in_data: dict):
    return bs.post( in_data, CreditLineHistoryModel, clhr.upsert_credit_line_history, get_credit_line_history_by_id)

def delete_credit_line_history_by_id( id):
    return bs.delete( id, 'credit_line_history', clhr.delete_credit_line_history_by_id)    
