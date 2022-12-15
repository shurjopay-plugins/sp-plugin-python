'''
 Shurjopay Python Plugin for ShurjoPay Gateway Services.
 Author Mahabubul Hasan
 Since 2022-10-10
'''
import requests
import datetime
import json
from .models import *
from .logger_config import ShurjopayLoggerConfig
from .utils import Endpoints, ShurjopayStatus
from .shurjopay_exceptions import ShurjopayException
from .netwotk_interface import getIP


class ShurjopayPlugin(object):
    '''
        ShurjoPay Python Plugin for shurjoPay Gateway Services.
        Includes all the methods - authenticate, makepayemnt, verify payment, check payment for shurjoPay payment gateway system.
        Intrigrate the plugin with your python application to make payment with shurjoPay.
        For more details view the shurjoPay version-3 integration documentation : https://docs.google.com/document/d/19J4HE0j873nBJqcN-uRBYYAa_qBA3p1XSY-jy2fwvEE/edit .    
    '''
    # API Endpoints of shurjoPay API
    TOKEN_END_POINT = Endpoints.TOKEN.value
    VERIFICATION_END_POINT = Endpoints.VERIFIED_ORDER.value
    PAYMENT_STATUS_END_POINT = Endpoints.PAYMENT_STATUS.value
    MAKE_PAYMENT_END_POINT = Endpoints.MAKE_PAYMENT.value
    AUTH_TOKEN = None # Shurjopay Token Model

    # Status Message
    AUTHENTICATION_SUCCESS = 'Marchent Authentication Successful!'
    AUTHENTICATION_FAILED = 'Marchent Authentication Failed!'
    AUTHENTICATION_TOKEN_EXPIRED = 'Shurjopay Token Expired!'
    PAYMENT_REQUEST_SUCCESS = 'Shurjopay Payment Request Successful!'
    PAYMENT_REQUEST_FAILED = 'Shurjopay Payment Request Failed!'
    PAYMENT_VERIFICATION_FAILED = 'Shurjopay Payment Verification Failed!'
    PAYMENT_CHECK_FAILED = 'Shurjopay Payment Checking Failed!'

    
    def __init__(self, shurjoPayConfigModel) -> None:
        # Initialize the configuration keys for plugin configuration
        self.SP_USERNAME = shurjoPayConfigModel.SP_USERNAME
        self.SP_PASSWORD = shurjoPayConfigModel.SP_PASSWORD
        self.SP_ENDPOINT = shurjoPayConfigModel.SP_ENDPOINT
        self.SP_CALLBACK = shurjoPayConfigModel.SP_CALLBACK
        self.SP_LOGDIR = shurjoPayConfigModel.SP_LOGDIR
        # Initialize the shurjopay logger configuration 
        self.logger = ShurjopayLoggerConfig(self.SP_LOGDIR).get_logger()


    def authenticate(self):
        '''
        This method is used to authenticate with shurjoPay.
        :return authorization token for shurjoPay payment gateway system.
        :return authentication details with valid token
        :raise ShurjopayException if authentication fails
        '''
        # Create token endpoint url
        url = self.SP_ENDPOINT + self.TOKEN_END_POINT
        payloads = {
            "username": self.SP_USERNAME,
            "password": self.SP_PASSWORD,
        }
        try:
            response = requests.post(url, data=payloads)
            token_details = response.json()
            # Check if authentication is successful
            if (int)(token_details['sp_code']) == ShurjopayStatus.AUTH_SUCCESS.value: 
                self.logger.info(f'sp_code:{token_details["sp_code"]}, sp_message:{token_details["message"]}')
                 # Map token details to token model
                self.AUTH_TOKEN = ShurjoPayTokenModel(**token_details)
                return self.AUTH_TOKEN
            self.logger.error(f'sp_code:{token_details["sp_code"]}, sp_message:{token_details["message"]}')
            raise ShurjopayException(token_details['sp_code'], token_details['message'])
        except ShurjopayException as ex:
            # Log authentication expception error
            self.logger.error(f'{self.AUTHENTICATION_FAILED}, {ex}') 
            # Raise exception if authentication fails
            raise ShurjopayException(self.AUTHENTICATION_FAILED, ex) 

    def is_token_valid(self):
        '''
        Check if token is valid or not by comparing token expiry time with current time
        :return True if token is valid else None
        '''
        return True if (datetime.datetime.strptime(
                       self.AUTH_TOKEN.token_create_time, "%Y-%m-%d %I:%M:%S%p") + datetime.timedelta(milliseconds=self.AUTH_TOKEN.expires_in)) > datetime.datetime.now() else False

    def make_payment(self, paymentReq):
        r'''
        This method is used to make payment request.
        :param PaymentRequest object.
        :return PaymentDetails object containing redirect URL to reach payment page, order id to verify order in shurjoPay.
        :return None if payment request fails.
        :raise ShurjopayException if payment fails due to token expired or invalid credentials.
        :raise ShurjopayException  if payment fails due to invalid payment request.   
        '''
        try:
            # Check if token is valid or expired
            if self.AUTH_TOKEN == None or self.is_token_valid() == False: 
                # Authenticate with shurjoPay
                self.AUTH_TOKEN = self.authenticate()
        except ShurjopayException as ex:
            self.logger.error(f'{self.AUTHENTICATION_FAILED}: {ex}') 
            raise 
         # Create make payment endpoint url
        url = self.SP_ENDPOINT + self.MAKE_PAYMENT_END_POINT
        headers = {
            'content-type': 'application/json',
            'Authorization': f'{self.AUTH_TOKEN.token_type} {self.AUTH_TOKEN.token}' 
        }
        # Map data from authentication token to payment request object
        payloads = self._map_payment_request(paymentReq) 
        if self.is_token_valid():
            try:
                response = requests.post(url, headers=headers, data=json.dumps(payloads))
                response_json = response.json()
                 # Check if payment request is successful
                if response_json['checkout_url'] == None:
                    self.logger.error(self.PAYMENT_REQUEST_FAILED)
                    return None
                self.logger.info(self.PAYMENT_REQUEST_SUCCESS)
                # Return payment detais object
                return PaymentDetailsModel(**response_json) 
            except ShurjopayException as ex:
                self.logger.error(f'{self.PAYMENT_REQUEST_FAILED}: {ex}')
                raise ShurjopayException(self.PAYMENT_REQUEST_FAILED, ex)
        else:
            self.logger.warning(f'{self.AUTHENTICATION_FAILED}: {self.AUTHENTICATION_TOKEN_EXPIRED}')
            raise ShurjopayException(self.AUTHENTICATION_FAILED, self.AUTHENTICATION_TOKEN_EXPIRED) 

    def verify_payment(self, order_id):
        '''
        Verify order using order id which is got by payment response object
        :param order_id
        :return verified payment object if payment is verified 
        :return None if invalid order id passed
        :raise ShurjopayException if payment verification fails due to token expired or invalid credentials.
        :raise ShurjopayException if payment is not successfull
        '''
        try:
            # Check if token is valid or expired
            if self.AUTH_TOKEN == None or self.is_token_valid() == False: 
                # Authenticate with shurjoPay
                self.AUTH_TOKEN = self.authenticate() 
        except ShurjopayException as ex:
            self.logger.error(self.AUTHENTICATION_FAILED, ex)
            raise 
        # Create verify payment endpoint url
        url = self.SP_ENDPOINT + self.VERIFICATION_END_POINT 
        headers = {'content-type': 'application/json',
                   'Authorization': f'{self.AUTH_TOKEN.token_type} {self.AUTH_TOKEN.token}'}
        payloads = {'order_id': order_id}
        if self.is_token_valid():
            try:
                response = requests.post(url, headers=headers, data=json.dumps(payloads))
                response = response.json()
                response = response[0]
                if(response['sp_code'] == ShurjopayStatus.INVALID_ORDER_ID.value):
                    self.logger.info(f'sp_code:{response["sp_code"]}, sp_message:{response["message"]}') 
                    return None
                elif(response['sp_code'] != ShurjopayStatus.TRANSACTION_SUCCESS.value):
                    self.logger.info(f'sp_code:{response["sp_code"]}, sp_message:{response["sp_message"]}')
                    # Raise exception if payment verification fails
                    raise ShurjopayException(self.PAYMENT_VERIFICATION_FAILED, response['sp_message']) 
                self.logger.info(f'sp_code:{response["sp_code"]}, sp_message:{response["sp_message"]}')
                # Return  verified payment detais object
                return VerifiedPaymentDetailsModel(**response) 
            except ShurjopayException as ex:
                self.logger.error(f'{self.PAYMENT_VERIFICATION_FAILED}: {ex}')
                raise ShurjopayException(self.PAYMENT_VERIFICATION_FAILED,ex)
        else:
            self.logger.warning(f'{self.AUTHENTICATION_FAILED}: {self.AUTHENTICATION_TOKEN_EXPIRED}')
            raise ShurjopayException(self.AUTHENTICATION_FAILED, self.AUTHENTICATION_TOKEN_EXPIRED)

    def check_payment_status(self, order_id):
        '''
         This method is used to check Shurjopay payment status using order-id which is retreved from callback
         :param order_id 
         :return verified order object
         :retun None if invalid order id passed
         :raise Exception if order verification fails due to token expired or invalid credentials.
         :raise ShurjopayException if order verification fails due to invalid order id.
        '''
        try:
            # Check if token is none or expired and authenticate based on token validity
            if self.AUTH_TOKEN == None or self.is_token_valid() == False:
                self.AUTH_TOKEN = self.authenticate()
        except ShurjopayException as ex:
            self.logger.error(self.AUTHENTICATION_FAILED, ex)
            raise 
        url = self.SP_ENDPOINT + self.PAYMENT_STATUS_END_POINT
        headers = {'content-type': 'application/json',
                   'Authorization': f'{self.AUTH_TOKEN.token_type} {self.AUTH_TOKEN.token}'}
        payloads = {'order_id': order_id}
        if self.is_token_valid():
            try:
                response = requests.post(url, headers=headers, data=json.dumps(payloads))
                response = response.json()
                # Check if order id is invalid
                if(type(response) == dict and response['sp_code'] == ShurjopayStatus.INVALID_ORDER_ID.value): 
                    self.logger.info(f'sp_code:{response["sp_code"]}, sp_message:{response["message"]}')
                    return None
                response = response[0]
                self.logger.info(f'sp_code:  {response["sp_code"]},  sp_message:{response["sp_message"]}')
                # Return verified payment details object
                return VerifiedPaymentDetailsModel(**response) 
            except ShurjopayException as ex:
                self.logger.error(f'{self.PAYMENT_VERIFICATION_FAILED}: {ex}')
                raise ShurjopayException(self.PAYMENT_VERIFICATION_FAILED,ex)
        else:
            self.logger.warning(f'{self.AUTHENTICATION_FAILED}: {self.AUTHENTICATION_TOKEN_EXPIRED}') 
            raise ShurjopayException(self.AUTHENTICATION_FAILED, self.AUTHENTICATION_TOKEN_EXPIRED) 
    def _map_payment_request(self, paymentReq):
        '''
        This method is used to map payment request object to payment request model
        :param payment_request
        :returns payment request model
        '''
        return {
            'token': self.AUTH_TOKEN.token,
            'return_url': self.SP_CALLBACK,
            'cancel_url': self.SP_CALLBACK,
            'store_id': self.AUTH_TOKEN.store_id,
            'prefix': paymentReq.prefix,
            'amount': paymentReq.amount,
            'order_id':  paymentReq.order_id,
            'currency': paymentReq.currency,
            'customer_name':  paymentReq.customer_name,
            'customer_address': paymentReq.customer_address,
            'customer_phone': paymentReq.customer_phone,
            'customer_city':  paymentReq.customer_city,
            'customer_post_code':  paymentReq.customer_post_code,
            'client_ip': getIP(),
        }
