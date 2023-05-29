from enum import Enum
import socket


class Endpoints(str, Enum):
    '''This class contains all the endpoints of shurjoPayAPI'''
    API = 'api/'
    TOKEN = "get_token"
    SECRET_PAY = "secret-pay"
    VERIFIFICATION = "verification"
    PAYMENT_STATUS = "payment-status"


class CustomResponse:
    """This class is used to create custom response for shurjoPayAPI during payment process

    Args:
    ----
    code(str/int): status code of the response
    message (str): message of the response
    """

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return f"HTTP Status code : {self.code} Message: {self.message}"


class ShurjopayStatus():
    '''This class contains the shurjoPayAPI Responses'''
    AUTH_SUCCESS = CustomResponse(
        200, "Successfully authenticated with Merchant")
    INVALID_ORDER_ID = CustomResponse('1011', "Invalid Payment ID")
    TRANSACTION_SUCCESS = CustomResponse('1000', "Transaction successful")


class ShurjopayException(Exception):
    '''Exceptions during payment process 

    Args:
    ---
        message: error message of different exception
        errors : errors of different exception
    '''

    def __init__(self, message, errors):
        super().__init__(message, errors)


class ShurjopayAuthException(Exception):
    '''Exceptions during authentication process 

    Args:
    ---
        message: authentication error message
        errors : authentication errors 
    '''

    def __init__(self, message, errors):
        super().__init__(message, errors)


def get_client_ip():
    '''This method is used to get the IP address of the merchant server  

    Returns:
    -------
        ip_address (str): IP address of the merchant server 

    Raises:
    ------
         ShurjoPayException while getting merchant IP address
         ShurjoPayException while getting merchant IP address
    '''

    IANA = '10.0.0.0'
    PORT = 0

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # connect() for UDP doesn't send packets
        s.connect((IANA, PORT))
        return s.getsockname()[0]
    except ShurjopayException as ex:
        raise ShurjopayException('Cannot connect to the internet"', ex)
    finally:
        s.close()
