import numpy as np
import admin.adm_setting_repository as ar
import common.base_service as bs

#--------------------
# adm_setting
#--------------------
from admin.admin_model import AdmSettingModel

@bs.repository_call
def get_adm_settings ():
    return ar.get_adm_settings()

@bs.repository_call
def get_adm_setting_by_prefix (prefix):
    return ar.get_adm_setting_by_prefix(prefix)

@bs.repository_call_single_row
def get_adm_setting_by_id (id):
    return ar.get_adm_setting_by_id(id)

@bs.repository_call_single_row
def upsert_adm_setting ( adm_setting:AdmSettingModel):
    return ar.upsert_adm_setting(adm_setting)

def delete_adm_setting ( id):
    df = ar.delete_adm_setting(id)
    return np.int64(df['id'].values[0]).item()

@bs.repository_call
def delete_adm_setting_by_prefix ( prefix):
    return ar.delete_adm_setting_by_prefix(prefix)

