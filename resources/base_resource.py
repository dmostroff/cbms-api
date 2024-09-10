from flask import current_app
from flask import request
from flask_restful import Resource
from common.common_service import json_rc_msg
import clients.client_loan_service as cs


class BaseResource(Resource):
    def no_func(self, my_data: dict):
        pass

    def get(self, id, get_func):
        return get_func(id)

    def post(self, id=0, post_func=no_func):
        retval = json_rc_msg( -1, "No msg")
        try:
            retval = post_func( request.get_json())
        except Exception as ex:
            current_app.logger.error( repr(ex))
            retval = json_rc_msg( -1, f"Error: {self.__class__.__name__} {request.method} {request.path}", repr(ex))
        finally:
            return retval

    def delete(self, id=0, del_func=no_func):
        retval = json_rc_msg( -1, "No msg")
        try:
            retval = del_func( id)
        except Exception as ex:
            current_app.logger.error( repr(ex))
            retval = json_rc_msg( -1, f"Error: {self.__class__.__name__} {request.method} {request.path}", repr(ex))
        finally:
            return retval
