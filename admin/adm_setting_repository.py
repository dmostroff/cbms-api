import common.db_layer as db


#######################
# adm_setting
#######################
from admin.admin_model import AdmSettingModel

def get_adm_setting_basesql():
    sql = """
    SELECT id, prefix, keyname, keyvalue, display_rank
    FROM admin.adm_setting
"""
    return sql

def get_adm_settings():
    sql = get_adm_setting_basesql()
    sql += " ORDER BY prefix, display_rank"
    return db.fetchall(sql)

def get_adm_setting_by_prefix(prefix):
    sql = get_adm_setting_basesql()
    sql += """
    WHERE prefix = %s
    ORDER BY display_rank
"""
    return db.fetchall(sql, [prefix])


def get_adm_setting_by_id(id):
    sql = get_adm_setting_basesql()
    sql += """
    WHERE id = %s
"""
    df = db.fetchall(sql, [id])
    return df.head(1)

def upsert_adm_setting( adm_setting:AdmSettingModel):
    sql = """
    WITH t AS (
        SELECT 
            %s::int as id
            , %s::varchar(32) as prefix
            , %s::varchar(32) as keyname
            , %s::text as keyvalue
            , %s::int as display_rank
    ),
    u AS (
        UPDATE admin.adm_setting
        SET 
            prefix=t.prefix
            , keyname=t.keyname
            , keyvalue=t.keyvalue
            , display_rank = t.display_rank
        FROM t
        WHERE adm_setting.id = t.id
        RETURNING adm_setting.*
    ),
    u1 AS (
        UPDATE admin.adm_setting
        SET keyvalue=t.keyvalue
            , display_rank = t.display_rank
        FROM t
        WHERE adm_setting.prefix = t.prefix AND adm_setting.keyname = t.keyname
            AND NOT EXISTS ( SELECT 1 FROM u)
        RETURNING adm_setting.*
    ),
    i AS (
        INSERT INTO admin.adm_setting( prefix, keyname, keyvalue, display_rank)
        SELECT 
            t.prefix
            , t.keyname
            , t.keyvalue
            , t.display_rank
        FROM t
        WHERE NOT EXISTS ( SELECT 1 FROM u)
            AND NOT EXISTS ( SELECT 1 FROM u1)
        RETURNING adm_setting.*
    )
    SELECT 'INSERT' as ACTION, i.id, i.prefix, i.keyname, i.keyvalue, i.display_rank
    FROM i
    UNION ALL
    SELECT 'UPDATE' as ACTION, u.id, u.prefix, u.keyname, u.keyvalue, u.display_rank
    FROM u
    UNION ALL
    SELECT 'UPDATE' as ACTION, u1.id, u1.prefix, u1.keyname, u1.keyvalue, u1.display_rank
    FROM u1
"""
    val = [
            adm_setting.id
            , adm_setting.prefix
            , adm_setting.keyname
            , adm_setting.keyvalue
            , adm_setting.display_rank
        ]
    return db.fetchall(sql, val)

def insert_adm_setting( adm_setting:AdmSettingModel):
    sql = """
    INSERT INTO admin.adm_setting( prefix,keyname,keyvalue)
    VALUES (%s, %s, %s)
    RETURNING *
    ;
"""
    val = [
            adm_setting.prefix
            , adm_setting.keyname
            , adm_setting.keyvalue
        ]
    return db.execute(sql, val)

# this has a flaw in loop.index > 2
def update_adm_setting( adm_setting:AdmSettingModel):
    sql = """
    UPDATE admin.adm_setting
    SET sprefix = %s, keyname = %s, keyvalue = %s
    WHERE id = %s
"""
    val = [
            adm_setting.prefix
            , adm_setting.keyname
            , adm_setting.keyvalue
            , adm_setting.id
        ]
    return db.execute(sql, val)

def delete_auth_user_setting( id):
    sql = """
    DELETE admin.adm_setting
    WHERE id = %s
    RETURNING id
"""
    return db.fetchall(sql, [ id ])

def delete_adm_setting_by_prefix( prefix):
    sql = """
    DELETE FROM admin.adm_setting
    WHERE prefix = %s
    RETURNING id
"""
    return db.fetchall(sql, [ prefix ])
