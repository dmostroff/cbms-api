from flask import current_app
import traceback
from pydantic import ValidationError
from models.CcAccountTodoModel import CcAccountTodoModel
from models.ClientPersonModel import ClientPersonModel
from models.CreditReportModel import CreditReportModel
from models.CreditLineHistoryModel import CreditLineHistoryModel



def JsonToModel():
    pass

def ClientPersonJsonToModel( client_person_dict: dict) -> ClientPersonModel:
    return ClientPersonModel.parse_obj( client_person_dict)

def CcAccountTodoJsonToModel( cc_account_todo_dict: str) -> CcAccountTodoModel:
    return CcAccountTodoModel.parse_obj( cc_account_todo_dict)

def CreditReportJsonToModel( client_loan_dict: str) -> CreditReportModel:
    return CreditReportModel.parse_obj( client_loan_dict)

def CreditLineHistoryJsonToModel( credit_line_dict: dict) -> CreditLineHistoryModel:
    return CreditLineHistoryModel.parse_obj( credit_line_dict)

# assemble all the client data into one json
def clientData( **kwargs):
    return { key: value for key, value in kwargs.items() }
