from enum import Enum
from logging import NOTSET


class Endpoints(str, Enum):
    TOKEN = "get_token"
    MAKE_PMNT = "secret-pay"
    VERIFIED_ORDER = "verification"
    PMNT_STAT = "payment-status"
