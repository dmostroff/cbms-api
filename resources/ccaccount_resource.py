from flask import current_app
import traceback
from flask import request
from flask_restful import Resource
from resources.base_resource import BaseResource
import clients.cc_account_service as cas
from common.common_service import json_rc_msg


ccAccount = {}
class CcAccounts(Resource):
    def get(self):
        return cas.get_cc_account()

class CcAccountsByClient(Resource):
    def get(self, client_id):
        return cas.get_cc_account_by_client_id(client_id)

class CcAccount(BaseResource):
    def get(self, id):
        return super().get(id)

    def post(self, id=0):
        return super().post(id, cas.post_cc_account)

    def delete( self, id):
        return cas.delete_client_cc_account_by_id(id)

# ccAccount = {}
# class CcAccounts(Resource):
#     def get(self):
#         return cas.get_cc_account()

# class CcAccountsByClient(Resource):
#     def get(self, client_id):
#         return cas.get_cc_account_by_client_id(client_id)

# class CcAccount(Resource):
#     def get(self, id):
#         return cas.get_cc_account_by_id(id)

#     def post(self, id=0):
#         retval = json_rc_msg( -1, "No msg")
#         try:
#             retval = cas.post_cc_account( request.get_json())
#         except Exception as ex:
#             current_app.logger.error(repr(ex))
#             retval = json_rc_msg( -1, f"Error: {request.method} {request.path}", repr(ex))
#             # raise ex
#         finally:
#             return retval
