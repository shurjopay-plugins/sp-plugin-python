'''
 Python SDK for ShurjoPay Gateway Services.
 Author Mahabubul Hasan
 Since 2022-10-10
'''
import requests
import datetime
import json
from models import ShurjoPayTokenModel, PaymentDetailsModel, VerifiedPaymentDetailsModel
from logger_config import logger
from endpoints import Endpoints
from shurjopay_exceptions import AuthException,PaymentException

class ShurjoPayPlugin(object):
    TOKEN_END_POINT = Endpoints.TOKEN.value
    VERIFICATION_END_POINT = Endpoints.VERIFIED_ORDER.value
    PAYMENT_STATUS_END_POINT = Endpoints.PMNT_STAT.value
    MAKE_PAYMENT_END_POINT = Endpoints.MAKE_PMNT.value
    AUTH_TOKEN = None
    AUTH_ERROR_MSG = 'Invalid Shurjopay Credentials!'

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
        Return authorization token for shurjoPay payment gateway system.
        Return authentication details with valid token
        Throws Exception if authentication fails
        '''
        url = self.SHURJOPAY_API + self.TOKEN_END_POINT
        payloads = {
            "username": self.SP_USERNAME,
            "password": self.SP_PASSWORD
        }
        try:
            response = requests.post(url, data=payloads)
            token_details = response.json()
            if int(token_details['sp_code']) == 200:
                logger.info(
                    'Merchant Authentication Successful!')
                self.AUTH_TOKEN = ShurjoPayTokenModel(**token_details)
                return self.AUTH_TOKEN
            else:
                raise AuthException(self.AUTH_ERROR_MSG)
        except AuthException as e:
            logger.error(self.AUTH_ERROR_MSG, e)

    def is_token_valid(self):
        # check if token is valid or not by comparing token expiration time
        return True if (datetime.datetime.strptime(
                       self.AUTH_TOKEN.token_create_time, "%Y-%m-%d %I:%M:%S%p") + datetime.timedelta(milliseconds=self.AUTH_TOKEN.expires_in)) > datetime.datetime.now() else False

    def make_payment(self, paymentReq):
        '''
        This method is used to make payment.
        @param Payment request object. See the shurjoPay version-2 integration documentation(beta).docx for details.
        @return Payment response object containing redirect URL to reach payment page, order id to verify order in shurjoPay.
        @throws Exception if payment fails due to token expired or invalid credentials.
        '''
        try:
            if self.AUTH_TOKEN == None or self.__is_token_valid() == False:
                self.AUTH_TOKEN = self.authenticate()
        except AuthException as e:
            logger.error(
                'Shurjopay Authentication Failed!', self.AUTH_ERROR_MSG)
            raise AuthException(self.AUTH_ERROR_MSG)

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
                raise PaymentException(f'Shurjopay Payment Request Failed!: {e}')
        else:
            logger.warning('Token Exired!')
            raise AuthException(self.AUTH_ERROR_MSG)

    def verify_payment(self, order_id):
        '''
        This method is used to verify order by order id which is got by payment response object
        @Param order_id
        @Return order object if order is verified 
        @Throws Exception if order verification fails due to token expired or invalid credentials.
        '''
        try:
            if self.AUTH_TOKEN == None or self.is_token_valid() == False:
                self.AUTH_TOKEN = self.authenticate()
        except AuthException as e:
            logger.error(
                'Shurjopay Authentication Faild!', self.AUTH_ERROR_MSG)
            raise AuthException(self.AUTH_ERROR_MSG)

        url = self.SHURJOPAY_API + self.VERIFICATION_END_POINT
        headers = {'content-type': 'application/json',
                   'Authorization': f'{self.AUTH_TOKEN.token_type} {self.AUTH_TOKEN.token}'}

        payloads = {'order_id': order_id}

        if self.is_token_valid():
            try:
                response = requests.post(
                    url, headers=headers, data=json.dumps(payloads))
                response_json = response.json()
                if (response_json != None):
                    logger.info(
                        'Shurjopay Payment verified!')

                return VerifiedPaymentDetailsModel(**response_json[0])

            except PaymentException as e:
                logger.error(
                    f'Shurjopay Payment Verification failed: {e}')
                raise PaymentException(f'Shurjopay Payment Verification failed: {e}')
        else:
            logger.warning('Token Exired!')
            raise AuthException(self.AUTH_ERROR_MSG)

    def check_payment_status(self, order_id):
        '''
         This method is used to check payment status by order id which is got by payment response object
         @Param order_id
         @Return order object if order is verified successfully
         @Return None if order is not verified
         @Throws Exception if order verification fails due to token expired or invalid credentials.
        '''
        try:
            if self.AUTH_TOKEN == None or self.is_token_valid() == False:
                self.AUTH_TOKEN = self.authenticate()
        except AuthException as e:
            logger.error(
                'Shurjopay Authentication Faild!', self.AUTH_ERROR_MSG)
            raise AuthException(self.AUTH_ERROR_MSG)

        url = self.SHURJOPAY_API + self.PAYMENT_STATUS_END_POINT
        headers = {'content-type': 'application/json',
                   'Authorization': f'{self.AUTH_TOKEN.token_type} {self.AUTH_TOKEN.token}'}

        payloads = {'order_id': order_id}

        if self.is_token_valid():
            try:
                response = requests.post(
                    url, headers=headers, data=json.dumps(payloads))
                response_json = response.json()

                if (response_json != None):
                    logger.info(
                        'Shurjopay Payment Checked!')
                return VerifiedPaymentDetailsModel(**response_json[0])
            except PaymentException as e:
                logger.error(
                    f'Shurjopay Payment Checking failed: {e}')
                raise PaymentException(f'Shurjopay Payment Checking failed: {e}')
        else:
            logger.warning('Token Exired!')
            raise AuthException(self.AUTH_ERROR_MSG)

    def _map_payment_request(self, paymentReq):
        '''
        This method is used to map payment request object to payment request model
        @Param payment_request
        @Return payment request model
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
            'client_ip': paymentReq.client_ip,
        }
