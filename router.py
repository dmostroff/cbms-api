import os
import datetime
import socket
from flask import current_app
from flask import Flask
from flask import request
from flask_restful import Api
import json
import jwt
import re

import common.common_service as cs

import admin.user_login_service as uls
from admin.user_login_resource import UserLogin
from admin.auth_user_resource import AuthUsers, AuthUser
from admin.auth_user_setting_resource import (
    AuthUserSetting,
    AuthUserSettingByPrefix,
    AuthUserSettingPost,
)
from admin.auth_role_resource import AuthRoles, AuthRole, AuthRolePost
from admin.adm_setting_resource import (
    AdmSettings,
    AdmSettingByPrefix,
    AdmSetting,
    AdmSettingPost,
)

# from cbmssummary_resource import CBMSSummary
from resources.credit_summary_resource import ClientCreditSummary, CreditSummary
from resources.banks_resource import Banks
from resources.client_resource import Client
from resources.clientperson_resource import ClientPersons, ClientPerson
from resources.client_address_resource import (
    ClientAddress,
    ClientAddressCurrent,
    ClientAddressByClient,
)
from resources.ccaccount_resource import CcAccounts, CcAccountsByClient, CcAccount

# from resources.ccaccounttodo_resource import CcAccountTodos, CcAccountTodoByClient, CcAccountTodoByCcAccount, CcAccountTodo, CcAccountTodoPost
from resources.clientisrael_resource import (
    ClientIsraels,
    ClientIsraelsByClient,
    ClientIsrael,
)
from resources.clientloan_resource import ClientLoans, ClientLoan, ClientLoanByClient
from resources.credit_report_resource import (
    CreditReports,
    CreditReport,
    CreditReportByClient,
)
from resources.credit_line_history_resource import (
    CreditLineHistories,
    CreditLineHistory,
    CreditLineHistoryByClient,
)
from resources.checking_resource import Checkings, Checking, CheckingByClient

from resources.cccard_resource import CcCards, CcCard
from resources.cccompany_resource import (
    CcCompanies,
    CcCompanies,
    CcCompany,
    CcCompanyPost,
)
from database.db_resource import DatabaseInfo


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        app = Flask(__name__)
        payload = jwt.decode(auth_token, app.config.get("SECRET_KEY"))
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return "Signature expired. Please log in again."
    except jwt.InvalidTokenError:
        return "Invalid token. Please log in again."


def is_route_guarded(request):
    guarded_route_prefix = [
        "adm",
        "auth",
        "bankaccount",
        "bankaccounts",
        'client',
        'clients',
        "cc",
        "creditcard",
        "creditcards",
        "creditsummary",
        "user",
    ]
    paths = request.path.split("/")
    prefixpath = paths[1] if len(paths) > 0 else ""
    return prefixpath in guarded_route_prefix


def before_and_after_requests(app):
    @app.before_request
    def check_jwt_token():
        if request.method == "OPTIONS":
            return
        # app.logger.info( f"Before Request: {request.method} {request.path}")
        if is_route_guarded(request):
            token_result = uls.token_result_from_request(request)
            if not uls.is_valid_token(token_result):
                current_app.logger.info(f"Token invalid: {request.path}")
                return token_result
        return

    @app.after_request
    def apply_jwt(response):
        if not (request.method == "OPTIONS" or response is None):
            if request.path.__eq__("/onboard/login") and request.method == "POST":
                username = (
                    request.json["username"]
                    if "username" in request.json
                    else "__unknown__"
                )
                response = uls.add_token_to_header(response, username)
                # current_app.logger.info( f"Token added: {request.method} {request.path}")
            elif is_route_guarded(request):
                response = uls.update_token(request, response)
                # current_app.logger.info( f"Token updated: {request.method} {request.path}")
        return response

    return app


# @staticmethod

# Using an `after_request` callback, we refresh any token that is within 30
# minutes of expiring. Change the timedeltas to match the needs of your application.
# @app.after_request
# def refresh_expiring_jwts(response):
#     try:
#         exp_timestamp = get_jwt()["exp"]
#         now = datetime.now(timezone.utc)
#         target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
#         if target_timestamp > exp_timestamp:
#             access_token = create_access_token(identity=get_jwt_identity())
#             set_access_cookies(response, access_token)
#         return response
#     except (RuntimeError, KeyError):
#         # Case where there is not a valid JWT. Just return the original respone
#         return response


