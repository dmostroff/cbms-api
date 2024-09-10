import numpy as np
import admin.auth_user_repository as ar
import admin.auth_user_setting_repository as ausr
import common.base_service as bs
from models.AuthUserModel import AuthUserModel
from models.AuthUserSettingModel import AuthUserSettingModel

# -----------
# auth_user
# -----------


@bs.repository_call
def get_auth_users():
    return ar.get_auth_users()


# @bs.repository_call
# def get_auth_user_by_auth_user_id (auth_user_id):
#     return ar.get_auth_user_by_auth_user_id(auth_user_id)


@bs.repository_call_single_row
def get_auth_user_by_id(id: int):
    return ar.get_auth_user_by_id(id)


@bs.repository_call_single_row_data
def authenticate_user(username: str, password: str):
    return ar.authenticate_user(username, password)
    # print( 'authenticate_user', username, password, retval)


@bs.repository_call_single_row_data
def get_auth_user_by_username(username: str):
    return ar.get_auth_user_by_username(username)


def upsert_auth_user(auth_user: AuthUserModel):
    df = ar.upsert_auth_user(auth_user)
    id = np.int64(df["id"].values[0]).item()
    return get_auth_user_by_id(id)


def delete_auth_user(id: int):
    df = ar.delete_auth_user(auth_user)
    id = np.int64(df["id"].values[0]).item()
    return get_auth_user_by_id(id)


####################
# AuthUserSetting
####################
@bs.repository_call
def get_auth_user_settings(user_id):
    return ausr.get_auth_user_settings(user_id)


@bs.repository_call
def get_auth_user_setting_by_user_id(user_id):
    return ausr.get_auth_user_setting_by_user_id(user_id)


@bs.repository_call
def get_auth_user_setting_by_prefix(user_id, prefix):
    return ausr.get_auth_user_setting_by_prefix(user_id, prefix)


@bs.repository_call_single_row
def get_auth_user_setting_by_id(id):
    return ausr.get_auth_user_setting_by_id(id)


def upsert_auth_user_setting(auth_user_setting: AuthUserSettingModel):
    df = ausr.upsert_auth_user_setting(auth_user_setting)
    id = np.int64(df["id"].values[0]).item()
    return get_auth_user_setting_by_id(id)


def delete_auth_user_setting_by_user(user_id):
    return ausr.delete_auth_user_setting_by_user(user_id)


@bs.repository_call_single_row
def delete_auth_user_setting(id):
    return ausr.delete_auth_user_setting(id)
