import common.base_service as bs
#--------------------
# client_address
#--------------------
import clients.client_address_repository as car
from models.ClientAddressModel import ClientAddressModel

@bs.repository_call_data
def get_client_address_by_client (client_id):
    return car.get_client_address_by_client_id(client_id)

@bs.repository_call_single_row
def get_client_address_by_id (id):
    return car.get_client_address_by_id(id)

@bs.repository_call
def get_client_addresses_by_client_id (client_id):
    return car.get_client_address_by_client_id(client_id)

def post_client_address ( in_data:dict):
    retval = bs.post( in_data, ClientAddressModel, car.upsert_client_address, get_client_address_by_id)
    if in_data.get('is_current', False):
        set_current_address( in_data)
    return retval

def delete_client_address_by_id( id):
    return bs.delete( id, 'client_address', car.delete_client_address_by_id)

@bs.repository_call
def set_current_address(in_data:dict):
    return car.set_current_address(in_data)