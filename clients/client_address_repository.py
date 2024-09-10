import common.db_layer as db

#######################
# client_address
#######################
from models.ClientAddressModel import ClientAddressModel

def client_address_dict_get(client_address:ClientAddressModel) -> dict:
    val = client_address.dict()
    return val

def get_client_address_basesql():
    sql = """
    SELECT id
        , client_id
        , client_code
        , street_address
        , city
        , state
        , zip
        , is_current
        , recorded_on
    FROM client.client_address
"""
    return sql

def get_client_addresss():
    sql = get_client_address_basesql()
    return db.fetchall(sql)

def get_client_address_by_id(id):
    sql = get_client_address_basesql()
    sql += """
    WHERE id = :id;
"""
    return db.fetchone( sql, { 'id': id} )
    
def get_client_address_by_client_id(id):
    sql = get_client_address_basesql()
    sql += """
    WHERE client_id = :client_id
    ORDER BY is_current DESC, state, street_address;
"""
    return db.fetchall(sql, { 'client_id': id})

# def get_client_address_by_client_address_id(client_address_id):
#     sql = get_client_address_basesql()
#     sql += """
#     WHERE client_address_id = %s
# """
#     return db.fetchall(sql, [client_address_id])

def upsert_client_address( client_address:ClientAddressModel):
    sql = """
SELECT client.f_client_address_insert(
    :client_id
    , :client_code
	, :street_address
	, :city
    , :state
    , :zip
	, :is_current
    , :id
);
"""
    val = client_address_dict_get(client_address)
    return db.fetchone(sql, val)

def set_current_address(in_data:dict):
    sql = """
    WITH tAddress AS (
        SELECT id, client_id
        FROM client.client_address
        WHERE id = :id
    )
    UPDATE client.client_address t1
    SET is_current = CASE WHEN t1.id = t2.id THEN :is_current ELSE false END
    FROM tAddress t2
	 WHERE t2.client_id = t1.client_id
	RETURNING t1.id, t1.is_current
    ;    """
    return db.fetchall(sql, in_data)

def delete_client_address_by_id(id: int):
    sql = "DELETE FROM client.client_address WHERE id = :id RETURNING id"
    return db.fetchone(sql, {'id': id})