def set_routes(app):

    api = Api(app)
    sundry_routes(app)
    login_routes(api)
    setting_routes(api)
    client_routes(api)
    cc_routes(api)
    creditcard_routes(api)
    db_routes(api)
    return app


def sundry_routes(app):
    @app.route("/", methods=["GET"])
    def read_main():
        dt = datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")
        return cs.json_rc_msg(
            1, "Welcome to CBMS", {"version": os.getenv("API_VERSION"), "time": dt}
        )

    @app.route("/ping", methods=["GET"])
    def ping():
        pattern = r"(\w+)://(\w+?):.+@(\w+)"
        preplace = r"\1:\2:*****@\3"
        connect_string = re.sub(pattern, preplace, os.getenv("CONNECTION_STRING"))
        dt = datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")
        return cs.json_rc_msg(
            1,
            "Ping",
            {
                "hostname": socket.gethostname(),
                "time": dt,
                "API_VERSION": os.getenv("API_VERSION"),
                "Connect": connect_string,
            },
        )

    @app.route("/pingos", methods=["GET"])
    def pingos():
        exclude_keys = [
            "JWT_SECRET_KEY",
            "ENCRYPT_KEY",
            "SQLCONNECTION_STRING",
            "CONNECTION_STRING",
        ]
        return cs.json_rc_msg(
            1,
            "PingOS",
            json.dumps(
                [{x: os.getenv(x)} for x in os.environ.keys() if x not in exclude_keys]
            ),
        )

    @app.route("/site-map")
    def site_map():
        # links = []
        # for rule in app.url_map.iter_rules():
        #     # Filter out rules we can't navigate to in a browser
        #     # and rules that require parameters
        #     if "GET" in rule.methods and has_no_empty_params(rule):
        #         url = url_for(rule.endpoint, **(rule.defaults or {}))
        #         links.append((url, rule.endpoint))
        links = cs.get_links(app)
        # links is now a list of url, endpoint tuples
        return cs.json_rc_msg(1, "Site Map", json.dumps(links))

    @app.route("/version", methods=["GET"])
    def version():
        return cs.json_rc_msg(1, "Version", {"version": os.getenv("API_VERSION")})

    @app.route("/<path:path>")
    def catch_all(path):
        return "You requested an invalid path: %s" % path


def login_routes(api):

    # -- Login
    api.add_resource(UserLogin, "/onboard/<string:name>")
    # -- Auth Users
    api.add_resource(AuthUsers, "/auth/users")
    api.add_resource(AuthUser, "/auth/user/<int:id>")
    # -- UserSettings
    api.add_resource(
        AuthUserSettingByPrefix, "/user/setting/<int:user_id>/<string:prefix>"
    )
    api.add_resource(AuthUserSetting, "/user/setting/<int:id>")
    api.add_resource(AuthUserSettingPost, "/user/setting")
    # -- Roles
    api.add_resource(AuthRoles, "/auth/roles")
    api.add_resource(AuthRole, "/auth/role/<int:id>")
    api.add_resource(AuthRolePost, "/auth/role")


def setting_routes(api):
    # -- Settings
    api.add_resource(AdmSettings, "/adm/settings")
    api.add_resource(AdmSettingByPrefix, "/adm/setting/<string:prefix>")
    api.add_resource(AdmSetting, "/adm/setting/<int:id>")
    api.add_resource(AdmSettingPost, "/adm/setting")


# #-- CBMS Summary
# api.add_resource( CBMSSummary, '/cbms/summary')


