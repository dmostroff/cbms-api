import common.db_layer as db


#######################
# cc_card
#######################
from models.CcCardModel import CcCardModel

def get_cc_card_basesql():
    sql = """
    SELECT c1.id
        , c1.card_name
        , c1.cc_company_id
        , c2.company_name
        , c1.version
        , c1.annual_fee
        , c1.first_year_free
        , c1.recorded_on
    FROM client.cc_card c1
        JOIN client.cc_company c2 ON c2.id = c1.cc_company_id
"""
    return sql
def get_cc_card_basesql():
    sql = """
WITH tCards AS (
    SELECT
        CASE
            WHEN POSITION('-' in xero_id) > 0 THEN SUBSTRING(xero_id FROM 1 FOR POSITION('-' IN xero_id) - 1)
            ELSE NULL
            END AS card_code
        , TRIM(card_name) AS card_name
FROM cc_account
)
SELECT card_code, card_name
FROM tCards
WHERE card_code IS NOT NULL
    """
    return sql

def get_cc_cards():
    sql = get_cc_card_basesql()
    sql += """
GROUP BY card_code, card_name
ORDER BY card_code, card_name
    """
    # sql += " ORDER BY cc_company_id, card_name"
    return db.fetchall(sql)

def get_cc_card_by_name(card_name):
    sql = get_cc_card_basesql()
    sql += """
    AMD card_name = %s
"""
    return db.fetchall(sql, [card_name])

# def get_cc_card_by_cc_card_id(cc_card_id):
#     sql = get_cc_card_basesql()
#     sql += """
#     WHERE cc_card_id = %s
# """
#     return db.fetchall(sql, [cc_card_id])

# def upsert_cc_card( cc_card:CcCardModel):
#     sql = """
#     WITH t AS (
#         SELECT 
#             %s::integer as id
#             , %s::integer as cc_company_id
#             , %s::text as card_name
#             , %s::text as version
#             , %s::numeric as annual_fee
#             , %s::boolean as first_year_free
#             , CURRENT_TIMESTAMP as recorded_on
#     ),
#     u AS (
#         UPDATE client.cc_card
#         SET 
#             cc_company_id=t.cc_company_id
#             , card_name=t.card_name
#             , version=t.version
#             , annual_fee=t.annual_fee
#             , first_year_free=t.first_year_free
#             , recorded_on=t.recorded_on
#         FROM t
#         WHERE cc_card.id = t.id
#         RETURNING cc_card.*
#     ),
#     i AS (
#         INSERT INTO client.cc_card( cc_company_id,card_name,version,annual_fee,first_year_free,recorded_on)
#         SELECT 
#             t.cc_company_id
#             , t.card_name
#             , t.version
#             , t.annual_fee
#             , t.first_year_free
#             , t.recorded_on
#         FROM t
#         WHERE NOT EXISTS ( SELECT 1 FROM u)
#         RETURNING client.cc_card.*
#     )
#     SELECT 'INSERT' as ACTION, i.*
#     FROM i
#     UNION ALL
#     SELECT 'UPDATE' as ACTION, u.*
#     FROM u
# """
#     val = [
#             cc_card.id
#             , cc_card.cc_company_id
#             , cc_card.card_name
#             , cc_card.version
#             , cc_card.annual_fee
#             , cc_card.first_year_free
#         ]
#     return db.fetchall(sql, val)

# def insert_cc_card( cc_card:CcCardModel):
#     sql = """
#     INSERT INTO client.cc_card( cc_company_id,card_name,version,annual_fee,first_year_free)
#     VALUES (%s, %s, %s, %s, %s)
#     RETURNING *
#     ;
# """
#     val = [
#             cc_card.cc_company_id
#             , cc_card.card_name
#             , cc_card.version
#             , cc_card.annual_fee
#             , cc_card.first_year_free
#         ]
#     return db.fetchone(sql, val)

# # this has a flaw in loop.index > 2
# def update_cc_card( cc_card:CcCardModel):
#     sql = """
#     UPDATE client.cc_card
#     SET cc_company_id = %s
#         , card_name = %s
#         , version = %s
#         , annual_fee = %s
#         , first_year_free = %s
#         , recorded_on = CURRENT_TIMESTAMP
#     WHERE id = %s
#     RETURNING *
# """
#     val = [
#             cc_card.cc_company_id
#             , cc_card.card_name
#             , cc_card.version
#             , cc_card.annual_fee
#             , cc_card.first_year_free
#             , cc_card.id            
#         ]
#     return db.fetchone(sql, val)
