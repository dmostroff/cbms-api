from flask import current_app
import traceback
from common.common_service import json_rc_msg
import json
from pydantic import BaseModel
from pandas import DataFrame
import numpy as np
from typing import Callable



def repository_call( func):
    def with_repository_call(*args, **kwargs):
        try:
            df = func(*args, **kwargs)
            dfjson = df.to_json(orient="records", date_format="iso")
            data = json.loads(dfjson)
            return json_rc_msg( 1, 'Success', data)
        except Exception as ex:
            current_app.logger.error( repr(ex))
            raise ex
    return with_repository_call

def repository_call_array( func):
    def with_repository_call(*args, **kwargs):
        try:
            df = func(*args, **kwargs)
            dfjson = df.to_json(orient="columns", date_format="iso")
            data = json.loads(dfjson)
            return json_rc_msg( 1, 'Success', data)
        except Exception as ex:
            current_app.logger.error( repr(ex))
            raise ex
    return with_repository_call

def repository_call_data( func):
    def with_repository_call(*args, **kwargs):
        try:
            df = func(*args, **kwargs)
            dfjson = df.to_json(orient="records", date_format="iso")
            data = json.loads(dfjson)
            return data
        except Exception as ex:
            current_app.logger.error( repr(ex))
            raise ex
    return with_repository_call

def repository_call_single_row( func):
    def with_repository_call(*args, **kwargs):
        retval = json_rc_msg( 0, __file__)
        try:
            df = func(*args, **kwargs)
            if df is not None and not df.empty:
                dfjson = df.to_json(orient="records", date_format="iso")
                data = json.loads(dfjson)
                retval = json_rc_msg( 1, 'Success', data[0])
            else:
                retval = json_rc_msg( 1, 'No data')
        except Exception as ex:
            current_app.logger.error( repr(ex))
            raise ex
        finally:
            return retval
    return with_repository_call
# print( 'base_service')

def repository_call_single_row_data( func):
    def with_repository_call(*args, **kwargs):
        retval = None
        try:
            df = func(*args, **kwargs)
            if df is not None:
                # retval = df.to_dict(orient="records")[0] if df.shape[0] > 0 else None
                dfjson = df.to_json(orient="records", date_format="iso")
                data = json.loads(dfjson)
                retval = data[0] if len(data) > 0 else None
        except Exception as ex:
            current_app.logger.error( repr(ex))
            raise ex
        finally:
            return retval
    return with_repository_call

def repository_tuple_call( func):
    def with_repository_call(*args, **kwargs):
        retval = json_rc_msg( 0, __name__)
        try:
            df = func(*args, **kwargs)
            dfjson = df.to_json(orient="records", date_format="iso")
            data = json.loads(dfjson)
            retval = json_rc_msg( 1, 'Success', data)
        except Exception as ex:
            current_app.logger.error( repr(ex))
            raise ex
        finally:
            return retval
    return with_repository_call

def execute_no_return( func):
    def with_repository_call(*args, **kwargs):
        funcargs = {}
        if len(args) > 0:
            funcargs['args'] = [ arg for arg in args]
        if len(kwargs) > 0:
            funcargs.update( { k: v for k, v in kwargs.items() })
        retval = json_rc_msg( 0, __name__, funcargs)
        try:
            funcretval = func(*args, **kwargs)
            funcargs.update( funcretval)
            retval = json_rc_msg( 1, 'Success', funcargs)
        except Exception as ex:
            funcargs['error'] = repr(ex)
            current_app.logger.error( repr(ex))
            retval = json_rc_msg( -1, 'Error', funcargs)
        finally:
            return retval
    return with_repository_call

def post( in_data: dict, data_model: BaseModel, upsert_func: Callable[[BaseModel], DataFrame], get_data_by_id: Callable[[int], dict]):
    retval = None
    try:
        mydata = data_model.parse_obj( in_data)
        df = upsert_func( mydata)
        if df is not None and df.shape[0] > 0:
            id = np.int64(df[df.columns[0]][0]).item()
            retval = get_data_by_id(id)
    except Exception as ex:
        current_app.logger.error( in_data)
        current_app.logger.error( traceback.format_exc())
    finally:
        return retval

def delete( id: int, entity_name: str, delete_func: Callable[[int], DataFrame]):
    deletemsg = { "Action": "Delete", "Item": entity_name }
    try:
        df = delete_func( id)
        if df.shape[0] > 0:
            dfretval = df.to_dict()
            dfretval['id'] = [ v for k, v in dfretval['id'].items()]
            if len(dfretval['id']) == 1:
                dfretval['id'] = dfretval['id'][0] 
            deletemsg.update( { 'retval': dfretval} )
        else:
            deletemsg.update( { 'retval': f"Not found {id}" } )
        retval = json_rc_msg( 1, 'Success', deletemsg)
    except Exception as ex:
        deletemsg['error'] = repr(ex)
        current_app.logger.error( repr(ex))
        retval = json_rc_msg( -1, 'Error', deletemsg)
    finally:
        return retval
