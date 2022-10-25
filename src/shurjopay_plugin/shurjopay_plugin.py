'''
 Python SDK for ShurjoPay Gateway Services.
 Author Mahabubul Hasan
 Since 2022-10-10
'''
from .models import ShurjoPayTokenModel, PaymentDetailsModel, VerifiedPaymentDetailsModel
from .logger_config import ShurjoPayConfig
from .endpoints import Endpoints
import requests
import datetime
import json
SHURJOPAY_LOGGER = ShurjoPayConfig()


class ShurjoPayPlugin(object):
    __TOKEN_END_POINT = Endpoints.TOKEN.value
    __VERIFICATION_END_POINT = Endpoints.VERIFIED_ORDER.value
    __PAYMENT_STATUS_END_POINT = Endpoints.PMNT_STAT.value
    __MAKE_PAYMENT_END_POINT = Endpoints.MAKE_PMNT.value
    __AUTH_TOKEN = None
    _AUTH_ERROR_MSG = 'Invalid Shurjopay Credentials!'

    def __init__(self) -> None:
        pass

    def __init__(self, shurjoPayConfigModel) -> None:
        self.__SP_USERNAME = shurjoPayConfigModel.SP_USERNAME
        self.__SP_PASSWORD = shurjoPayConfigModel.SP_PASSWORD
        self.__SHURJOPAY_API = shurjoPayConfigModel.SHURJOPAY_API
        self.__SP_RETURN_URL = shurjoPayConfigModel.SP_CALLBACK
        self.__SP_CANCEL_URL = shurjoPayConfigModel.SP_CALLBACK
        pass

    def __authenticate(self):
        '''
        Return authorization token for shurjoPay payment gateway system.
        Return authentication details with valid token
        Throws Exception if authentication fails
        '''
        url = self.__SHURJOPAY_API + self.__TOKEN_END_POINT
        payloads = {
            "username": self.__SP_USERNAME,
            "password": self.__SP_PASSWORD
        }
        try:
            response = requests.post(url, data=payloads)
            token_details = response.json()
            if int(token_details['sp_code']) == 200:
                SHURJOPAY_LOGGER._logger.info(
                    'Merchant Authentication Successful!')
                self.__AUTH_TOKEN = ShurjoPayTokenModel(**token_details)
                return self.__AUTH_TOKEN
            else:
                raise Exception(self._AUTH_ERROR_MSG)
        except Exception as e:
            SHURJOPAY_LOGGER._logger.error(self._AUTH_ERROR_MSG, e)

    def __is_token_valid(self):
        # check if token is valid or not by comparing token expiration time
        return True if (datetime.datetime.strptime(
                       self.__AUTH_TOKEN.token_create_time, "%Y-%m-%d %I:%M:%S%p") + datetime.timedelta(milliseconds=self.__AUTH_TOKEN.expires_in)) > datetime.datetime.now() else False

    def make_payment(self, paymentReq):
        '''
        This method is used to make payment.
        @param Payment request object. See the shurjoPay version-2 integration documentation(beta).docx for details.
        @return Payment response object containing redirect URL to reach payment page, order id to verify order in shurjoPay.
        @throws Exception if payment fails due to token expired or invalid credentials.
        '''
        try:
            if self.__AUTH_TOKEN == None or self.__is_token_valid() == False:
                self.__AUTH_TOKEN = self.__authenticate()
        except Exception as e:
            SHURJOPAY_LOGGER._logger.error(
                'Shurjopay Authentication Failed!', self._AUTH_ERROR_MSG)
            raise Exception(self._AUTH_ERROR_MSG)

        url = self.__SHURJOPAY_API + self.__MAKE_PAYMENT_END_POINT
        headers = {
            'content-type': 'application/json',
            'Authorization': f'{self.__AUTH_TOKEN.token_type} {self.__AUTH_TOKEN.token}'
        }
        payloads = self._map_payment_request(paymentReq)

        if self.__is_token_valid:
            try:
                response = requests.post(
                    url, headers=headers, data=json.dumps(payloads))
                response_json = response.json()

                SHURJOPAY_LOGGER._logger.info(
                    'Shurjopay Payment Request Successful!')
                return PaymentDetailsModel(**response_json)
            except Exception as e:
                SHURJOPAY_LOGGER._logger.error(
                    f'Shurjopay Payment Request Failed!: {e}')
                raise Exception(f'Shurjopay Payment Request Failed!: {e}')
        else:
            SHURJOPAY_LOGGER._logger.warning('Token Exired!')
            raise Exception(self._AUTH_ERROR_MSG)

    def verify_payment(self, order_id):
        '''
        This method is used to verify order by order id which is got by payment response object
        @Param order_id
        @Return order object if order is verified 
        @Throws Exception if order verification fails due to token expired or invalid credentials.
        '''
        try:
            if self.__AUTH_TOKEN == None or self.__is_token_valid() == False:
                self.__AUTH_TOKEN = self.__authenticate()
        except Exception as e:
            SHURJOPAY_LOGGER._logger.error(
                'Shurjopay Authentication Faild!', self._AUTH_ERROR_MSG)
            raise Exception(self._AUTH_ERROR_MSG)

        url = self.__SHURJOPAY_API + self.__VERIFICATION_END_POINT
        headers = {'content-type': 'application/json',
                   'Authorization': f'{self.__AUTH_TOKEN.token_type} {self.__AUTH_TOKEN.token}'}

        payloads = {'order_id': order_id}

        if self.__is_token_valid:
            try:
                response = requests.post(
                    url, headers=headers, data=json.dumps(payloads))
                response_json = response.json()
                if (response_json != None):
                    SHURJOPAY_LOGGER._logger.info(
                        'Shurjopay Payment verified!')

                return VerifiedPaymentDetailsModel(**response_json[0])

            except Exception as e:
                SHURJOPAY_LOGGER._logger.error(
                    f'Shurjopay Payment Verification failed: {e}')
                raise Exception(f'Shurjopay Payment Verification failed: {e}')
        else:
            SHURJOPAY_LOGGER._logger.warning('Token Exired!')
            raise Exception(self._AUTH_ERROR_MSG)

    def check_payment_status(self, order_id):
        '''
         This method is used to check payment status by order id which is got by payment response object
         @Param order_id
         @Return order object if order is verified successfully
         @Return None if order is not verified
         @Throws Exception if order verification fails due to token expired or invalid credentials.
        '''
        try:
            if self.__AUTH_TOKEN == None or self.__is_token_valid() == False:
                self.__AUTH_TOKEN = self.__authenticate()
        except Exception as e:
            self.__SHURJOPAY_CONFIG._logger.error(
                'Shurjopay Authentication Faild!', self._AUTH_ERROR_MSG)
            raise Exception(self._AUTH_ERROR_MSG)

        url = self.__SHURJOPAY_API + self.__PAYMENT_STATUS_END_POINT
        headers = {'content-type': 'application/json',
                   'Authorization': f'{self.__AUTH_TOKEN.token_type} {self.__AUTH_TOKEN.token}'}

        payloads = {'order_id': order_id}

        if self.__is_token_valid:
            try:
                response = requests.post(
                    url, headers=headers, data=json.dumps(payloads))
                response_json = response.json()

                if (response_json != None):
                    SHURJOPAY_LOGGER._logger.info(
                        'Shurjopay Payment Checked!')
                return VerifiedPaymentDetailsModel(**response_json[0])
            except Exception as e:
                SHURJOPAY_LOGGER._logger.error(
                    f'Shurjopay Payment Checking failed: {e}')
                raise Exception(f'Shurjopay Payment Checking failed: {e}')
        else:
            SHURJOPAY_LOGGER._logger.warning('Token Exired!')
            raise Exception(self._AUTH_ERROR_MSG)

    def _map_payment_request(self, paymentReq):
        '''
        This method is used to map payment request object to payment request model
        @Param payment_request
        @Return payment request model
        '''
        return {
            'token': self.__AUTH_TOKEN.token,
            'return_url': self.__SP_RETURN_URL,
            'cancel_url': self.__SP_CANCEL_URL,
            'store_id': self.__AUTH_TOKEN.store_id,
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