def client_routes(api):
    # #-- Client
    api.add_resource(Client, "/client/<int:id>")

    # #-- ClientPerson
    api.add_resource(CreditSummary, "/creditsummary")
    api.add_resource(ClientPersons, "/clients")
    api.add_resource(ClientPerson, "/client/person/<int:id>")

    # #-- ClientAddress
    api.add_resource(ClientAddressCurrent, "/client/address/<int:id>/current")
    api.add_resource(ClientAddress, "/client/address/<int:id>")
    api.add_resource(ClientAddressByClient, "/client/<int:client_id>/address")

    # -- ClientIsrael
    api.add_resource(ClientIsraels, "/client/israels")
    api.add_resource(ClientIsraelsByClient, "/client/<int:client_id>/israel")
    api.add_resource(ClientIsrael, "/client/israel/<int:id>")

    # -- ClientLoan
    api.add_resource(ClientLoans, "/client/loans")
    api.add_resource(ClientLoanByClient, "/client/<int:client_id>/loan")
    api.add_resource(ClientLoan, "/client/loan/<int:id>")
    # api.add_resource( ClientLoan, '/client/loan/<int:id>', '/client/loan')

    # -- CreditReport
    api.add_resource(CreditReports, "/client/creditreport")
    api.add_resource(CreditReportByClient, "/client/<int:client_id>/creditreport")
    api.add_resource(CreditReport, "/client/creditreport/<int:id>")

    # -- Credit Line History
    api.add_resource(CreditLineHistories, "/client/creditline")
    api.add_resource(CreditLineHistoryByClient, "/client/<int:client_id>/creditline")
    api.add_resource(CreditLineHistory, "/client/creditline/<int:id>")

    # -- Checking
    api.add_resource(Checkings, "/client/checking")
    api.add_resource(CheckingByClient, "/client/<int:client_id>/checking")
    api.add_resource(Checking, "/client/checking/<int:id>")


def cc_routes(api):
    # -- CCAccount
    api.add_resource(CcAccounts, "/cc/accounts")
    api.add_resource(CcAccountsByClient, "/client/<int:client_id>/cc/account")
    api.add_resource(CcAccount, "/cc/account/<int:id>")

    # -- Client CC Account to do
    # api.add_resource( CcAccountTodos, '/cc/accounttodos')
    # api.add_resource( CcAccountTodoByClient, '/client/<int:client_id>/ccaccounttodo')
    # api.add_resource( CcAccountTodoByCcAccount, '/cc/account/<int:cc_account_id>/todo')
    # api.add_resource( CcAccountTodo, '/cc/accounttodo/<int:id>')
    # api.add_resource( CcAccountTodoPost, '/cc/accounttodo')


def creditcard_routes(api):
    # -- Banks
    api.add_resource(Banks, "/banks")

    # -- Credit Cards
    api.add_resource(CcCards, "/creditcards")
    api.add_resource(CcCard, "/creditcard/<string:card_name>")
    # api.add_resource( CcCompanies, '/cc/companies')
    # api.add_resource( CcCompany, '/cc/company/<int:id>')
    # api.add_resource( CcCompanyPost, '/cc/company')


def import_routes(api):
    pass


def export_routes(api):
    pass


def db_routes(api):
    # -- Database
    api.add_resource(DatabaseInfo, "/db/<string:name>")


# print( 'router DONE')


# -- ClientCcHistory
# from ClientCcHistory import ClientCcHistory
# @app.route('/client/cc_history', methods=['GET'])
# def get_client_cc_history ():
#     return cs.get_client_cc_history()

# @app.route('/client/{client_id}/cc_history', methods=['GET'])
# def get_client_cc_history_by_client_id (client_id):
#     return cs.get_client_cc_history_by_client_id(client_id)

# @app.route('/client/cc_history/<id>', methods=['GET'])
# def get_client_cc_history_by_id (id):
#     return cs.get_client_cc_history_by_id(id)

# @app.route('/client/cc_history', methods=['POST'])
# def post_client_cc_history ( client_cc_history:ClientCcHistory):
#     return cs.upsert_client_cc_history(client_cc_history)


# # @app.route('/client/person', methods=['GET'])
# # def get_client_person ():
# #     return cs.get_client_person()

# # @app.route('/client/<client_id>/person', methods=['GET'])
# # def get_client_person_by_client_id (client_id):
# #     return cs.get_client_person_by_client_id(client_id)

# # @app.route('/client/person/<id>', methods=['GET'])
# # def get_client_person_by_id (id):
# #     return cs.get_client_person_by_id(id)

# # @app.route('/client/person', methods=['POST'])
# # def post_client_person ( client_person:ClientPerson):
# #     return cs.upsert_client_person(client_person)


# #-- ClientCreditlineHistory
# from ClientCreditlineHistory import ClientCreditlineHistory
# @app.route('/client/creditline_history', methods=['GET'])
# def get_client_creditline_history ():
#     return cs.client_creditline_history()

