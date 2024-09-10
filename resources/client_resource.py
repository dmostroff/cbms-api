from flask import current_app
import traceback
from flask_restful import Resource
from common.common_service import json_rc_msg
import clients.client_service as cs
import clients.client_person_service as cps
import clients.client_address_service as cads
import clients.cc_account_service as cas
import clients.client_israel_service as cis
import clients.cc_account_todo_service as cats
import clients.client_loan_service as cls
import clients.credit_report_service as crs
import clients.checking_service as checks
import clients.credit_line_history_service as clhs

from clients.client_transform import ClientPersonJsonToModel, clientData

class Client(Resource):
    def get(self, id):
        try:
            client_person = cps.get_client_person_data(id)
            credit_summary = cs.get_client_credit_summary_by_client( id)
            address = cads.get_client_address_by_client (id)
            cc_account = cas.get_cc_account_data_by_client(id)
            loan = cls.get_client_loan_by_client_id(id)
            credit_report = crs.get_credit_report_by_client_id(id)
            client_israel = cis.get_client_israel_by_client (id)
            checking = checks.get_checking_by_client_id(id)
            credit_line_history = clhs.get_credit_line_history_by_client_id( id)
            # cc_account_todo = cats.get_cc_account_todo_by_client(id)
            # bt = cs.get_client_cc_balance_transfer_by_client_id (id)
            data = clientData( 
                person = client_person
                , credit_summary = credit_summary
                , address = address
                , client_israel = client_israel
                , cc_account = cc_account
                , loan = loan
                , credit_report = credit_report
                , checking = checking
                , credit_line_history = credit_line_history
                # cc_account_todo = cc_account_todo
                # , balance_transfer = bt
                )
            retval = json_rc_msg( 1, 'Success', data)
        except Exception as ex:
            current_app.logger.error( f"{__name__} {repr(ex)}")
            current_app.logger.error( traceback.format_exc())
            retval = json_rc_msg( -1, "Error", repr(ex))
        finally:
            return retval
