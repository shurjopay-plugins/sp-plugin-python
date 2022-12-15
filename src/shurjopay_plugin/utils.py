from enum import Enum

class Endpoints(str, Enum):
    '''This class contains all the endpoints of Shurjopay API'''
    TOKEN = "get_token"
    MAKE_PAYMENT = "secret-pay"
    VERIFIED_ORDER = "verification"
    PAYMENT_STATUS = "payment-status"


class ShurjopayStatus(Enum):
    '''This enum class contains the status codes of Shurjopay API'''
    AUTH_SUCCESS = 200
    INVALID_ORDER_ID = '1011'
    TRANSACTION_SUCCESS = 1000



