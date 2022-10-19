'''
 Plugin service to provide shurjoPay gateway services.
 Author Mahabubul Hasan
 Since 2022-10-10
'''
import logging
from models import ShurjoPayTokenModel, PaymentDetailsModel, VerifiedPaymentDetailsModel, PaymentRequestModel
from shurjopay_config import ShurjopayConfig
from endpoints import Endpoints
import requests
import datetime
import json


class ShurjoPayPlugin(object):
    __SHURJOPAY_CONFIG = ShurjopayConfig()
    __SP_USERNAME = __SHURJOPAY_CONFIG._env('SP_USERNAME')
    __SP_PASSWORD = __SHURJOPAY_CONFIG._env('SP_PASSWORD')
    __SHURJOPAY_API = __SHURJOPAY_CONFIG._env('SHURJOPAY_API')
    __SP_RETURN_URL = __SHURJOPAY_CONFIG._env('SP_CALLBACK')
    __SP_CANCEL_URL = __SHURJOPAY_CONFIG._env('SP_CALLBACK')
    __TOKEN_END_POINT = Endpoints.TOKEN.value
    __VERIFICATION_END_POINT = Endpoints.VERIFIED_ORDER.value
    __PAYMENT_STATUS_END_POINT = Endpoints.PMNT_STAT.value
    __MAKE_PAYMENT_END_POINT = Endpoints.MAKE_PMNT.value
    __AUTH_TOKEN = None
    _AUTH_ERROR_MSG = 'Invalid User name or Password due to ShurjoPay Authentication.'

    def __init__(self) -> None:
        pass

    def __authenticate(self):
        '''
        Return authorization token for shurjoPay payment gateway system.
        Return authentication details with valid token
        throws Exception if authentication fails
        '''
        _url = self.__SHURJOPAY_API + self.__TOKEN_END_POINT
        _payloads = {
            "username": self.__SP_USERNAME,
            "password": self.__SP_PASSWORD
        }
        if (self.__SHURJOPAY_CONFIG._logger.level == logging.DEBUG):
            self.__SHURJOPAY_CONFIG._logger.debug(
                f'url: {_url}, payload: {_payloads}')
        try:
            response = requests.post(_url, data=_payloads)
            token_details = response.json()
            if (self.__SHURJOPAY_CONFIG._logger.level == logging.DEBUG):
                self.__SHURJOPAY_CONFIG._logger.debug(token_details)
            if int(token_details['sp_code']) == 200:
                self.__SHURJOPAY_CONFIG._logger.info(
                    'Merchant authentication successful!')
                if (self.__SHURJOPAY_CONFIG._logger.level == logging.DEBUG):
                    self.__SHURJOPAY_CONFIG._logger.debug(
                        f"response: {token_details}")
                self.__AUTH_TOKEN = ShurjoPayTokenModel(**token_details)
                return self.__AUTH_TOKEN
            else:
                raise Exception(self._AUTH_ERROR_MSG)
        except Exception as e:
            self.__SHURJOPAY_CONFIG._logger.error(self._AUTH_ERROR_MSG, e)

    def __is_token_valid(self):
        # check if token is valid or not by comparing token expiration time
        return True if (datetime.datetime.strptime(
                       self.__AUTH_TOKEN.token_create_time, "%Y-%m-%d %I:%M:%S%p") + datetime.timedelta(milliseconds=self.__AUTH_TOKEN.expires_in)) > datetime.datetime.now() else False

    def make_payment(self, paymentReq):
        '''
        This method is used to make payment.
        @param Payment request object. See the shurjoPay version-2 integration documentation(beta).docx for details.
        @return Payment response object containing redirect URL to reach payment page, order id to verify order in shurjoPay.
        '''
        try:
            if self.__AUTH_TOKEN == None or self.__is_token_valid() == False:
                self.__AUTH_TOKEN = self.__authenticate()
        except Exception as e:
            self.__SHURJOPAY_CONFIG._logger.error(
                'Shurjopay Authentication Faild!', self._AUTH_ERROR_MSG)

        finally:
            if self.__AUTH_TOKEN == None or self.__is_token_valid() == False:
                self.__AUTH_TOKEN = self.__authenticate()

        _url = self.__SHURJOPAY_API + self.__MAKE_PAYMENT_END_POINT
        _headers = {
            'content-type': 'application/json',
            'Authorization': f'{self.__AUTH_TOKEN.token_type} {self.__AUTH_TOKEN.token}'
        }
        _payloads = self._map_payment_request(paymentReq)

        if (self.__SHURJOPAY_CONFIG._logger.level == logging.DEBUG):
            self.__SHURJOPAY_CONFIG._logger.debug(
                f'url: {_url}, payload: {_payloads}')

        if self.__is_token_valid:
            try:
                response = requests.post(
                    _url, headers=_headers, data=json.dumps(_payloads))
                response_json = response.json()

                if (self.__SHURJOPAY_CONFIG._logger.level == logging.DEBUG):
                    self.__SHURJOPAY_CONFIG._logger.debug(
                        f'Shurjopay Payment Response: {response_json}')

                self.__SHURJOPAY_CONFIG._logger.info(
                    'Shurjopay Payment verified!')
                return PaymentDetailsModel(**response_json)
            except Exception as e:
                self.__SHURJOPAY_CONFIG._logger.error(
                    f'Payment request failed: {e}')
        else:
            self.__SHURJOPAY_CONFIG._logger.warning('Token Exired!')
            pass

    def verify_payment(self, order_id):
        '''
        This method is used to verify order by order id which is got by payment response object
        @param orderId
        @return order object if order is verified successfully
        '''
        try:
            if self.__AUTH_TOKEN == None or self.__is_token_valid() == False:
                self.__AUTH_TOKEN = self.__authenticate()
        except Exception as e:
            self.__SHURJOPAY_CONFIG._logger.error(
                'Shurjopay Authentication Faild!', self._AUTH_ERROR_MSG)

        finally:
            if self.__AUTH_TOKEN == None or self.__is_token_valid() == False:
                self.__AUTH_TOKEN = self.__authenticate()

        _url = self.__SHURJOPAY_API + self.__VERIFICATION_END_POINT
        _headers = {'content-type': 'application/json',
                    'Authorization': f'{self.__AUTH_TOKEN.token_type} {self.__AUTH_TOKEN.token}'}

        _payloads = {'order_id': order_id}

        if (self.__SHURJOPAY_CONFIG._logger.level == logging.DEBUG):
            self.__SHURJOPAY_CONFIG._logger.debug(
                f'url: {_url}, payload: {_payloads}')

        if self.__is_token_valid:
            try:
                response = requests.post(
                    _url, headers=_headers, data=json.dumps(_payloads))
                response_json = response.json()
                if (self.__SHURJOPAY_CONFIG._logger.level == logging.DEBUG):
                    self.__SHURJOPAY_CONFIG._logger.debug(
                        f'Shurjopay Payment Response: {response_json}')

                if (response_json != None):
                    self.__SHURJOPAY_CONFIG._logger.info(
                        'Shurjopay Payment verified!')

                return VerifiedPaymentDetailsModel(**response_json[0])

            except Exception as e:
                self.__SHURJOPAY_CONFIG._logger.error(
                    f'Shurjopay Payment Verification failed: {e}')
        else:
            self.__SHURJOPAY_CONFIG._logger.warning('Shurjopay Token Exired!')
            pass

    def check_payment_status(self, order_id):
        '''
         This method is used to verify order by order id which is got by payment response object
         @param orderId
         @return order object if order is verified successfully
         '''
        try:
            if self.__AUTH_TOKEN == None or self.__is_token_valid() == False:
                self.__AUTH_TOKEN = self.__authenticate()
        except Exception as e:
            self.__SHURJOPAY_CONFIG._logger.error(
                'Shurjopay Authentication Faild!', self._AUTH_ERROR_MSG)
        finally:
            if self.__AUTH_TOKEN == None or self.__is_token_valid() == False:
                self.__AUTH_TOKEN = self.__authenticate()

        _url = self.__SHURJOPAY_API + self.__PAYMENT_STATUS_END_POINT
        _headers = {'content-type': 'application/json',
                    'Authorization': f'{self.__AUTH_TOKEN.token_type} {self.__AUTH_TOKEN.token}'}

        _payloads = {'order_id': order_id}

        if (self.__SHURJOPAY_CONFIG._logger.level == logging.DEBUG):
            self.__SHURJOPAY_CONFIG._logger.debug(
                f'url: {_url}, payload: {_payloads}')

        if self.__is_token_valid:
            try:
                response = requests.post(
                    _url, headers=_headers, data=json.dumps(_payloads))
                response_json = response.json()

                if (self.__SHURJOPAY_CONFIG._logger.level == logging.DEBUG):
                    self.__SHURJOPAY_CONFIG._logger.debug(
                        f'Shurjopay Payment Response: {response_json[0]}')

                if (response_json != None):
                    self.__SHURJOPAY_CONFIG._logger.info(
                        'Shurjopay Payment Checked!')

                return VerifiedPaymentDetailsModel(**response_json[0])
            except Exception as e:
                self.__SHURJOPAY_CONFIG._logger.error(
                    f'Payment Checking failed: {e}')
        else:
            self.__SHURJOPAY_CONFIG._logger.warning('Token Exired!')
            pass

    def _map_payment_request(self, paymentReq):
        '''
        This method is used to map payment request object to payment request model
        @param payment_request
        @return payment request model
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
