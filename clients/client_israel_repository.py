import common.db_layer as db
from models.ClientIsraelModel import ClientIsraelModel

#######################
# client_israel
#######################

def get_client_israel_basesql():
    sql = """
    SELECT client_israel.id
        , client_id
        , client_code
        , bank
        , branch
        , account
        , iban
        , iban_name
        , address
        , city
        , zip
        , phone
        , notes
        , recorded_on
    FROM client.client_israel
"""
    return sql

def get_client_israels():
    sql = get_client_israel_basesql()
    return db.fetchall(sql)

def get_client_israel_by_id(id):
    sql = get_client_israel_basesql()
    sql += """
    WHERE client_israel.id = :id
"""
    return db.fetchone( sql, { 'id': id} )

def get_client_israel_by_client_id( client_id):
    sql = get_client_israel_basesql()
    sql += """
    WHERE client_id = :client_id
"""
    return db.fetchall(sql, { 'client_id': client_id})

def upsert_client_israel( client_israel:ClientIsraelModel):
    sql = """
SELECT client.f_client_israel_insert(
    :client_id
    , :client_code
	, :bank
	, :branch
	, :account
	, :iban
	, :iban_name
	, :address
	, :city
	, :zip
	, :phone
	, :notes
	, :id
);
"""
    val = client_israel.dict()
    return db.fetchone(sql, val)

def insert_client_israel( client_israel:ClientIsraelModel):
    return upsert_client_israel( client_israel)


def get_bank_names():
    sql = """
    SELECT bank
    FROM client.client_israel
    GROUP BY bank
    ORDER BY bank
"""
    return db.fetchall(sql)

def delete_client_israel_by_id(id: int):
    sql = "DELETE FROM client.client_israel WHERE id = :id RETURNING id"
    return db.fetchone( sql, { 'id': id} )

