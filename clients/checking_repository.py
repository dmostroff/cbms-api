# import pgsql_db_layer as db
import common.db_layer as db


#######################
# checking
#######################
from models.CheckingModel import CheckingModel

def get_checking_basesql():
    sql = """
    SELECT id
        , client_id
        , xero_id
        , xero_main
        , client_code
        , client_code_additional
        , name_on_account
        , account_status
        , admin.f_adm_setting_get('ACCOUNTSTATUS', account_status) AS account_status_desc
        , device
        , open_date
        , login
        , admin.f_adm_decrypt(pwd) as pwd
        , bank
        , routing
        , account
        , member_number
        , admin.f_adm_decrypt(debit_card_info) as debit_card_info
        , admin.f_adm_decrypt(phone_pin) as phone_pin
        , reconciled_on
        , zelle
        , wise
        , wise_device
        , checking_info
        , task
        , notes
        , recorded_on
  FROM client.checking
"""
    return sql

def get_checkings():
    sql = get_checking_basesql()
    return db.fetchall(sql)

def get_checking_by_id(id):
    sql = get_checking_basesql()
    sql += """
    WHERE id = :id
"""
    return db.fetchall(sql, { 'id': id} )

def get_checking_by_client_id(client_id):
    sql = get_checking_basesql()
    sql += """
    WHERE client_id = :client_id
"""
    return db.fetchall(sql, { 'client_id': client_id })

def upsert_checking( checking:CheckingModel):
    sql = """
SELECT client.f_checking_insert(
    :xero_id
    , :xero_main
    , :client_id
    , :client_code
    , :client_code_additional
    , :name_on_account
    , :account_status
    , :device
    , CAST(:open_date AS VARCHAR(10))
    , :login
    , :pwd
    , :bank
    , :routing
    , :account
    , :member_number
    , :debit_card_num
    , :debit_card_exp
    , :debit_card_cvv
    , :debit_card_pin
    , :phone_pin
    , CAST(:reconciled_on AS VARCHAR(10))
    , :zelle
    , :wise
    , :wise_device
    , :notes
    , :task
    , :id
    );
"""
    val = checking.dict()
    return db.fetchall(sql, val)

def insert_checking( checking:CheckingModel):
    return upsert_checking( checking)

def delete_checking_by_id( id: int):
    sql = "DELETE FROM client.checking WHERE id = :id RETURNING id;"
    return db.fetchone( sql, { 'id': id} )