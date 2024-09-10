from flask_restful import Resource
from resources.base_resource import BaseResource
import clients.credit_report_service as crs

class CreditReports(Resource):
    def get(self):
        return cs.get_credit_reports()

class CreditReport(BaseResource):
    def get(self, id):
        return crs.get_credit_report_by_id(id)

    def post(self, id=0):
        return super().post( id, crs.post_credit_report)

    def delete(self, id):
        return crs.delete_credit_report_by_id(id)

class CreditReportByClient(Resource):
    def get(self, client_id):
        return crs.get_credit_report_by_client_id(client_id)
