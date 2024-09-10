# mssql_db_layer
#
# DB Layer for SQLAlchemy
#------------------------
import os
from flask import current_app
from pandas import DataFrame
import pandas.io.sql as pdsql
import sqlalchemy as sa
from sqlalchemy.sql import text
# from sqlalchemy import create_engine, event

conn = None

#---------------------------
# Called once in the script
#---------------------------
def get_connection( connString = None):
    global conn
    if conn is None or not conn:
        if connString is None:
            connString = os.getenv('CONNECTION_STRING')
        if connString is None or connString == "":
            raise NameError("Connection string does not exist.")
        try:
            engine = sa.create_engine( connString).execution_options(autocommit=True)
            conn = engine.connect()
        except Exception as e:
            raise e
      
    return conn

# utility
def get_args( args):
    return args if isinstance(args, list) or isinstance( args, dict) else [args]
#---------------------
# Base functionality
#---------------------
def conn_execute(conn, sql, args=None):
    try:
        if args is None:
            result = conn.execute( text(sql)).fetchone()
        else:
            result = conn.execute( text(sql), args).fetchone()
        # conn.commit()
    except Exception as ex:
        current_app.logger.error( repr(ex))
        raise ex
    finally:
        return(result)

def conn_read_sql_query(conn, sql, args=None):
    if args is None:
        df = pdsql.read_sql_query( text(sql), conn)
    else:
        sql_params = get_args( args)
        df = pdsql.read_sql_query( text(sql), conn, params=sql_params)
    return df

def log_compiled_sql(conn, cursor, statement, parameters, context, executemany):
    compiled_sql = cursor.mogrify(statement, parameters)
    print("Compiled SQL: ", compiled_sql.decode('utf-8'))

def log_sql_statement( conn, stmt, *args):
    compiled = stmt.compile(compile_kwargs={"literal_binds": True})
    print("Compiled SQL: ", compiled.string)
    print("Parameters: ", compiled.params)
    current_app.logger.info( stmt)

def conn_fetchall(conn, sql, args=None):
    try:
        # event.listen( conn.engine, "before_cursor_execute", log_compiled_sql)
        if args is None:
            retval = pdsql.read_sql( text(sql), conn)
        else:
            sql_params = get_args( args)
            retval = pdsql.read_sql( text(sql), conn, params=sql_params)
        conn.commit()
        return retval
    except Exception as ex:
        current_app.logger.error( repr(ex))
        conn.rollback()
        raise ex

def conn_fetchone(conn, sql, args=None):
    df = conn_fetchall( conn, sql, args)
    return df.head()

def conn_df_to_sql(conn, obj_data, table_name, schema, if_exists='append', args=None):
    df = DataFrame( obj_data)
    df.index = df.index + 1
    df.to_sql( name=table_name, con=conn,schema=schema,if_exists=if_exists, index=True, index_label='id', method=None)

def conn_does_exist(sql, args=None):
    try:
        res = conn.execute( text(sql)).one() if args is None else conn.execute(text(sql), args).one()
        return res[0] == 1 if len(res) > 0 else False
    except Exception as ex:
        current_app.logger.error( repr(ex))
        raise ex

def conn_read_and_run( conn, filename):
    with open( filename, mode="r", encoding="utf-8") as fp:
        sql = text(fp.read())
        retval = conn.execute( text(sql))
        return retval

#-------------------------------


def db_globalconnector( func):
    def with_connection_(*args, **kwargs):
        global conn
        return func( conn, *args, **kwargs)
    return with_connection_


@db_globalconnector
def execute(conn, sql, args=None):
    result = None
    try:
        if args is None:
            result = conn.execute( text(sql)).fetchone()
        else:
            result = conn.execute( text(sql), args).fetchone()
        # conn.commit()
    except Exception as ex:
        current_app.logger.error( repr(ex))
        raise ex
    finally:
        return(result)

@db_globalconnector
def read_sql_query(conn, sql, args=None):
    if args is None:
        df = pdsql.read_sql_query( text(sql), conn)
    else:
        sql_params = get_args( args)
        df = pdsql.read_sql_query( text(sql), conn, params=sql_params)
    return df

@db_globalconnector
def fetchall(conn, sql, args=None):
    return conn_fetchall( conn, sql, args)

@db_globalconnector
def fetchone(conn, sql, args=None):
    return conn_fetchone( conn, sql, args)

@db_globalconnector
def df_to_sql(conn, obj_data, table_name, schema, if_exists='append', args=None):
    return conn_df_to_sql(conn, obj_data, table_name, schema, if_exists, args)

@db_globalconnector
def read_and_run( conn, filename):
    return conn_read_and_run( conn, filename)

def does_exist(conn, sql, args=None):
    return conn_does_exist(conn, sql, args)

    

##########################
# db connection wrappers 
##########################
def db_connector( func):
    def with_connection_(*args, **kwargs):
        conn = None
        connString = os.getenv('CONNECTION_STRING')
        if connString is None or connString == "":
            raise NameError("Connection string does not exist.")
        try:
            engine = sa.create_engine( connString)
            with engine.connect() as conn:
                return func( conn, *args, **kwargs)
        except Exception as ex:
            raise ex
        finally:
            if conn:
                conn.close()
    return with_connection_
    

@db_connector
def db_df_to_sql(conn, obj_data, table_name, schema, if_exists='append', args=None):
    conn_df_to_sql(conn, obj_data, table_name, schema, if_exists, args)

# @db_connector
# def get_sql_data_source_name( conn, arg=None, arg2=None):
#     return conn.getinfo(pyodbc.SQL_DATA_SOURCE_NAME)

def does_table_exist(conn, table_name) -> bool:
    sql = "SELECT COUNT(name) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = ?"
    res = conn.execute( text(sql), [(table_name)]).one()
    return res[0] == 1 if len(res) > 0 else False

@db_connector
def db_read_sql_query(conn, sql, args=None):
    return conn_read_sql_query(conn, sql, args)

@db_connector
def db_fetchall(conn, sql, args=None):
    return conn_fetchall(conn, sql, args)

@db_connector
def db_fetchone(conn, sql, args=None):
    return conn_fetchone(conn, sql, args)

@db_connector
def db_execute(conn, sql, args=None):
    return conn_execute( conn, sql, args)

@db_connector
def db_does_exist(conn, sql, args=None):
    return conn_does_exist( conn, sql, args)

@db_connector
def db_read_and_run( conn, filename):
    read_and_run( conn, filename)
