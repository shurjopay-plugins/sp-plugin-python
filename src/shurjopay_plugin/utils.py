from enum import Enum
import socket
 
class Endpoints(str, Enum):
    '''This class contains all the endpoints of shurjoPayAPI'''
    TOKEN = "get_token"
    MAKE_PAYMENT = "secret-pay"
    VERIFIED_ORDER = "verification"
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
    AUTH_SUCCESS = CustomResponse(200, "Successfully authenticated with Marchent")
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

class ShurjopayAuthException(ShurjopayException):
    '''Exceptions during authentication process 
    
    Args:
    ---
        message: authentication error message
        errors : authentication errors 
    '''
    def __init__(self, message, errors):
        super().__init__(message, errors)

def get_host_ip():
    '''This method is used to get the IP address of the marchent server  
     
    Returns:
    -------
        ip_address (str): IP address of the marchent server 
    
    Raises:
    ------
         ShurjoPayException while getting marchent IP address
    '''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # connect() for UDP doesn't send packets
        s.connect(('10.0.0.0', 0)) 
        return s.getsockname()[0]
    except ShurjopayException as ex:
        raise ShurjopayException('Cannot connect to the internet"', ex) 
    finally:
        s.close()