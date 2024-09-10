import common.db_layer as db

def get_db_info( funcname):
    return db.fetchall(f"SELECT {funcname}()")
    # return retval[funcname][0] if funcname in retval and len(retval[funcname]) > 0 else 'unknown'
    # return retval if funcname in retval and len(retval[funcname]) > 0 else 'unknown'

def get_database_name():
    return get_db_info("current_database")

def get_version():
    return get_db_info("version")

def get_server_name():
    return get_db_info("inet_server_addr")

def get_connection_info():
    sql = """SELECT datid
    pid,
    datname,
    usename,
    application_name,
    backend_start,
    client_addr,
    client_hostname,
    client_port,
    query_start
FROM pg_stat_activity
WHERE pid = pg_backend_pid()
"""
    return db.fetchall(sql)