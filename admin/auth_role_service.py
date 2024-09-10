import numpy as np
import admin.auth_role_repository as ar
import common.base_service as bs
from admin.admin_model import AuthRolePermissionModel
from admin.admin_model import AuthRoleModel


#--------------------
# auth_role_permission
#--------------------

@bs.repository_call
def get_auth_role_permissions ():
    return ar.get_auth_role_permissions()

# @bs.repository_call
# def get_auth_role_permission_by_auth_role_id (auth_role_id):
#     return ar.get_auth_role_permission_by_auth_role_id(auth_role_id)

@bs.repository_call_single_row
def get_auth_role_permission_by_id (id):
    return ar.get_auth_role_permission_by_id(id)

def upsert_auth_role_permission ( auth_role_permission:AuthRolePermissionModel):
    df = ar.upsert_auth_role_permission(auth_role_permission)
    id = np.int64(df['id'].values[0]).item()
    return get_auth_role_permission_by_id(id)


#--------------------
# auth_role
#--------------------

@bs.repository_call
def get_auth_roles ():
    return ar.get_auth_roles()

# @bs.repository_call
# def get_auth_role_by_auth_role_id (auth_role_id):
#     return ar.get_auth_role_by_auth_role_id(auth_role_id)

@bs.repository_call_single_row
def get_auth_role_by_id (id):
    return ar.get_auth_role_by_id(id)

def upsert_auth_role ( auth_role:AuthRoleModel):
    df = ar.upsert_auth_role(auth_role)
    id = np.int64(df['id'].values[0]).item()
    return get_auth_role_by_id(id)

