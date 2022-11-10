'''
 Python SDK for ShurjoPay Gateway Services.
 Author Mahabubul Hasan
 Since 2022-10-10
'''
import requests
import datetime
import json
from .models import ShurjoPayTokenModel, PaymentDetailsModel, VerifiedPaymentDetailsModel
from .logger_config import logger
from .endpoints import Endpoints
from .shurjopay_exceptions import AuthException, PaymentException
from .shurjopay_status_codes import *
from .netwotk_interface import getIP


class ShurjoPayPlugin(object):
    '''
        ShurjoPay Python Plugin for shurjoPay Gateway Services.
        Includes all the methods to make payment and verify payment.
        For more details view the shurjoPay version-3 integration documentation : https://docs.google.com/document/d/19J4HE0j873nBJqcN-uRBYYAa_qBA3p1XSY-jy2fwvEE/edit .
    '''
    TOKEN_END_POINT = Endpoints.TOKEN.value
    VERIFICATION_END_POINT = Endpoints.VERIFIED_ORDER.value
    PAYMENT_STATUS_END_POINT = Endpoints.PMNT_STAT.value
    MAKE_PAYMENT_END_POINT = Endpoints.MAKE_PMNT.value
    AUTH_TOKEN = None

    def __init__(self) -> None:
        pass

    def __init__(self, shurjoPayConfigModel) -> None:
        self.SP_USERNAME = shurjoPayConfigModel.SP_USERNAME
        self.SP_PASSWORD = shurjoPayConfigModel.SP_PASSWORD
        self.SHURJOPAY_API = shurjoPayConfigModel.SHURJOPAY_API
        self.SP_RETURN_URL = shurjoPayConfigModel.SP_CALLBACK
        self.SP_CANCEL_URL = shurjoPayConfigModel.SP_CALLBACK
        pass

    def authenticate(self):
        '''
        This method is used to authenticate with shurjoPay.
        returns authorization token for shurjoPay payment gateway system.
        returns authentication details with valid token
        throws Exception if authentication fails
        '''
        url = self.SHURJOPAY_API + self.TOKEN_END_POINT
        payloads = {
            "username": self.SP_USERNAME,
            "password": self.SP_PASSWORD,
        }
        try:
            response = requests.post(url, data=payloads)
            token_details = response.json()
            if (token_details['sp_code']) == POST_SUCCESS[0]:
                logger.info(
                    'Merchant Authentication Successful!')
                self.AUTH_TOKEN = ShurjoPayTokenModel(**token_details)
                return self.AUTH_TOKEN

        except AuthException as e:
            logger.error(AUTHENTICATION_FAILED[1])
            raise AuthException(AUTHENTICATION_FAILED[1], e)

    def is_token_valid(self):
        '''Check if token is valid or not by comparing token expiry time with current time'''
        return True if (datetime.datetime.strptime(
                       self.AUTH_TOKEN.token_create_time, "%Y-%m-%d %I:%M:%S%p") + datetime.timedelta(milliseconds=self.AUTH_TOKEN.expires_in)) > datetime.datetime.now() else False

    def make_payment(self, paymentReq):
        '''
        This method is used to make payment request.
        @param Payment request object. See the shurjoPay version-2 integration documentation(beta).docx for details.
        @returns Payment response object containing redirect URL to reach payment page, order id to verify order in shurjoPay.
        @raise AuthException if payment fails due to token expired or invalid credentials.
        @raise PaymentException  if payment fails due to invalid payment request.   
        '''

        try:
            if self.AUTH_TOKEN == None or self.is_token_valid() == False:
                self.AUTH_TOKEN = self.authenticate()
        except AuthException as e:
            logger.error(
                'Shurjopay Authentication Failed!', AUTHENTICATION_FAILED[1])
            raise AuthException(AUTHENTICATION_FAILED[1])

        url = self.SHURJOPAY_API + self.MAKE_PAYMENT_END_POINT
        headers = {
            'content-type': 'application/json',
            'Authorization': f'{self.AUTH_TOKEN.token_type} {self.AUTH_TOKEN.token}'
        }
        payloads = self._map_payment_request(paymentReq)

        if self.is_token_valid():
            try:
                response = requests.post(
                    url, headers=headers, data=json.dumps(payloads))

                response_json = response.json()

                logger.info(
                    'Shurjopay Payment Request Successful!')
                return PaymentDetailsModel(**response_json)
            except PaymentException as e:
                logger.error(
                    f'Shurjopay Payment Request Failed!: {e}')
                raise PaymentException(
                    f'Shurjopay Payment Request Failed!: {e}')
        else:
            logger.warning('Token Exired!')
            raise AuthException(AUTHENTICATION_FAILED[1])

    def verify_payment(self, order_id):
        '''
        This method is used to verify order by order id which is got by payment response object
        @param order_id
        @return order object if order is verified 
        @raise AuthException if order verification fails due to token expired or invalid credentials.
        @raise PaymentException  if order verification fails due to invalid order id.
        '''
        try:
            if self.AUTH_TOKEN == None or self.is_token_valid() == False:
                self.AUTH_TOKEN = self.authenticate()
        except AuthException as e:
            logger.error(
                'Shurjopay Authentication Faild!', AUTHENTICATION_FAILED[1])
            raise AuthException(AUTHENTICATION_FAILED[1])

        url = self.SHURJOPAY_API + self.VERIFICATION_END_POINT
        headers = {'content-type': 'application/json',
                   'Authorization': f'{self.AUTH_TOKEN.token_type} {self.AUTH_TOKEN.token}'}

        payloads = {'order_id': order_id}

        if self.is_token_valid():
            try:
                response = requests.post(
                    url, headers=headers, data=json.dumps(payloads))
                response_json = response.json()
                response_json = response_json[0]
                if (int)(response_json['sp_code']) == INVALID_ORDER_ID[0]:
                    logger.log(INVALID_ORDER_ID[1])
                    raise PaymentException(INVALID_ORDER_ID[1])
                logger.info(
                    'Shurjopay Payment verified!')
                return VerifiedPaymentDetailsModel(**response_json)

            except PaymentException as e:
                logger.error(
                    f'Shurjopay Payment Verification failed: {e}')
                raise PaymentException(
                    f'Shurjopay Payment Verification failed: {e}')
        else:
            logger.warning('Token Exired!')
            raise AuthException(AUTHENTICATION_FAILED[1])

    def check_payment_status(self, order_id):
        '''
         This method is used to check payment status by order id which is got by payment response object
         @Param order_id
         @returns order object if order is verified successfully
         @returns None if order is not verified
         @raise Exception if order verification fails due to token expired or invalid credentials.
         @raise PaymentException if order verification fails due to invalid order id.

        '''
        try:
            if self.AUTH_TOKEN == None or self.is_token_valid() == False:
                self.AUTH_TOKEN = self.authenticate()
        except AuthException as e:
            logger.error(
                'Shurjopay Authentication Faild!', AUTHENTICATION_FAILED[1])
            raise AuthException(AUTHENTICATION_FAILED[1])

        url = self.SHURJOPAY_API + self.PAYMENT_STATUS_END_POINT
        headers = {'content-type': 'application/json',
                   'Authorization': f'{self.AUTH_TOKEN.token_type} {self.AUTH_TOKEN.token}'}

        payloads = {'order_id': order_id}

        if self.is_token_valid():
            try:
                response = requests.post(
                    url, headers=headers, data=json.dumps(payloads))
                response_json = response.json()
                response_json = response_json[0]
                if (int)(response_json['sp_code']) == INVALID_ORDER_ID[0]:
                    logger.log(INVALID_ORDER_ID[1])
                    raise PaymentException(INVALID_ORDER_ID[1])
                logger.info(
                    'Shurjopay Payment Checked!')
                return VerifiedPaymentDetailsModel(**response_json)
            except PaymentException as e:
                logger.error(
                    f'Shurjopay Payment Checking failed: {e}')
                raise PaymentException(
                    f'Shurjopay Payment Checking failed: {e}')
        else:
            logger.warning('Token Exired!')
            raise AuthException(AUTHENTICATION_FAILED[1])

    def _map_payment_request(self, paymentReq):
        '''
        This method is used to map payment request object to payment request model
        @param payment_request
        @returns payment request model
        '''
        return {
            'token': self.AUTH_TOKEN.token,
            'return_url': self.SP_RETURN_URL,
            'cancel_url': self.SP_CANCEL_URL,
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
