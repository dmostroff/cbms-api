# mssql_db_layer
#
# DB Layer for MSSQL
#------------------------
import os
import sys
from pandas import DataFrame
import pandas.io.sql as pdsql
import sqlalchemy as sa

def sqldb_connector( func):
    def with_connection_(*args, **kwargs):
        conn = None
        connString = os.getenv('CONNECTION_STRING')
        if connString is None or connString == "":
            raise NameError("Connection string does not exist.")
        try:
            engine = sa.create_engine( connString)
            with engine.connect() as conn:
                return func( conn, *args, **kwargs)
        except Exception as e:
            print( sys.exc_info()[1])
            raise e
        finally:
            if conn:
                conn.close()
    return with_connection_
    

# @db_connector
# def get_sql_data_source_name( conn, arg=None, arg2=None):
#     return conn.getinfo(pyodbc.SQL_DATA_SOURCE_NAME)

def does_table_exist(conn, table_name) -> bool:
    sql = "SELECT COUNT(name) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = ?"
    res = conn.execute( sql, [(table_name)]).one()
    return res[0] == 1 if len(res) > 0 else False

@sqldb_connector
def read_sql_query(conn, sql, args=None):
    if args is None:
        df = pdsql.read_sql_query( sql, conn)
    else:
        sql_params = args if isinstance(args, list) else [args]
        df = pdsql.read_sql_query( sql, conn, params=sql_params)
    return df

@sqldb_connector
def fetchall(conn, sql, args=None):
    try:
        if args is None:
            retval = pdsql.read_sql( sql, conn)
        else:
            sql_params = args if isinstance(args, list) else [args]
            retval = pdsql.read_sql( sql, conn, params=sql_params)
        return retval
    except Exception as ex:
        print( sys.exc_info()[1])
        raise ex

@sqldb_connector
def fetchone(conn, sql, args=None):
    try:
        if args is None:
            retval = pdsql.read_sql( sql, conn)
        else:
            sql_params = args if isinstance(args, list) else [args]
            retval = pdsql.read_sql( sql, conn, params=sql_params)
        return retval.head()
    except Exception as ex:
        print( sys.exc_info()[1])
        raise ex

@sqldb_connector
def execute(conn, sql, args=None):
    try:
        curs = conn.cursor()
        if args is None:
            curs.execute( sql)
        else:
            curs.execute( sql, args)
        # conn.commit()
    except Exception as ex:
        print( sys.exc_info()[1])
        raise ex

@sqldb_connector
def does_exist(conn, sql, args=None):
    try:
        res = conn.execute( sql).one() if args is None else conn.execute(sql, args).one()
        return res[0] == 1 if len(res) > 0 else False
    except Exception as ex:
        print( sys.exc_info()[1])
        raise ex
