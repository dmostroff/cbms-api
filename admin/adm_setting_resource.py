from flask import request
from flask_restful import Resource
import admin.adm_setting_service as admserv
from models.AdmSettingModel import AdmSettingModel


class AdmSettings(Resource):
    def get(self):
        return admserv.get_adm_settings()

class AdmSetting(Resource):
    def get(self, id):
        return admserv.get_adm_setting_by_id(id)

class AdmSettingByPrefix(Resource):
    def get(self, prefix):
        return admserv.get_adm_setting_by_prefix(prefix)

class AdmSettingPost(Resource):
    def post(self):
        adm_setting = AdmSettingModel.parse_obj(request.get_json())
        retval = admserv.upsert_adm_setting( adm_setting)
        return retval
