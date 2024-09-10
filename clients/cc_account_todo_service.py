import clients.cc_account_todo_repository as cr
import common.base_service as bs

from models.CcAccountTodoModel import CcAccountTodoModel

#--------------------
# cc_account_todo
#--------------------

@bs.repository_call
def get_cc_account_todos ():
    return cr.get_cc_account_todos()

@bs.repository_call_data
def get_cc_account_todo_by_client (client_id):
    return cr.get_cc_account_todo_by_client_id(client_id)

@bs.repository_call_data
def get_cc_account_todo_by_cc_account (cc_account_id):
    return cr.get_cc_account_todo_by_cc_account_id(cc_account_id)

@bs.repository_call_single_row
def get_cc_account_todo_by_id (id):
    return cr.get_cc_account_todo_by_id(id)

@bs.repository_call
def post_cc_account_todo ( cc_account_todo:CcAccountTodoModel):
    return cr.cr.upsert_cc_account_todo(cc_account_todo)

