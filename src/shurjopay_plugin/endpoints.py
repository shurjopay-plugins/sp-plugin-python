from enum import Enum
from logging import NOTSET

class Endpoints(str, Enum):
    '''This class contains all the endpoints of shurjoPay API'''
    TOKEN = "get_token"
    MAKE_PMNT = "secret-pay"
    VERIFIED_ORDER = "verification"
    PMNT_STAT = "payment-status"

    