'''
 Shurjopay Python Plugin for ShurjoPay Gateway Services.
 Author Mahabubul Hasan
 Since 2022-10-10
'''
import requests
import datetime
import json
from models import *
from logger_config import ShurjopayLoggerConfig
from utils import Endpoints, ShurjopayStatus
from shurjopay_exceptions import ShurjoPayException
from netwotk_interface import getIP


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
        # Initialize the  secret keys for plugin configuration
        self.SP_USERNAME = shurjoPayConfigModel.SP_USERNAME
        self.SP_PASSWORD = shurjoPayConfigModel.SP_PASSWORD
        self.SHURJOPAY_API = shurjoPayConfigModel.SHURJOPAY_API
        self.SP_CALLBACK = shurjoPayConfigModel.SP_CALLBACK
        self.SP_LOG_DIR = shurjoPayConfigModel.SP_LOG_DIR
        # Initialize the logger 
        self.logger = ShurjopayLoggerConfig(self.SP_LOG_DIR).get_logger()


    def authenticate(self):
        '''
        This method is used to authenticate with shurjoPay.
        return authorization token for shurjoPay payment gateway system.
        return authentication details with valid token
        raise ShurjoPayException if authentication fails
        '''
        url = self.SHURJOPAY_API + self.TOKEN_END_POINT #  Get-token URL of shurjoPay API
        payloads = {
            "username": self.SP_USERNAME,
            "password": self.SP_PASSWORD,
        }
        try:
            response = requests.post(url, data=payloads)
            token_details = response.json()
            if (int)(token_details['sp_code']) == ShurjopayStatus.AUTH_SUCCESS.value: # Check if authentication is successful
                self.logger.info(f'sp_code:{token_details["sp_code"]}, sp_message:{token_details["message"]}')
                self.AUTH_TOKEN = ShurjoPayTokenModel(**token_details) # Map token details to token model
                return self.AUTH_TOKEN
            self.logger.error(f'sp_code:{token_details["sp_code"]}, sp_message:{token_details["message"]}')
            raise ShurjoPayException(token_details['sp_code'], token_details['message'])
        except ShurjoPayException as ex:
            self.logger.error(f'{self.AUTHENTICATION_FAILED}, {ex}') # Log expception error
            raise ShurjoPayException(self.AUTHENTICATION_FAILED, ex) # Raise exception if authentication fails

    def is_token_valid(self):
        '''Check if token is valid or not by comparing token expiry time with current time'''
        return True if (datetime.datetime.strptime(
                       self.AUTH_TOKEN.token_create_time, "%Y-%m-%d %I:%M:%S%p") + datetime.timedelta(milliseconds=self.AUTH_TOKEN.expires_in)) > datetime.datetime.now() else False

    def make_payment(self, paymentReq):
        '''
        This method is used to make payment request.
        @param PaymentRequest object.
        @return PaymentDetails object containing redirect URL to reach payment page, order id to verify order in shurjoPay.
        @return None if payment request fails.
        @raise ShurjoPayException if payment fails due to token expired or invalid credentials.
        @raise ShurjoPayException  if payment fails due to invalid payment request.   
        '''
        try:
            if self.AUTH_TOKEN == None or self.is_token_valid() == False: # Check if token is valid or expired
                self.AUTH_TOKEN = self.authenticate() # Authenticate with shurjoPay
        except ShurjoPayException as ex:
            self.logger.error(f'{self.AUTHENTICATION_FAILED}: {ex}') 
            raise 
        url = self.SHURJOPAY_API + self.MAKE_PAYMENT_END_POINT # Make payment URL of shurjoPay API
        headers = {
            'content-type': 'application/json',
            'Authorization': f'{self.AUTH_TOKEN.token_type} {self.AUTH_TOKEN.token}' # Add toekn type and value to authorization header
        }
        payloads = self._map_payment_request(paymentReq) # Map payment request 
        if self.is_token_valid(): # Check if token is expired
            try:
                response = requests.post(url, headers=headers, data=json.dumps(payloads))
                response_json = response.json()
                if response_json['checkout_url'] == None: # Check if payment request is successful
                    self.logger.error(self.PAYMENT_REQUEST_FAILED)
                    return None
                self.logger.info(self.PAYMENT_REQUEST_SUCCESS)
                return PaymentDetailsModel(**response_json) # Map payment details to payment details model
            except ShurjoPayException as ex:
                self.logger.error(f'{self.PAYMENT_REQUEST_FAILED}: {ex}')
                raise ShurjoPayException(self.PAYMENT_REQUEST_FAILED, ex)
        else:
            self.logger.warning(f'{self.AUTHENTICATION_FAILED}: {self.AUTHENTICATION_TOKEN_EXPIRED}')
            raise ShurjoPayException(self.AUTHENTICATION_FAILED, self.AUTHENTICATION_TOKEN_EXPIRED) # Raise exception if token is expired

    def verify_payment(self, order_id):
        '''
        verify order using order id which is got by payment response object
        @param order_id
        @return order object if order is verified 
        @return None if order is not verified
        @raise ShurjoPayException if order verification fails due to token expired or invalid credentials.
        @raise ShurjoPayException  if order verification fails due to invalid order id.
        '''
        try:
            if self.AUTH_TOKEN == None or self.is_token_valid() == False: # Check if token is valid or expired
                self.AUTH_TOKEN = self.authenticate() # Authenticate with shurjoPay
        except ShurjoPayException as ex:
            self.logger.error(self.AUTHENTICATION_FAILED, ex)
            raise 
        url = self.SHURJOPAY_API + self.VERIFICATION_END_POINT # Verification URL of shurjoPay API
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
                    return ShurjoPayMessageModel(**response) # Map message details to message model
                self.logger.info(f'sp_code:{response["sp_code"]}, sp_message:{response["sp_message"]}')
                return VerifiedPaymentDetailsModel(**response) # Map payment details to verified payment details model
            except ShurjoPayException as ex:
                self.logger.error(f'{self.PAYMENT_VERIFICATION_FAILED}: {ex}')
                raise ShurjoPayException(self.PAYMENT_VERIFICATION_FAILED,ex)
        else:
            self.logger.warning(f'{self.AUTHENTICATION_FAILED}: {self.AUTHENTICATION_TOKEN_EXPIRED}')
            raise ShurjoPayException(self.AUTHENTICATION_FAILED, self.AUTHENTICATION_TOKEN_EXPIRED) # Raise exception if token is expired

    def check_payment_status(self, order_id):
        '''
         Check shurjoPay payment status using order-id which is retreved from callback
         @param order_id
         @return order object
         @retun None if order is not found
         @raise Exception if order verification fails due to token expired or invalid credentials.
         @raise ShurjoPayException if order verification fails due to invalid order id.
        '''
        try:
            if self.AUTH_TOKEN == None or self.is_token_valid() == False: # Check if token is valid or expired
                self.AUTH_TOKEN = self.authenticate() # Authenticate with shurjoPay
        except ShurjoPayException as ex:
            self.logger.error(self.AUTHENTICATION_FAILED, ex)
            raise 
        url = self.SHURJOPAY_API + self.PAYMENT_STATUS_END_POINT
        headers = {'content-type': 'application/json',
                   'Authorization': f'{self.AUTH_TOKEN.token_type} {self.AUTH_TOKEN.token}'}
        payloads = {'order_id': order_id}
        if self.is_token_valid():
            try:
                response = requests.post(url, headers=headers, data=json.dumps(payloads))
                response = response.json()
                if(type(response) == dict and response['sp_code'] == ShurjopayStatus.INVALID_ORDER_ID.value): # Check if order id is invalid
                    self.logger.info(f'sp_code:{response["sp_code"]}, sp_message:{response["message"]}')
                    return ShurjoPayMessageModel(**response)
                response = response[0]
                self.logger.info(f'sp_code:  {response["sp_code"]},  sp_message:{response["sp_message"]}')
                return VerifiedPaymentDetailsModel(**response) # Map payment details to verified payment details model
            except ShurjoPayException as ex:
                self.logger.error(f'{self.PAYMENT_VERIFICATION_FAILED}: {ex}')
                raise ShurjoPayException(self.PAYMENT_VERIFICATION_FAILED,ex)
        else:
            self.logger.warning(f'{self.AUTHENTICATION_FAILED}: {self.AUTHENTICATION_TOKEN_EXPIRED}') 
            raise ShurjoPayException(self.AUTHENTICATION_FAILED, self.AUTHENTICATION_TOKEN_EXPIRED) # Raise exception if token is expired

    def _map_payment_request(self, paymentReq):
        '''
        This method is used to map payment request object to payment request model
        @param payment_request
        @returns payment request model
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
