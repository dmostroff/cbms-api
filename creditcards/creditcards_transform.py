from models.CcCompanyModel import CcCompanyModel
from models.CcCardModel import CcCardModel

def CcCompanyModelJsonToModel( company_json: str) -> CcCompanyModel:
    return CcCompanyModel.parse_obj( company_json)

def CcCardModelJsonToModel( cccard_json: str) -> CcCardModel:
    return CcCardModel.parse_obj( cccard_json)
