import common.db_layer as db

#######################
# auth_user
#######################
from models.AuthUserModel import AuthUserModel


def get_auth_user_basesql():
    sql = """
    SELECT id
        , username
        , password
        , first_name
        , last_name
        , email
        , is_superuser
        , is_staff
        , is_active
        , password_hint
        , array_to_string(roles, ',') as roles
        , recorded_on
    FROM admin.auth_user
"""
    return sql

def authenticate_user( username, password):
    sql = get_auth_user_basesql()
    sql += """
    WHERE username = :username
        AND password is NOT NULL 
        AND password = :password
"""
    return db.fetchall(sql, { 'username': username, 'password': password })

def get_auth_users():
    sql = get_auth_user_basesql()
    return db.fetchall(sql)

def get_auth_user_by_id(id):
    sql = get_auth_user_basesql()
    sql += """
    WHERE id = :id
"""
    return db.fetchall(sql, { 'id': id})

def get_auth_user_by_username(username):
    sql = get_auth_user_basesql()
    sql += """
    WHERE username = :username
"""
    return db.fetchall(sql, { 'username': username })

# def get_auth_user_by_auth_user_id(auth_user_id):
#     sql = get_auth_user_basesql()
#     sql += """
#     WHERE auth_user_id = %s
# """
#     return db.fetchall(sql, [auth_user_id])

def upsert_auth_user( auth_user:AuthUserModel):
    sql = """
SELECT admin.f_adm_auth_user_insert(
    %(first_name)s::varchar
    , %(last_name)s::varchar
    , %(email)s::varchar
    , %(username)s::varchar
    , %(password)s::varchar
    , %(password_hint)s::varchar
    , %(is_superuser)s::varchar
    , %(is_staff)s::varchar
    , %(is_active)s::varchar
    , %(roles)s::varchar
    , %(recorded_on)s::varchar
    , %(id)s::varchar
);
"""
    v = auth_user.dict()
    return db.fetchone(sql, v)