# @app.route('/client/{client_id}/creditline_history', methods=['GET'])
# def get_client_creditline_history_by_client_id (client_id):
#     return cs.client_creditline_history_by_client_id(client_id)

# @app.route('/client/creditline_history/<id>', methods=['GET'])
# def get_client_creditline_history_by_id (id):
#     return cs.client_creditline_history_by_id(id)

# @app.route('/client/creditline_history', methods=['POST'])
# def post_client_creditline_history ( client_creditline_history:ClientCreditlineHistory):
#     return cs.upsert_client_creditline_history(client_creditline_history)


# #-- ClientAddress
# from ClientAddress import ClientAddress
# @app.route('/client/address', methods=['GET'])
# def get_client_address ():
#     return cs.client_address()

# @app.route('/client/{client_id}/address', methods=['GET'])
# def get_client_address_by_client_id (client_id):
#     return cs.client_address_by_client_id(client_id)

# @app.route('/client/address/<id>', methods=['GET'])
# def get_client_address_by_id (id):
#     return cs.client_address_by_id(id)

# @app.route('/client/address', methods=['POST'])
# def post_client_address ( client_address:ClientAddress):
#     return cs.upsert_client_address(client_address)


# #-- ClientCcAccount
# from CcAccount import CcAccount
# @app.route('/client/cc_account', methods=['GET'])
# def get_cc_account ():
#     return cs.cc_account()

# @app.route('/client/{client_id}/cc_account', methods=['GET'])
# def get_cc_account_by_client_id (client_id):
#     return cs.cc_account_by_client_id(client_id)

# @app.route('/client/cc_account/<id>', methods=['GET'])
# def get_cc_account_by_id (id):
#     return cs.cc_account_by_id(id)

# @app.route('/client/cc_account', methods=['POST'])
# def post_cc_account ( cc_account:CcAccount):
#     return cs.upsert_cc_account(cc_account)


# #-- ClientSettingclie
# from ClientSetting import ClientSetting
# @app.route('/client/setting', methods=['GET'])
# def get_client_setting ():
#     return cs.client_setting()

# @app.route('/client/{client_id}/setting', methods=['GET'])
# def get_client_setting_by_client_id (client_id):
#     return cs.client_setting_by_client_id(client_id)

# @app.route('/client/setting/<id>', methods=['GET'])
# def get_client_setting_by_id (id):
#     return cs.client_setting_by_id(id)

# @app.route('/client/setting', methods=['POST'])
# def post_client_setting ( client_setting:ClientSetting):
#     return cs.upsert_client_setting(client_setting)


# #-- ClientIsrael
# from ClientIsrael import ClientIsrael
# @app.route('/client/bank_account', methods=['GET'])
# def get_client_bank_account ():
#     return cs.client_bank_account()

# @app.route('/client/{client_id}/bank_account', methods=['GET'])
# def get_client_bank_account_by_client_id (client_id):
#     return cs.client_bank_account_by_client_id(client_id)

# @app.route('/client/bank_account/<id>', methods=['GET'])
# def get_client_bank_account_by_id (id):
#     return cs.client_bank_account_by_id(id)

# @app.route('/client/bank_account', methods=['POST'])
# def post_client_bank_account ( client_bank_account:ClientIsrael):
#     return cs.upsert_client_bank_account(client_bank_account)


# #-- ClientNote
# from ClientNote import ClientNote
# @app.route('/client/note', methods=['GET'])
# def get_client_note ():
#     return cs.client_note()

# @app.route('/client/{client_id}/note', methods=['GET'])
# def get_client_note_by_client_id (client_id):
#     return cs.client_note_by_client_id(client_id)

# @app.route('/client/note/<id>', methods=['GET'])
# def get_client_note_by_id (id):
#     return cs.client_note_by_id(id)

# @app.route('/client/note', methods=['POST'])
# def post_client_note ( client_note:ClientNote):
#     return cs.upsert_client_note(client_note)


# #-- ClientCcPoints
# from ClientCcPoints import ClientCcPoints
# @app.route('/client/cc_points', methods=['GET'])
# def get_client_cc_points ():
#     return cs.client_cc_points()

# @app.route('/client/{client_id}/cc_points', methods=['GET'])
# def get_client_cc_points_by_client_id (client_id):
#     return cs.client_cc_points_by_client_id(client_id)

