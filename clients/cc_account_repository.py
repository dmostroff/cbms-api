import common.db_layer as db

#######################
# cc_account_promo
#######################
from models.CcAccountPromoModel import CcAccountPromoModel

def get_cc_account_promo_basesql():
    sql = """
    SELECT promo_id,cc_account_id,offer,loan_amt,bal_transfer_date,bal_transfer_amt,promo_info,recorded_on
    FROM client.cc_account_promo
"""
    return sql

def get_cc_account_promo():
    sql = get_cc_account_promo_basesql()
    return db.fetchall(sql)

def get_cc_account_promo_by_id(id):
    sql = get_cc_account_promo_basesql()
    sql += """
    WHERE promo_id = %s
"""
    return db.fetchall(sql, [id])

def get_cc_account_promo_by_client_id(client_id):
    sql = get_cc_account_promo_basesql()
    sql += """
    WHERE client_id = %s
"""
    return db.fetchall(sql, [client_id])

def upsert_cc_account_promo( cc_account_promo:CcAccountPromoModel):
    sql = """
    WITH t AS (
        SELECT 
            %s as promo_id
            , %s as cc_account_id
            , %s as offer
            , %s as loan_amt
            , %s as bal_transfer_date
            , %s as bal_transfer_amt
            , %s as promo_info
            , CURRENT_TIMESTAMP as recorded_on
    ),
    u AS (
        UPDATE client.cc_account_promo
        SET 
            cc_account_id=t.cc_account_id
            , offer=t.offer
            , loan_amt=t.loan_amt
            , bal_transfer_date=t.bal_transfer_date
            , bal_transfer_amt=t.bal_transfer_amt
            , promo_info=t.promo_info
            , recorded_on=t.recorded_on
        FROM t
        WHERE cc_account_promo.promo_id = t.promo_id
        RETURNING cc_account_promo.*
    ),
    i AS (
        INSERT INTO client.cc_account_promo( cc_account_id,offer,loan_amt,bal_transfer_date,bal_transfer_amt,promo_info,recorded_on)
        SELECT 
            t.cc_account_id
            , t.offer
            , t.loan_amt
            , t.bal_transfer_date
            , t.bal_transfer_amt
            , t.promo_info
            , t.recorded_on
        FROM t
        WHERE NOT EXISTS ( SELECT 1 FROM u)
        RETURNING cc_account_promo.*
    )
    SELECT 'INSERT' as ACTION, i.*
    FROM i
    UNION ALL
    SELECT 'UPDATE' as ACTION, u.*
    FROM u
"""
    val = [
            cc_account_promo.promo_id
            , cc_account_promo.id
            , cc_account_promo.offer
            , cc_account_promo.loan_amt
            , cc_account_promo.bal_transfer_date
            , cc_account_promo.bal_transfer_amt
            , cc_account_promo.promo_info
            , cc_account_promo.recorded_on
        ]
    return db.execute(sql, val)

def insert_cc_account_promo( cc_account_promo:CcAccountPromoModel):
    sql = """
    INSERT INTO client.cc_account_promo(
        cc_account_id
        ,offer
        ,loan_amt
        ,bal_transfer_date
        ,bal_transfer_amt
        ,promo_info
        ,recorded_on
        )
    VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
    ;
"""
    val = cc_account_promo.dict()
    return db.execute(sql, val)

# this has a flaw in loop.index > 2
def update_cc_account_promo( cc_account_promo:CcAccountPromoModel):
    sql = """
    UPDATE admin.cc_account_promo
    SET cc_account_id = %s
        , offer = %s
        , loan_amt = %s
        , bal_transfer_date = %s
        , bal_transfer_amt = %s
        , promo_info = %s
        , recorded_on = CURRENT_TIMESTAMP
    WHERE promo_id = %s
"""
    val = cc_account_promo.dict()
    return db.execute(sql, val)

#######################
# cc_account
#######################
from models.CcAccountModel import CcAccountModel

def get_cc_account_basesql():
    sql = """
    SELECT cca.id
        , cca.client_id
        , TRIM(CONCAT(cp.last_name, ',', cp.first_name, ' ', cp.middle_name)) as client_name
        , cca.xero_id
        , cca.client_code
        , cca.first_name
        , cca.last_name
        , cca.card_name
        , cca.card_status
        , admin.f_adm_setting_get('CARDSTATUS', cca.card_status) AS cc_status_desc
        , cca.device
        , admin.f_adm_setting_get('DEVICE', cca.device) AS device_desc
        , to_char(cca.open_date::date, 'YYYY-MM-DD') as open_date
        , cca.cc_login
        , admin.f_adm_decrypt( cca.cc_pwd) as cc_pwd
        , admin.f_adm_decrypt( cca.cc_card_info) as cc_card_info
        , to_char(cca.reconciled_on, 'YYYY-MM-DD') as reconciled_on
        , to_char(cca.charged_on, 'YYYY-MM-DD') as charged_on
        , cca.credit_line
        , to_char(cca.due_on, 'YYYY-MM-DD') as due_on
        , cca.bonus_to_spend
        , to_char(cca.bonus_spend_by, 'YYYY-MM-DD') as bonus_spend_by
        , cca.bonus_spent
        , cca.ccaccount_info
        , cca.task
        , cca.in_charge
        , cca.notes
        , cca.recorded_on
    FROM client.cc_account  cca
        LEFT JOIN client.client_person cp ON cp.id = cca.client_id
"""
    return sql

def get_cc_account():
    sql = get_cc_account_basesql()
    return db.fetchall(sql)

def get_cc_account_by_id(id):
    sql = get_cc_account_basesql()
    sql += """
    WHERE cca.id = :id;
"""
    return db.fetchone(sql, { 'id' : id} )

def get_cc_account_by_client_id(client_id):
    sql = get_cc_account_basesql()
    sql += """
    WHERE cca.client_id = :client_id;
"""
    return db.fetchall(sql, {'client_id' : client_id})

def upsert_cc_account( cc_account:CcAccountModel):
    sql = """
SELECT client.f_cc_account_insert(
	:xero_id
	, :client_id
	, :client_code
	, :first_name
	, :last_name
    , :card_name
    , :card_status
	, :device
    , CAST( :open_date AS VARCHAR)
    , :cc_login
	, :cc_pwd
	, :card_num
	, :card_exp
	, :card_cvv
	, :card_pin
	, CAST( :reconciled_on AS VARCHAR)
	, CAST( :charged_on AS VARCHAR)
	, CAST( :credit_line AS VARCHAR)
	, CAST( :due_on AS VARCHAR)
	, CAST( :bonus_to_spend AS VARCHAR)
	, CAST( :bonus_spend_by AS VARCHAR)
	, CAST( :bonus_spent AS VARCHAR)
    , :ccaccount_info
    , :task
	, :in_charge
    , :notes
	, :id
    );
    """
    val = cc_account.dict()
    return db.fetchone(sql, val)

def insert_cc_account( cc_account:CcAccountModel):
    return upsert_cc_account( cc_account)

def delete_client_cc_account_by_id( id: int):
    sql = "DELETE FROM client.cc_account WHERE id = :id RETURNING id;"
    return db.fetchone( sql, { 'id': id} )