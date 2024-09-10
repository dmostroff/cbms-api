import common.db_layer as db


#######################
# credit line history
#######################
from models.CreditLineHistoryModel import CreditLineHistoryModel

def get_credit_line_history_base_sql():
    sql = """
	SELECT id
        , client_id
        , client_code
        , card_id
        , xero_id
        , CAST( cl_date AS date) AS cl_date
        , amount
        , cl_status
        , admin.f_adm_setting_get('CREDITLINESTATUS', cl_status) AS cl_status_desc
        , notes
        , cl_info
        , recorded_on
	FROM client.credit_line_history
"""
    return sql

def get_credit_line_histories():
    sql = get_credit_line_history_base_sql()
    sql += "ORDER BY card_id, client_id, cl_date"
    return db.fetchall(sql)

def get_credit_line_history_by_id(id):
    sql = get_credit_line_history_base_sql()
    sql += """
    WHERE id = :id
"""
    return db.fetchone( sql, { 'id': id} )

def get_credit_line_history_by_client_id(client_id: int):
    sql = get_credit_line_history_base_sql()
    sql += "WHERE client_id = :client_id"
    sql += " ORDER BY card_id, cl_date"
    return db.fetchall(sql, { 'client_id': client_id})

def get_credit_line_history_by_card_id(card_id: int):
    sql = get_credit_line_history_base_sql()
    sql += "WHERE card_id = :card_id"
    sql += " ORDER BY client_id, cl_date"
    return db.fetchall(sql, {'card_id': card_id})

def upsert_credit_line_history( credit_line_history:CreditLineHistoryModel):
    sql = """
SELECT client.f_credit_line_history_insert(
    :client_id
    , :client_code
    , :xero_id
    , :cl_date
    , :amount
    , :cl_status
    , :notes
    , :cl_info
    , :id
    );
"""
    val = credit_line_history.dict()
    return db.fetchall(sql, val)


def delete_credit_line_history_by_id( id: int):
    sql = """
    DELETE FROM client.credit_line_history
    WHERE id = :id
    RETURNING id
"""
    return db.fetchone( sql, { 'id': id} )
  


# print( 'client_repository')