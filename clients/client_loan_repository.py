import common.db_layer as db


#######################
# client_loan
#######################
from models.ClientLoanModel import ClientLoanModel

def get_client_loan_basesql():
    sql = """
    SELECT id
        , client_id
        , xero_id
        , client_code
        , first_name
        , last_name
        , card_name
        , loan_status
        , device
        , open_date -- to_char(open_date, 'MM/DD/YYYY') as open_date
        , login
        , admin.f_adm_decrypt( pwd) as pwd
        , loan_number
        , reconciled_on -- to_char(reconciled_on, 'MM/DD/YYYY') as reconciled_on
        , credit_line
        , autopay_account
        , due_on -- to_char(due_on, 'MM/DD/YYYY') as due_on
        , loan_type
        , maturity_on
        , loan_info
        , task
        , notes
        , recorded_on
    FROM client.loan
"""
    return sql


def get_client_loans():
    sql = get_client_loan_basesql()
    return db.fetchall(sql)


def get_client_loan_by_id(id):
    sql = get_client_loan_basesql()
    sql += """
    WHERE id = :id
"""
    return db.fetchone( sql, { 'id': id} )

def get_client_loan_by_client_id(client_id):
    sql = get_client_loan_basesql()
    sql += """
    WHERE client_id = :client_id
"""
    return db.fetchall(sql, { 'client_id': client_id})


def upsert_client_loan(client_loan: ClientLoanModel):
    sql = """
SELECT client.f_loan_insert(
	:xero_id
    , :client_id
	, :client_code
	, :first_name
	, :last_name
    , :card_name
    , :loan_status
	, :device
    , CAST( :open_date as varchar)
    , :login
	, :pwd
	, :loan_number
	, CAST( :reconciled_on AS varchar)
	, :credit_line
    , :autopay_account
	, :due_on
	, :loan_type
	, :maturity_on
    , :loan_info
    , :task
    , :notes
	, CAST( :id as integer)
    );
"""
    val = client_loan.dict()
    return db.fetchone(sql, val)


def delete_client_loan_by_id( id: int):
    sql = "DELETE FROM client.client_loan WHERE id = :id RETURNING id;"
    return db.fetchone( sql, { 'id': id})