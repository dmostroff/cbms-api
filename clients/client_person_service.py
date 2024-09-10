import common.base_service as bs
#--------------------
# client_person
#--------------------
from models.ClientPersonModel import ClientPersonModel
import clients.client_person_repository as cpr

@bs.repository_call
def get_client_persons ():
    return cpr.get_client_persons()

@bs.repository_call
def get_client_person_by_client (client_id):
    return cpr.get_client_person_by_id(client_id)

@bs.repository_call_single_row_data
def get_client_person_data (client_id):
    person = cpr.get_client_person_by_id(client_id)
    return person

@bs.repository_call_single_row
def get_client_person_by_id (id):
    return cpr.get_client_person_by_id(id)

def post_client_person( in_data: dict):
    return bs.post( in_data, ClientPersonModel, cpr.upsert_client_person, get_client_person_by_id)

def delete_client_person( id):
    return bs.delete( id, 'client_person', cpr.delete_client_person_by_id)    

@bs.repository_call
def put_client_person (client_person:ClientPersonModel):
    return cpr.insert_client_person(client_person)

