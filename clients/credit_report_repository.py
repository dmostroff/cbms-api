import common.db_layer as db


#######################
# credit_report
#######################
from  models.CreditReportModel import CreditReportModel

def get_credit_report_basesql():
    sql = """
    SELECT id
        , client_id
        , client_code
        , credit_bureau
        , login
        , admin.f_adm_decrypt(pwd) as pwd
        , admin.f_adm_decrypt(pin) as pin
        , recorded_on
    FROM client.credit_report
"""
    return sql

def get_credit_reports():
    sql = get_credit_report_basesql()
    return db.fetchall(sql)

def get_credit_report_by_id(id):
    sql = get_credit_report_basesql()
    sql += """
    WHERE id = :id
"""
    return db.fetchone( sql, { 'id': id} )

def get_credit_report_by_client_id(client_id):
    sql = get_credit_report_basesql()
    sql += """
    WHERE client_id = :client_id
"""
    return db.fetchall(sql, { 'client_id': client_id})

def upsert_credit_report( credit_report:CreditReportModel):
    sql = """
SELECT client.f_credit_report_insert(
    :client_id
	, :client_code
	, :credit_bureau
    , :login
	, :pwd
    , :pin
	, :id
);
    """
    val = credit_report.dict()
    return db.fetchall(sql, val)
    
def delete_credit_report_by_id( id: int):
    sql = "DELETE FROM client.credit_report WHERE id = :id RETURNING id;"
    return db.fetchone( sql, { 'id': id} )