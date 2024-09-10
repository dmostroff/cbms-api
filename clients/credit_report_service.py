#--------------------
# credit_report
#--------------------
import clients.credit_report_repository as cr
import common.base_service as bs
from  models.CreditReportModel import CreditReportModel

@bs.repository_call
def get_credit_reports ():
    return cr.get_credit_reports()

@bs.repository_call_data
def get_credit_report_by_client_id (client_id):
    return cr.get_credit_report_by_client_id(client_id)

@bs.repository_call_single_row
def get_credit_report_by_id (id):
    return cr.get_credit_report_by_id(id)

def post_credit_report( in_data: dict)->dict:
    retval = bs.post( in_data, CreditReportModel, cr.upsert_credit_report, get_credit_report_by_id)
    return retval

def delete_credit_report_by_id( id):
    return bs.delete( id, 'credit_report', cr.delete_credit_report_by_id)    
