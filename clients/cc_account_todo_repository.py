import common.db_layer as db

#######################
# cc_account_todo
#######################
from models.CcAccountTodoModel import CcAccountTodoModel

def get_cc_account_todo_basesql():
    sql = """
    SELECT id,client_id,cc_account_id,task,description,assigned_to,due_on,recorded_on
    FROM client.cc_account_todo
"""
    return sql

def get_cc_account_todos():
    sql = get_cc_account_todo_basesql()
    return db.fetchall(sql)

def get_cc_account_todo_by_id(id):
    sql = get_cc_account_todo_basesql()
    sql += """
    WHERE id = %s
"""
    return db.fetchall(sql, [id])

def get_cc_account_todo_by_cc_account_id(cc_account_id):
    sql = get_cc_account_todo_basesql()
    sql += """
    WHERE cc_account_id = %s
"""
    return db.fetchall(sql, [cc_account_id])

def get_cc_account_todo_by_client_id(client_id):
    sql = get_cc_account_todo_basesql()
    sql += """
    WHERE client_id = %s
"""
    return db.fetchall(sql, [client_id])

def upsert_cc_account_todo( cc_account_todo:CcAccountTodoModel):
    sql = """
    WITH t AS (
        SELECT 
            %s::integer as id
            , %s::integer as client_id
            , %s::integer as cc_account_id
            , %s::character varying as task
            , %s::text as description
            , %s::character varying as assigned_to
            , %s::timestamp with time zone as due_on
            , CURRENT_TIMESTAMP as recorded_on
    ),
    u AS (
        UPDATE client.cc_account_todo
        SET 
            client_id=t.client_id
            , cc_account_id=t.cc_account_id
            , task=t.task
            , description=t.description
            , assigned_to=t.assigned_to
            , due_on=t.due_on
            , recorded_on=t.recorded_on
        FROM t
        WHERE cc_account_todo.id = t.id
        RETURNING cc_account_todo.*
    ),
    i AS (
        INSERT INTO client.cc_account_todo (
            client_id
            , cc_account_id
            , task
            , description
            , assigned_to
            , due_on
            , recorded_on
            )
        SELECT 
            t.client_id
            , t.cc_account_id
            , t.task
            , t.description
            , t.assigned_to
            , t.due_on
            , t.recorded_on
        FROM t
        WHERE NOT EXISTS ( SELECT 1 FROM u)
        RETURNING cc_account_todo.*
    )
    SELECT 'INSERT' as ACTION, i.*
    FROM i
    UNION ALL
    SELECT 'UPDATE' as ACTION, u.*
    FROM u
"""
    val = [
        cc_account_todo.id
        , cc_account_todo.client_id
        , cc_account_todo.cc_account_id
        , cc_account_todo.task
        , cc_account_todo.description
        , cc_account_todo.assigned_to
        , cc_account_todo.due_on
        ]
    return db.fetchall(sql, val)

def insert_cc_account_todo( cc_account_todo:CcAccountTodoModel):
    sql = """
    INSERT INTO cc_account_todo( client_id,cc_account_id,task,description,assigned_to,due_on)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING *
    ;
"""
    val = [
        cc_account_todo.client_id
        , cc_account_todo.cc_account_id
        , cc_account_todo.task
        , cc_account_todo.description
        , cc_account_todo.assigned_to
        , cc_account_todo.due_on
        ]
    return db.fetchone(sql, val)

# this has a flaw in loop.index > 2
def update_cc_account_todo( cc_account_todo:CcAccountTodoModel):
    sql = """
    UPDATE client.cc_account_todo
    SET client_id = %s
        , cc_account_id = %s
        , task = %s
        , description = %s
        , assigned_to = %s
        , due_on = %s
        , recorded_on = CURRENT_TIMESTAMP
    WHERE id = %s
    RETURNING *
"""
    val = [
        cc_account_todo.client_id
        , cc_account_todo.cc_account_id
        , cc_account_todo.task
        , cc_account_todo.description
        , cc_account_todo.assigned_to
        , cc_account_todo.due_on
        , cc_account_todo.id            
        ]
    return db.fetchone(sql, val)
