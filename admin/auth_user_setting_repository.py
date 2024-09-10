import common.db_layer as db

#######################
# auth_user_setting
#######################
from admin.admin_model import AdmSettingModel

def get_auth_user_setting_basesql():
    sql = """
    SELECT id, user_id, prefix, keyname, keyvalue, display_rank
    FROM admin.auth_user_setting
"""
    return sql

def get_auth_user_settings():
    sql = get_auth_user_setting_basesql()
    sql += " ORDER BY prefix, display_rank"
    return db.fetchall(sql)

def get_auth_user_setting_by_user(user_id):
    sql = get_auth_user_setting_basesql()
    sql += """
    WHERE user_id = :user_id
"""
    return db.fetchall(sql, { 'user_id' : user_id })

def get_auth_user_setting_by_prefix(user_id, prefix):
    sql = get_auth_user_setting_basesql()
    sql += """
    WHERE user_id = :user_id AND prefix = :prefix
    ORDER BY display_rank
"""
    return db.fetchall(sql, { 'user_id' : user_id, 'prefix' : prefix })

def get_auth_user_setting_by_id(id):
    sql = get_auth_user_setting_basesql()
    sql += """
    WHERE id = %s
"""
    df = db.fetchall(sql, [id])
    return df.head(1)

def upsert_auth_user_setting( auth_user_setting:AdmSettingModel):
    sql = """
    WITH t AS (
        SELECT 
            :id::int as id
            , :user_id::int as user_id
            , :prefix::varchar(32) as prefix
            , :keyname::varchar(32) as keyname
            , :keyvalue::text as keyvalue
            , :display_rank::int as display_rank
    ),
    u AS (
        UPDATE admin.auth_user_setting
        SET
            prefix=t.prefix
            , keyname=t.keyname
            , keyvalue=t.keyvalue
            , display_rank = t.display_rank
        FROM t
        WHERE auth_user_setting.id = t.id
        RETURNING auth_user_setting.*
    ),
    u1 AS (
        UPDATE admin.auth_user_setting
        SET keyvalue=t.keyvalue
            , display_rank = t.display_rank
        FROM t
        WHERE auth_user_setting.user_id = t.user_id
            AND auth_user_setting.prefix = t.prefix
            AND auth_user_setting.keyname = t.keyname
            AND NOT EXISTS ( SELECT 1 FROM u)
        RETURNING auth_user_setting.*
    ),
    i AS (
        INSERT INTO admin.auth_user_setting( user_id, prefix, keyname, keyvalue, display_rank)
        SELECT 
            t.user_id
            , t.prefix
            , t.keyname
            , t.keyvalue
            , t.display_rank
        FROM t
        WHERE NOT EXISTS ( SELECT 1 FROM u)
            AND NOT EXISTS ( SELECT 1 FROM u1)
        RETURNING auth_user_setting.*
    )
    SELECT 'INSERT' as ACTION, i.id, i.user_id, i.prefix, i.keyname, i.keyvalue, i.display_rank
    FROM i
    UNION ALL
    SELECT 'UPDATE' as ACTION, u.id, u.user_id, u.prefix, u.keyname, u.keyvalue, u.display_rank
    FROM u
    UNION ALL
    SELECT 'UPDATE' as ACTION, u1.id, u1.user_id, u1.prefix, u1.keyname, u1.keyvalue, u1.display_rank
    FROM u1
"""
    val = {
            'id': auth_user_setting.id
            , 'user_id' : auth_user_setting.user_id
            , 'prefix' : auth_user_setting.prefix
            , 'keyname' : auth_user_setting.keyname
            , 'keyvalue' : auth_user_setting.keyvalue
            , 'display_rank' : auth_user_setting.display_rank
    }
    return db.fetchall(sql, val)

def insert_auth_user_setting( auth_user_setting:AdmSettingModel):
    sql = """
    INSERT INTO admin.auth_user_setting( user_id, prefix, keyname, keyvalue, display_rank)
    VALUES (:user_id, :prefix, :keyname, :keyvalue, :display_rank)
    RETURNING *
    ;
"""
    val = {
            'user_id' : auth_user_setting.user_id
            , 'prefix' : auth_user_setting.prefix
            , 'keyname' : auth_user_setting.keyname
            , 'keyvalue' : auth_user_setting.keyvalue
            , 'display_rank' : auth_user_setting.display_rank
    }
    return db.execute(sql, val)

# this has a flaw in loop.index > 2
def update_auth_user_setting_value( auth_user_setting:AdmSettingModel):
    sql = """
    UPDATE admin.auth_user_setting
    SET keyvalue = %s
    WHERE id = %s
"""
    val = [
            auth_user_setting.keyvalue
            , auth_user_setting.id
        ]
    return db.execute(sql, val)

def delete_auth_user_setting( id):
    sql = """
    DELETE FROM admin.auth_user_setting
    WHERE id = %s
    RETURNING id
"""
    return db.fetchall(sql, [ id ])

def delete_auth_user_setting_by_user( user_id):
    sql = """
    DELETE FROM admin.auth_user_setting
    WHERE user_id = %s
    RETURNING id
"""
    return db.fetchall(sql, [ user_id ])

def delete_auth_user_setting_by_prefix( auth_user_setting:AdmSettingModel):
    sql = """
    DELETE FROM admin.auth_user_setting
    WHERE user_id = %s AND prefix = %s
    RETURNING id
"""
    val = [
            auth_user_setting.user_id
            , auth_user_setting.prefix
        ]
    return db.fetchall(sql, val)
