from flask import current_app
from flask import request
from flask_restful import Resource
from common.common_service import json_rc_msg
# import cc_account_todo_service as cs

# class CcAccountTodos(Resource):
#     def get(self):
#         return cs.get_cc_account_todos()

# class CcAccountTodoByClient(Resource):
#     def get(self, client_id):
#         return cs.get_cc_account_todo_by_client(client_id)

# class CcAccountTodoByCcAccount(Resource):
#     def get(self, cc_account_id):
#         return cs.get_cc_account_todo_by_cc_account(cc_account_id)

# class CcAccountTodo(Resource):
#     def get(self, id):
#         return cs.get_cc_account_todo_by_id(id)

#     def post(self, id=0):
#         retval = json_rc_msg( -1, "cc_account_todo")
#         try:
#             retval = cs.post_cc_account_todo( request.get_json())
#         except Exception as ex:
#             current_app.logger.error( repr(ex))
#             retval = json_rc_msg( -1, "error", repr(ex))
#         finally:
#             return retval

# class CcAccountTodoPost(Resource):
#     def post(self):
#         return 
