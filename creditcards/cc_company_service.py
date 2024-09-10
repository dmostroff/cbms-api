import creditcards.cc_company_repository as cr
import common.base_service as bs

from models.CcCompanyModel import CcCompanyModel



#--------------------
# cc_company
#--------------------

@bs.repository_call
def get_cc_companies ():
    return cr.get_cc_companies()

# @bs.repository_call
# def get_cc_company_by_cc_company_id (cc_company_id):
#     return cr.get_cc_company_by_cc_company_id(cc_company_id)

@bs.repository_call_single_row
def get_cc_company_by_id (id):
    return cr.get_cc_company_by_id(id)

@bs.repository_call_single_row
def post_cc_company ( cc_company:CcCompanyModel):
    return cr.upsert_cc_company(cc_company)
    # id = np.int64(df['cc_company_id'].values[0]).item()
    # return get_cc_company_by_id(id)

