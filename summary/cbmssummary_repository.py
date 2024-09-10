import common.db_layer as db


#######################
# cbms_summary
#######################
def get_cbms_summary():
    sql = """
    SELECT 'Clients' AS category, 'Clients' as title, count(*) as row_count
    FROM client.client_person
    UNION ALL
    SELECT 'Credit Card Accounts', 'Total Accounts', COUNT(*)
    FROM client.cc_account
    UNION ALL
    SELECT 'Credit Card Status', cc_status, COUNT(*)
    FROM client.cc_account
    GROUP BY cc_status
    UNION ALL
    SELECT 'Card Name', card_name, COUNT(*)
    FROM client.cc_account
    GROUP BY card_name
    UNION ALL
    SELECT 'Card Name', CAST(CAST(credit_limit / 1000 AS INT) * 1000 AS text), COUNT(*)
    FROM client.cc_account
    GROUP BY CAST(credit_limit / 1000 AS INT) * 1000
"""
    return db.fetchall(sql)

