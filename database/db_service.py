import common.base_service as bs
import database.db_repository as dr

@bs.repository_call_single_row
def get_database_name():
    return dr.get_database_name()

@bs.repository_call_single_row
def get_version():
    return dr.get_version()

@bs.repository_call_single_row
def get_connection_info():
    return dr.get_connection_info()

@bs.repository_call_single_row
def get_server_name():
    return dr.get_server_name()

