import common.db_layer as db
#######################
# client_person
#######################
from models.ClientPersonModel import ClientPersonModel

def get_client_person_base_sql():
    sql = """
	SELECT client_person.id
		, client_code
        , TRIM(CONCAT( last_name, ', ', first_name, ' ', middle_name)) as client_name
        , last_name
		, first_name
		, middle_name
		, CASE WHEN dob = '0001-01-01 BC' THEN '1900-01-01' ELSE to_char(dob, 'YYYY-MM-DD') END AS dob
		, ssn
		, mmn
		, email
		, admin.f_adm_decrypt(pwd) as pwd
		, occupation
		, employer
		, income
		, phone
		, phone_2
		, contact_email
		, tax_status
		, wise
		, client_status
		, notes
		, client_info
	FROM client.client_person
"""
    return sql

def get_client_persons():
    sql = get_client_person_base_sql()
    sql += "ORDER BY last_name, first_name, dob;"
    return db.fetchall(sql)

def get_client_person_by_id(id):
    sql = get_client_person_base_sql()
    sql += """
    WHERE id = :id;
"""
    return db.fetchall(sql, {'id': id})

def upsert_client_person( client_person:ClientPersonModel):
    sql = """
SELECT client.f_client_person_insert(
    :client_code
    , :first_name
    , :last_name
    , :middle_name
    , :dob
    , :ssn
    , :mmn
    , :email
    , :pwd
    , :occupation
    , :employer
    , :income
    , :phone
    , :phone_2
    , :contact_email
    , :tax_status
    , :wise
    , :client_status
    , :notes
    , :client_info
    , :id
    );
"""
    val = client_person.dict()
    return db.fetchone(sql, val)
# SELECT client.f_client_person_insert(
#     :client_code::varchar
#     , :first_name::varchar
#     , :last_name::varchar
#     , :middle_name::varchar
#     , :dob::varchar
#     , :ssn::varchar
#     , :mmn::varchar
#     , :email::varchar
#     , :pwd::varchar
#     , :occupation::varchar
#     , :employer::varchar
#     , :income::varchar
#     , :phone::varchar
#     , :phone_2::varchar
#     , :contact_email::varchar
#     , :tax_status::varchar
#     , :wise
#     , :client_status::varchar
#     , :notes::varchar
#     , :client_info::varchar
#     , :id
#     );
# """
def insert_client_person( client_person:ClientPersonModel):
    return upsert_client_person( client_person)

def delete_client_person_by_id( id):
    sql = """
    DELETE FROM client.client_person
    WHERE id = :id
    RETURNING id
"""
    return db.fetchone( sql, { 'id': id} )