'''
 * Plug-in service to provide shurjoPay get way services.
 * @author Mahabubul Hasan, Mashruk Zaman
 * @since 2022-10-10
'''
import os
import environ
import requests
import datetime
import logging
import json
from model.models import *


'''
    * Setup .env from conf/shurjopay file with your credentials.
    * Change envdir path sandbox to shurjopay if shurjopay in not selected.
'''
env = environ.Env()
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
envdir = os.path.join(basedir, 'conf\\sandbox\\')
env.read_env(os.path.join(envdir, '.env'))

# create a logger
logger = logging.getLogger(__name__)
# set log level
logger.setLevel(logging.DEBUG)
# define file handler and set formatter
#log_fileName = 'LOG/{:%Y-%m-%d}.log'.format(datetime.datetime.now())
log_fileName = env('LOG_LOCATION') + \
    '{:%Y-%m-%d}.log'.format(datetime.datetime.now())

# create log file
os.makedirs(os.path.dirname(log_fileName), exist_ok=True)
file_handler = logging.FileHandler(log_fileName, mode="a", encoding=None, )
formatter = logging.Formatter(
    '%(asctime)s : %(levelname)s : %(name)s : %(funcName)s  %(message)s')
file_handler.setFormatter(formatter)
# add file handler to logger
logger.addHandler(file_handler)


class ShurjoPayPlugin(object):
    __SP_USERNAME = env('SP_USERNAME')
    __SP_PASSWORD = env('SP_PASSWORD')
    __API_URL = env('API_URL')
    __RETURN_URL = env('CALLBACK_URL')
    __CANCEL_URL = env('CALLBACK_URL')
    __TOKEN_END_POINT = env('TOKEN_END_POINT')
    __VERIFICATION_END_POINT = env('VERIFICATION_END_POINT')
    __PAYMENT_STATUS_END_POINT = env('PAYMENT_STATUS_END_POINT')
    __AUTH_TOKEN = None

    def __init__(self) -> None:
        pass

    '''
	 * Return authorization token for shurjoPay payment gateway system. 
	 * @return authentication details with valid token
	 * @throws IllegalAccessException 
    '''

    def _authenticate(self):
        try:
            payload = {
                "username": self.__SP_USERNAME,
                "password": self.__SP_PASSWORD
            }
            logger.info(
                f"url: {self.__API_URL + self.__TOKEN_END_POINT}, payload:{payload}")
            response = requests.post(
                self.__API_URL + self.__TOKEN_END_POINT, data=payload)
            token_details = response.json()

            if int(token_details["sp_code"]) == 200:
                # set token information
                logger.info(f"response: {token_details}")
                authToken = ShurjoPayToken(
                    token_details['token'],
                    token_details['store_id'],
                    token_details['execute_url'],
                    token_details['token_type'],
                    token_details['sp_code'],
                    token_details['message'],
                    datetime.datetime.strptime(
                        token_details["token_create_time"], "%Y-%m-%d %I:%M:%S%p"),
                    token_details['expires_in'])
                self.__AUTH_TOKEN = authToken
            else:
                raise Exception(token_details)
        except Exception as e:
            logger.exception(e)
            pass
    # checks if token is valid or not

    def __is_token_valid(self):
        return True if (self.__AUTH_TOKEN.token_create_time + datetime.timedelta(milliseconds=self.__AUTH_TOKEN.expires_in)) > datetime.datetime.now() else False

    '''
     * This method is used for making payment. 
	 * @param Payment request object. See the shurjoPay version-2 integration documentation(beta).docx for details.
	 * @return Payment response object contains redirect URL to reach payment page, order id to verify order in shurjoPay.
	'''

    def _make_payment(self, paymentReq):
        try:
            if self.__AUTH_TOKEN == None:
                self.authToken = self._authenticate()

            elif self.__is_token_valid() == False:
                self.authToken = self._authenticate()

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
        except Exception as e:
            logger.exception(e)
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