# @app.route('/client/cc_points/<id>', methods=['GET'])
# def get_client_cc_points_by_id (id):
#     return cs.client_cc_points_by_id(id)

# @app.route('/client/cc_points', methods=['POST'])
# def post_client_cc_points ( client_cc_points:ClientCcPoints):
#     return cs.upsert_client_cc_points(client_cc_points)


# #-- ClientCharges
# from ClientCharges import ClientCharges
# @app.route('/client/charges', methods=['GET'])
# def get_client_charges ():
#     return cs.client_charges()

# @app.route('/client/{client_id}/charges', methods=['GET'])
# def get_client_charges_by_client_id (client_id):
#     return cs.client_charges_by_client_id(client_id)

# @app.route('/client/charges/<id>', methods=['GET'])
# def get_client_charges_by_id (id):
#     return cs.client_charges_by_id(id)

# @app.route('/client/charges', methods=['POST'])
# def post_client_charges ( client_charges:ClientCharges):
#     return cs.upsert_client_charges(client_charges)


# #-- ClientCcBalanceTransfer
# from ClientCcBalanceTransfer import ClientCcBalanceTransfer
# @app.route('/client/cc_balance_transfer', methods=['GET'])
# def get_client_cc_balance_transfer ():
#     return cs.client_cc_balance_transfer()

# @app.route('/client/{client_id}/cc_balance_transfer', methods=['GET'])
# def get_client_cc_balance_transfer_by_client_id (client_id):
#     return cs.client_cc_balance_transfer_by_client_id(client_id)

# @app.route('/client/cc_balance_transfer/<id>', methods=['GET'])
# def get_client_cc_balance_transfer_by_id (id):
#     return cs.client_cc_balance_transfer_by_id(id)

# @app.route('/client/cc_balance_transfer', methods=['POST'])
# def post_client_cc_balance_transfer ( client_cc_balance_transfer:ClientCcBalanceTransfer):
#     return cs.upsert_client_cc_balance_transfer(client_cc_balance_transfer)


# #-- ClientCcAction
# from ClientCcAction import ClientCcAction
# @app.route('/client/cc_action', methods=['GET'])
# def get_client_cc_action ():
#     return cs.client_cc_action()

# @app.route('/client/{client_id}/cc_action', methods=['GET'])
# def get_client_cc_action_by_client_id (client_id):
#     return cs.client_cc_action_by_client_id(client_id)

# @app.route('/client/cc_action/<id>', methods=['GET'])
# def get_client_cc_action_by_id (id):
#     return cs.client_cc_action_by_id(id)

# @app.route('/client/cc_action', methods=['POST'])
# def post_client_cc_action ( client_cc_action:ClientCcAction):
#     return cs.upsert_client_cc_action(client_cc_action)


# #-- ClientSelfLender
# from ClientSelfLender import ClientSelfLender
# @app.route('/client/self_lender', methods=['GET'])
# def get_client_self_lender ():
#     return cs.client_self_lender()

# @app.route('/client/{client_id}/self_lender', methods=['GET'])
# def get_client_self_lender_by_client_id (client_id):
#     return cs.client_self_lender_by_client_id(client_id)

# @app.route('/client/self_lender/<id>', methods=['GET'])
# def get_client_self_lender_by_id (id):
#     return cs.client_self_lender_by_id(id)

# @app.route('/client/self_lender', methods=['POST'])
# def post_client_self_lender ( client_self_lender:ClientSelfLender):
#     return cs.upsert_client_self_lender(client_self_lender)


# #-- ClientCcTransaction
# from ClientCcTransaction import ClientCcTransaction
# @app.route('/client/cc_transaction', methods=['GET'])
# def get_client_cc_transaction ():
#     return cs.client_cc_transaction()

# @app.route('/client/{client_id}/cc_transaction', methods=['GET'])
# def get_client_cc_transaction_by_client_id (client_id):
#     return cs.client_cc_transaction_by_client_id(client_id)

# @app.route('/client/cc_transaction/<id>', methods=['GET'])
# def get_client_cc_transaction_by_id (id):
#     return cs.client_cc_transaction_by_id(id)

# @app.route('/client/cc_transaction', methods=['POST'])
# def post_client_cc_transaction ( client_cc_transaction:ClientCcTransaction):
#     return cs.upsert_client_cc_transaction(client_cc_transaction)
