from flask import current_app
from flask import jsonify, url_for
from typing import Union
import os
import json
import re
from datetime import datetime, date
from cryptography.fernet import Fernet


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


def get_links(app):
    links = []
    for rule in app.url_map.iter_rules():
    # Filter out rules we can't navigate to in a browser
    # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return links


def init_environ(app, config):
    os.environ['CONNECTION_STRING'] = config['MSSQL']['CONNECTION_STRING']
    # os.environ['UPLOAD_DIR'] = config['System']['UPLOAD_DIR']
    # os.environ['ADD_TO_REF_TABLES'] = config['System']['ADD_TO_REF_TABLES']

    for k in config['System']: os.environ[k] = config['System'][k]
    # fix up the ADD_TO_REF_TABLES to be 1 or 0
    os.environ['ADD_TO_REF_TABLES'] = '1' if os.getenv(
        'ADD_TO_REF_TABLES') == 'True' else '0'
    app.config['ALLOWED_EXTENSIONS'] = {'xlsx', 'csv'}
    # app.config['SECRET_KEY'] = config['System']['SECRET_KEY']


def json_rc_msg(rc: int = 0, msg: str = '', data: Union[dict, list] = None, retstatus: int = 200):
    retval = {'rc': rc}
    if msg is not None and len(msg) > 0:
        retval['msg'] = msg
    # print( data, type(data))
    if isinstance(data, str) or isinstance(data, dict) or isinstance( data, list):
        newdata = {'data': data}
    elif isinstance(data, set):
        newdata = {'data': dict.fromkeys(data)}
    else:
        newdata = data
    if newdata is not None:
        retval = {**retval, **newdata}
    return retval


def df_to_dict(df):
    dfjson = df_to_json(df)
    return json.loads(dfjson)


def df_to_json(df):
    return df.to_json(orient="records", date_format="iso")


def df_to_json_pretty(df):
    dfjson = df_to_json(df)
    parsed = json.loads(dfjson)
    return json.dumps(parsed, indent=4)


def json_view(df):
    return jsonify(json.loads(df_to_json(df)) if df is not None else {})


def decrypt(encoded_string):
    key = os.getenv('KEY')
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(bytes(encoded_string, 'utf-8'))


def encrypt(decoded_string):
    key = os.getenv('KEY')
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(bytes(decoded_string, 'utf-8'))


def empty_to_none(obj, keys):
    for k in keys:
        obj[k] = empty_to_none_or_trim(obj.get(k))


def empty_to_none_or_trim(instr: str) -> str:
    if instr is None:
        return instr
    return None if instr.strip() == '' else instr.strip()


def string_to_date(obj, keys):
    for k in keys:
        obj[k] = sanitize_date( obj.get(k))

def string_to_float(obj, keys):
    for k in keys:
        obj[k] = sanitize_float( obj.get(k))


def obj_to_jsonstring(obj, keys):
    for k in keys:
        if obj.get(k) is not None:
            obj[k] = json.dumps(obj[k])


def convert_int(s: str):
    try:
        ival = int(s)
    except ValueError:
        ival = None
    return ival


def convert_date(obj: dict, keys: list) -> dict:
    for k in keys:
        obj[k] = sanitize_date(obj.get(k))
    return obj


def sanitize_phone(in_phone: str) -> str:
    return re.sub(r'[^\d]', '', in_phone)[0:10] if in_phone is not None else in_phone


def sanitize_datetime(in_date) -> datetime:
    if in_date is None or isinstance(in_date, datetime):
        return in_date
    if isinstance(in_date, date):
        return datetime.combine(in_date, datetime.min.time())
    patterns = (
        (r'^\d\d?/\d\d?/\d{4} \d\d?:\d\d?:\d\d?$', '%m/%d/%Y %H:%M:%S')
        , (r'^\d\d\.\d\d?\.\d{4} \d\d?:\d\d?:\d\d?$', '%d.%m.%Y %H:%M:%S')
        , (r'^\d{4}-\d\d?-\d\d? \d\d?:\d\d?:\d\d?$', '%Y-%m-%d %H:%M:%S')
        , (r'^\d{4}\-\d{2}\-\d{2}T\d{2}:\d{2}}\.\d{3}Z$', '%Y-%m-%dT%H:%M:%S.%fZ')
    )
    retval = [datetime.strptime(in_date, x[1])
                                for x in patterns if re.match(x[0], in_date)]
    return retval[0] if len(retval) > 0 else None


def sanitize_date(in_date) -> date:
    if in_date is None or isinstance(in_date, date):
        return in_date
    if isinstance(in_date, datetime):
        return in_date.date()
    patterns = (
        (r'^\d\d?/\d\d?/\d{4}$', '%m/%d/%Y')
        , (r'^\d\d\.\d\d?\.\d{4}$', '%d.%m.%Y')
        , (r'^\d{4}\-\d\d?\-\d\d?$', '%Y-%m-%d')
        , (r'^\d{4}\-\d{2}\-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$', '%Y-%m-%dT%H:%M:%S.%fZ')
    )
    retval = [datetime.strptime(in_date, x[1]).date()
                                for x in patterns if re.match(x[0], in_date)]
    return retval[0] if len(retval) > 0 else None

def sanitize_int(in_int):
    retval = None
    try:
        if isinstance(in_int, str):
            ival = re.sub(r'[^\d\.', '', in_int)
            retval=None if ival == '' else int(ival)
    except Exception as ex:
        current_app.logger.error( repr(ex))
        raise ex
    finally:
        return retval


def sanitize_float(in_float):
    retval = None
    try:
        if isinstance(in_float, float):
            retval = in_float
        elif isinstance(in_float, str):
            fval = re.sub(r'[^\d\.]', '', in_float)
            retval=None if fval == '' else float(fval)
        else:
            retval = float(in_float)
    except Exception as ex:
        current_app.logger.error( repr(ex))
        raise ex
    finally:
        return retval

def sanitize_bool( in_bool):
    if isinstance( in_bool, bool):
        return in_bool
    if isinstance( in_bool, str):
        return True if in_bool.strip().lower() == 'y' else False
    if isinstance( in_bool, int):
        return True if in_bool != 0 else False

def get_card_part(card_info, part_no):
    if card_info is None:
        return None
    else:
        parts = card_info.split( '~')
        return parts[part_no] if len(parts) > part_no else None

def extract_card_info(df, card_info_name: str, card_part_names: list):
    if not df.empty:
        for idx, name in enumerate(card_part_names):
            df[name] = df.apply( lambda row: get_card_part(row[card_info_name], idx), axis = 1)
