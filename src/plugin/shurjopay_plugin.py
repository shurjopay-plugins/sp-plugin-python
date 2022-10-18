'''
 Plug-in service to provide shurjoPay get way services.
 Author Mahabubul Hasan
 Since 2022-10-10
'''
from models import ShurjoPayToken, PaymentDetails, VerifiedPaymentDetails
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
    __SP_CALLBACK = __SHURJOPAY_CONFIG._env('SP_CALLBACK')
    __TOKEN_END_POINT = Endpoints.TOKEN.value
    __VERIFICATION_END_POINT = Endpoints.VERIFIED_ORDER.value
    __PAYMENT_STATUS_END_POINT = Endpoints.PMNT_STAT.value
    __MAKE_PAYMENT_END_POINT = Endpoints.MAKE_PMNT.value
    __AUTH_TOKEN = None

    _authError = "Invalid User name or Password due to shurjoPay authentication."

    def __init__(self) -> None:
        pass

    def _authenticate(self):
        '''
        Return authorization token for shurjoPay payment gateway system.
        Return authentication details with valid token
        throws AuthenticationException if authentication failed
        '''
        URL = self.__SHURJOPAY_API + self.__TOKEN_END_POINT
        payload = {
            "username": self.__SP_USERNAME,
            "password": self.__SP_PASSWORD
        }
        self.__SHURJOPAY_CONFIG._logger.info(payload)
        self.__SHURJOPAY_CONFIG._logger.info(URL)
        if (self.__SHURJOPAY_CONFIG._logger.level == 'DEBUG'):
            self.__SHURJOPAY_CONFIG._logger.debug(
                f'url: {URL}, payload: {payload}')
        try:
            response = requests.post(URL, data=payload)
            token_details = response.json()
            if (self.__SHURJOPAY_CONFIG._logger.level == 'DEBUG'):
                self.__SHURJOPAY_CONFIG._logger.debug(token_details)
            if int(token_details["sp_code"]) == 200:
                if (self.__SHURJOPAY_CONFIG._logger.level == 'DEBUG'):
                    self.__SHURJOPAY_CONFIG._logger.info(
                        f"response: {token_details}")
                self.__AUTH_TOKEN = ShurjoPayToken(**token_details)
            else:
                raise Exception(self._authError)
        except Exception as e:
            self.__SHURJOPAY_CONFIG._logger.error(self._authError)

    def __is_token_valid(self):
        return True if (self.__AUTH_TOKEN.token_create_time + datetime.timedelta(milliseconds=self.__AUTH_TOKEN.expires_in)) > datetime.datetime.now() else False

    '''
     * This method is used for making payment. 
	 * @param Payment request object. See the shurjoPay version-2 integration documentation(beta).docx for details.
	 * @return Payment response object contains redirect URL to reach payment page, order id to verify order in shurjoPay.
	'''

    def _make_payment(self, paymentReq):
        try:
            if self.__AUTH_TOKEN == None or self.__is_token_valid() == False:
                self.authToken = self.__authenticate()
        except Exception as e:
            self.__SHURJOPAY_CONFIG._logger.error(self._authError)

        finally:
            self.__AUTH_TOKEN = self.__authenticate()

        _headers = {'content-type': 'application/json',
                    'Authorization': f'{self.__AUTH_TOKEN.token_type} {self.__AUTH_TOKEN.token}'}

        _payloads = {
            'token': self.__AUTH_TOKEN.token,
            'return_url': self.__RETURN_URL,
            'cancel_url': self.__CANCEL_URL,
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

        if self.__is_token_valid:
            logger.info(
                f'url: {self.__AUTH_TOKEN.execute_url}, header:{_headers}, payload: {_payloads}')
            response = requests.post(
                self.__AUTH_TOKEN.execute_url, headers=_headers, data=json.dumps(_payloads))
            response_json = response.json()
            logger.info(f"response: {response_json}")
            paymentDetails = PaymentDetails(**response_json)
            return paymentDetails
        else:
            logger.warning(f"is_token_expired: {self.__is_token_valid()}")
            pass

        '''
	 * This method is used for verifying order by order id which could be get by payment response object
	 * @param orderId
	 * @return order object if order verified successfully
    '''

    def _verify_payment(self, order_id):
        try:
            if self.__AUTH_TOKEN == None:
                self.authToken = self._authenticate()

            elif self.__is_token_valid() == False:
                self.authToken = self._authenticate()

            _headers = {'content-type': 'application/json',
                        'Authorization': f'{self.__AUTH_TOKEN.token_type} {self.__AUTH_TOKEN.token}'}

            _payloads = {'order_id': order_id}

            if self.__is_token_valid:
                logger.info(
                    f'url: {self.__API_URL + self.__VERIFICATION_END_POINT}, header:{_headers}, payload: {_payloads}')
                response = requests.post(
                    self.__API_URL + self.__VERIFICATION_END_POINT, headers=_headers, data=json.dumps(_payloads))
                response_json = response.json()
                logger.info(f"response: {response_json}")
                verifiedOrderDetails = VerifiedPaymentDetails(
                    **response_json[0])
                return verifiedOrderDetails

            else:
                logger.warning(f"is_token_expired: {self.__is_token_valid()}")
                pass
        except Exception as e:
            logger.exception(e)
            pass

    def _check_payment_status(self, order_id):
        '''
        * This method is used for checking successfully paid paymnet status by order_id which could be get after verifying order
        * 
        * @param order_id
        * @return VerifiedPaymentDetails if payment verified successfully
        '''

        try:
            if self.__AUTH_TOKEN == None:
                self.__AUTH_TOKEN = self._authenticate()

            elif self.__is_token_valid() == False:
                self.__AUTH_TOKEN = self._authenticate()

            _headers = {'content-type': 'application/json',
                        'Authorization': f'{self.__AUTH_TOKEN.token_type} {self.__AUTH_TOKEN.token}'}

            _payloads = {'order_id': order_id}

            if self.__is_token_valid:
                logger.info(
                    f'url: {self.__API_URL + self.__PAYMENT_STATUS_END_POINT}, header:{_headers}, payload: {_payloads}')
                response = requests.post(
                    self.__API_URL + self.__PAYMENT_STATUS_END_POINT, headers=_headers, data=json.dumps(_payloads))
                response_json = response.json()
                logger.info(f"response: {response_json}")
                verifiedOrderDetails = VerifiedPaymentDetails(
                    **response_json[0])
                return verifiedOrderDetails

            else:
                logger.warning(f"is_token_expired: {self.__is_token_valid()}")
                pass
        except Exception as e:
            logger.exception(e)
            pass
