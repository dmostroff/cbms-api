import numpy as np
import cbmssummary_repository as cr
import base_service as bs

#--------------------
# cbms_summary
#--------------------

@bs.repository_call
def get_cbms_summary ():
    return cr.get_cbms_summary()
