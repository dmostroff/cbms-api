import common.db_layer as db


#######################
# client dashboard
#######################
def get_client_credit_summary_sql():
    sql = """
WITH tCcAccount AS (
	SELECT cca.client_id
		, COUNT(cca.client_id) AS cc_account_count
		, CAST(SUM( cca.credit_line ) AS DECIMAL(12,2)) AS total_credit_limit
		, MIN(COALESCE(cca.open_date, '2900-01-01')) as min_open_date
	FROM client.cc_account cca
    WHERE cca.client_id = COALESCE( :client_id, cca.client_id)
	GROUP BY cca.client_id
), tCreditLineHistoryByCard AS (
    SELECT clh.client_id
        , clh.card_id
        , SUM( clh.amount) AS amount
    FROM client.credit_line_history clh
    WHERE clh.client_id = COALESCE( :client_id, clh.client_id)
    GROUP BY clh.client_id, card_id
), tCreditLineHistory AS (
    SELECT tclh.client_id
        , SUM( tclh.amount) as amount
    FROM tCreditLineHistoryByCard tclh
    GROUP BY tclh.client_id
), tAddress AS (
	SELECT ca.client_id
	   , MIN(TRIM(CONCAT(ca.street_address, ' ', ca.city, ' ', ca.state, ' ', ca.zip))) as address
	FROM client.client_address ca
	WHERE ca.is_current = true
        AND ca.client_id = COALESCE( :client_id, ca.client_id)
	GROUP BY ca.client_id
)
SELECT cp.id as id
        , cp.client_code
        , TRIM( CONCAT(cp.last_name, ', ', cp.first_name, ' ', cp.middle_name)) as client_name
        , COALESCE(tca.cc_account_count, 0) AS cc_account_count
        , (SELECT COUNT(*) FROM client.loan cl WHERE cl.client_id = cp.id) AS loan_count
        , (SELECT COUNT(*) FROM client.checking ch WHERE ch.client_id = cp.id) AS checking_count
        , cp.email AS email
        , cp.phone as phone
        , CASE WHEN tca.min_open_date = '2900-01-01' THEN NULL ELSE tca.min_open_date END AS min_open_date
        , COALESCE(tca.total_credit_limit, 0) AS total_credit_limit
        , COALESCE(tclh.amount, 0) AS credit_limit
    FROM client.client_person cp
    	LEFT JOIN tAddress ta ON ta.client_id = cp.id
    	LEFT JOIN tCcAccount  tca ON tca.client_id = cp.id
        LEFT JOIN tCreditLineHistory tclh ON tclh.client_id = cp.id
    WHERE cp.id = COALESCE( :client_id, cp.id)
    ORDER BY client_name, min_open_date;
"""
    return sql

def get_client_credit_summary():
    sql = get_client_credit_summary_sql()
    return db.fetchall(sql, { 'client_id': None })

def get_client_credit_summary_by_client_id( id):
    sql = get_client_credit_summary_sql()
    return db.fetchall(sql, { 'client_id': id })
    




# print( 'client_repository')