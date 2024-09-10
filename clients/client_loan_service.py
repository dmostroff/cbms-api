import common.base_service as bs
import clients.client_loan_repository as clr
from models.ClientLoanModel import ClientLoanModel


#--------------------
# client_loan
#--------------------

@bs.repository_call
def get_client_loans ():
    return clr.get_client_loans()

# @bs.repository_call
# def get_client_loan_by_client_loan_id (client_loan_id):
#     return cr.get_client_loan_by_client_loan_id(client_loan_id)

@bs.repository_call_data
def get_client_loan_by_client_id ( client_id):
    return clr.get_client_loan_by_client_id(client_id)

@bs.repository_call_single_row
def get_client_loan_by_id (id):
    return clr.get_client_loan_by_id(id)

def post_client_loan( in_data: dict):
    return bs.post( in_data, ClientLoanModel, clr.upsert_client_loan, get_client_loan_by_id)

def delete_client_loan_by_id( id):
    return bs.delete( id, 'client_loan', clr.delete_client_loan_by_id)