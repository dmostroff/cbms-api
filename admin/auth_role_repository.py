import common.db_layer as db
from admin.admin_model import AuthRoleModel, AuthRolePermissionModel

#######################
# auth_role_permission
#######################

def get_auth_role_permission_basesql():
    sql = """
    SELECT id,role,permission
    FROM auth_role_permission
"""
    return sql

def get_auth_role_permissions():
    sql = get_auth_role_permission_basesql()
    return db.fetchall(sql)

def get_auth_role_permission_by_id(id):
    sql = get_auth_role_permission_basesql()
    sql += """
    WHERE id = %s
"""
    return db.fetchall(sql, [id])

# def get_auth_role_permission_by_auth_role_id(auth_role_id):
#     sql = get_auth_role_permission_basesql()
#     sql += """
#     WHERE auth_role_id = %s
# """
#     return db.fetchall(sql, [auth_role_id])

def upsert_auth_role_permission( auth_role_permission:AuthRolePermissionModel):
    sql = """
    WITH t AS (
        SELECT 
            %s::int as id
            , %s::text as role
            , %s::text as permission
    ),
    u AS (
        UPDATE admin.auth_role_permission
        SET 
            role=t.role
            , permission=t.permission
        FROM t
        WHERE admin.auth_role_permission.id = t.id
        RETURNING admin.auth_role_permission.id
    ),
    i AS (
        INSERT INTO admin.auth_role_permission( role,permission)
        SELECT 
            t.role
            , t.permission
        FROM t
        WHERE NOT EXISTS ( SELECT 1 FROM u)
        RETURNING admin.auth_role_permission.id
    )
    SELECT 'INSERT' as ACTION, id
    FROM i
    UNION ALL
    SELECT 'UPDATE' as ACTION, id
    FROM u
"""
    val = [
            auth_role_permission.id
            , auth_role_permission.role
            , auth_role_permission.permission
        ]
    return db.execute(sql, val)

def insert_auth_role_permission( auth_role_permission:AuthRolePermissionModel):
    sql = """
    INSERT INTO admin.auth_role_permission( role,permission)
    VALUES (%s, %s)
    ;
"""
    val = [
        auth_role_permission.role
        , auth_role_permission.permission
        ]
    return db.execute(sql, val)

# this has a flaw in loop.index > 2
def update_auth_role_permission( auth_role_permission:AuthRolePermissionModel):
    sql = """
    UPDATE admin.auth_role_permission
    SET role = %s, permission = %s
    WHERE id = %s
"""
    val = [
        auth_role_permission.role
        , auth_role_permission.permission
        , auth_role_permission.id            
        ]
    return db.execute(sql, val)

#######################
# auth_role
#######################
def get_auth_role_basesql():
    sql = """
    SELECT id,role,description
    FROM admin.auth_role
"""
    return sql

def get_auth_roles():
    sql = get_auth_role_basesql()
    return db.fetchall(sql)

def get_auth_role_by_id(id):
    sql = get_auth_role_basesql()
    sql += """
    WHERE id = %s
"""
    return db.fetchall(sql, [id])

def upsert_auth_role( auth_role:AuthRoleModel):
    sql = """
    WITH t AS (
        SELECT 
            %s::int as id
            , %s::text as role
            , %s::text as description
    ),
    u AS (
        UPDATE admin.auth_role
        SET 
            role=t.role
            , description=t.description
        FROM t
        WHERE (admin.auth_role.id = t.id) OR (admin.auth_role.role = t.role)
        RETURNING admin.auth_role.id
    ),
    i AS (
        INSERT INTO admin.auth_role( role,description)
        SELECT 
            t.role
            , t.description
        FROM t
        WHERE NOT EXISTS ( SELECT 1 FROM u)
        RETURNING admin.auth_role.id
    )
    SELECT 'INSERT' as ACTION, id
    FROM i
    UNION ALL
    SELECT 'UPDATE' as ACTION, id
    FROM u
"""
    val = [
            auth_role.id
            , auth_role.role
            , auth_role.description
        ]
    return db.fetchall(sql, val)

def insert_auth_role( auth_role:AuthRoleModel):
    sql = """
    INSERT INTO admin.auth_role( role,description)
    VALUES (%s, %s)
    RETURNING admin.auth_role.id
    ;
"""
    val = [
            auth_role.role
            , auth_role.description
        ]
    return db.execute(sql, val)

# this has a flaw in loop.index > 2
def update_auth_role( auth_role:AuthRoleModel):
    sql = """
    UPDATE admin.auth_role
    SET role= %s, description = %s
    WHERE id = %s
    RETURNING id, auth_role, description
"""
    val = [
        auth_role.role
        , auth_role.description
        , auth_role.id
        ]
    return db.execute(sql, val)
