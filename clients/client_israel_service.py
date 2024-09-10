import common.base_service as bs
from common.common_service import json_rc_msg
import clients.client_israel_repository as cr
from models.ClientIsraelModel import ClientIsraelModel

#--------------------
# client_israel
#--------------------

@bs.repository_call
def get_client_israels ():
    return cr.get_client_israels()

# @bs.repository_call
# def get_client_israel_by_client_israel_id (client_israel_id):
#     return cr.get_client_israel_by_client_israel_id(client_israel_id)

@bs.repository_call_data
def get_client_israel_by_client (client_id):
    return cr.get_client_israel_by_client_id(client_id)

@bs.repository_call_single_row
def get_client_israel_by_id (id):
    return cr.get_client_israel_by_id(id)

def post_client_israel( in_data: dict):
    return bs.post( in_data, ClientIsraelModel, cr.upsert_client_israel, get_client_israel_by_id)

@bs.repository_call_array
def get_bank_names():
    return cr.get_bank_names()

def delete_client_israel_by_id( id):
    return bs.delete( id, 'client_israel', cr.delete_client_israel_by_id)
