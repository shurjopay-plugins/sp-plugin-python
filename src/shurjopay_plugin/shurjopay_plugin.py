'''
 Shurjopay Python Plugin for shurjoPay Gateway Services.
 Author Md Mahabubul Hasan
 Since 2022-10-10
'''
import requests
import datetime
import json
from .models import (
    PaymentDetailsModel,
    ShurjoPayTokenModel,
    VerifiedPaymentDetailsModel
)
from .utils import (
    get_client_ip,
    Endpoints,
    ShurjopayStatus,
    ShurjopayException,
    ShurjopayAuthException
)
from .logger_config import ShurjopayLoggerConfig


class ShurjopayPlugin(object):
    """
        shurjoPay Online payment gateway has several API's
        which need to be integrated by merchants for
        accessing different services. The available services are:
        - Authenticating
        - Making payment
        - Verifying payment
        - Checking payment status
        For more details view the shurjoPay version-2.1 integration documentation :
        https://docs.google.com/document/d/19J4HE0j873nBJqcN-uRBYYAa_qBA3p1XSY-jy2fwvEE/edit .
    """
    # shurjopay Token attributes
    # token(str),
    # token_type,
    # expires_in,
    # sp_code,
    # message
    AUTH_TOKEN = None

    # Status Message
    AUTHENTICATION_SUCCESS = 'Merchant Authentication Successful!'
    AUTHENTICATION_FAILED = 'Merchant Authentication Failed!'
    AUTHENTICATION_SUCCESS = 'Merchant Authentication Successful!'
    AUTHENTICATION_FAILED = 'Merchant Authentication Failed!'
    AUTHENTICATION_TOKEN_EXPIRED = 'Shurjopay Token Expired!'
    WRONG_CREDENTIALS = 'Please Check Your Credentials!'
    PAYMENT_REQUEST_SUCCESS = 'Shurjopay Payment Request Successful!'
    PAYMENT_REQUEST_FAILED = 'Shurjopay Payment Request Failed!'
    PAYMENT_VERIFICATION_FAILED = 'Shurjopay Payment Verification Failed!'
    PAYMENT_CHECK_FAILED = 'Shurjopay Payment Checking Failed!'

    def __init__(self, sp_config) -> None:
        # Initialize the configuration keys for plugin configuration
        self.SP_USERNAME = sp_config.SP_USERNAME
        self.SP_PASSWORD = sp_config.SP_PASSWORD
        self.SP_ENDPOINT = requests.compat.urljoin(
            sp_config.SP_ENDPOINT, Endpoints.API.value)
        self.SP_RETURN = sp_config.SP_RETURN
        self.SP_CANCEL = sp_config.SP_CANCEL
        self.SP_PREFIX = sp_config.SP_PREFIX

        if sp_config.SP_LOGDIR is None or sp_config.SP_LOGDIR == '':
            self.logger = ShurjopayLoggerConfig().get_logger()
            return
        self.logger = ShurjopayLoggerConfig().get_file_logger(sp_config.SP_LOGDIR)

    def authenticate(self):
        """ Authenticate with shurjoPay Payment Gateway using Merchant credectials.

        Returns
        -------
        AUTH_TOKEN (ShurjoPayTokenModel): token details from shurjopay
            - token(str), 
            - token_type(str),
            - expires_in(int),(in seconds)
            - sp_code(int),
            - message(str)

        Raises
        -----
        ShurjopayAuthException: If authentication fails due to 
        invalid credentials or any other reason. 
        """
        # Create token endpoint url
        url = requests.compat.urljoin(self.SP_ENDPOINT, Endpoints.TOKEN.value)
        self.logger.info(self.SP_ENDPOINT)
        self.logger.info(url)
        payloads = {
            "username": self.SP_USERNAME,
            "password": self.SP_PASSWORD,
        }
        try:
            response = requests.post(url, data=payloads)
            token_details = response.json()
            # Check if authentication is successful
            if (int)(token_details['sp_code']) == ShurjopayStatus().AUTH_SUCCESS.code:
                self.logger.info(
                    f'sp_code:{token_details["sp_code"]}, sp_message:{ShurjopayStatus().AUTH_SUCCESS.message}')
                # set AUTH_TOKEN from response
                self.AUTH_TOKEN = ShurjoPayTokenModel(**token_details)
                return self.AUTH_TOKEN
            self.logger.error(
                f'sp_code:{token_details["sp_code"]}, sp_message:{token_details["message"]}')
            raise ShurjopayException(
                token_details['sp_code'], token_details['message'])
        except ShurjopayAuthException as ex:
            # Log authentication expception error
            self.logger.error(f'{self.WRONG_CREDENTIALS}, {ex}')
            # Raise exception if authentication fails
            raise ShurjopayAuthException(self.WRONG_CREDENTIALS, ex)

    def is_token_valid(self):
        """Checks if token is valid or not by comparing
        token expiry time with current time

        Returns
        -------
        True: if token is valid 
        None: if token is invalid
        """
        return True if (datetime.datetime.strptime(
                       self.AUTH_TOKEN.token_create_time, "%Y-%m-%d %I:%M:%S%p") +
            datetime.timedelta(seconds=self.AUTH_TOKEN.expires_in)) > datetime.datetime.now() else False

    def make_payment(self, payment_req):
        """Make payment request to shurjoPay Gateway 
        using a payment request object containing payment details.

        Args
        ----
        payment_req (PaymentRequestModel): PaymentRequestModel object containing payment details.

        Returns
        -------
        payment_details (PaymentDetailsModel): PaymentDetailsModel object containing redirect URL 
        to reach payment page, order id to verify order in shurjoPay.
        None: if response dosenot contains callback url.

        Raises
        ------
        ShurjopayAuthException if payment fails due to token expired or invalid token.
        ShurjopayException if payment fails due to any other reason.
        """
        try:
            # Check if token is valid or expired
            if self.AUTH_TOKEN is None or self.is_token_valid() is False:
                # Authenticate with shurjoPay
                self.AUTH_TOKEN = self.authenticate()
        except ShurjopayAuthException as ex:
            self.logger.error(f'{self.AUTHENTICATION_FAILED}: {ex}')
            raise ShurjopayAuthException(
                self.AUTHENTICATION_FAILED, self.AUTHENTICATION_TOKEN_EXPIRED)

         # Create make payment endpoint url
        url = requests.compat.urljoin(
            self.SP_ENDPOINT, Endpoints.SECRET_PAY.value)
        headers = {
            'content-type': 'application/json',
            'Authorization': f'{self.AUTH_TOKEN.token_type} {self.AUTH_TOKEN.token}'
        }
        # Map data from authentication token to payment request object
        payloads = self._map_payment_request(payment_req)
        if self.is_token_valid():
            try:
                response = requests.post(
                    url, headers=headers, data=json.dumps(payloads))
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
            self.logger.warning(
                f'{self.AUTHENTICATION_FAILED}: {self.AUTHENTICATION_TOKEN_EXPIRED}')
            raise ShurjopayAuthException(
                self.AUTHENTICATION_FAILED, self.AUTHENTICATION_TOKEN_EXPIRED)

    def verify_payment(self, order_id):
        """ Complete the payment process ushig the order id in the the IPN.
        Args
        -----
        order_id (str): Order id of the payment.

        Returns
        -------
        VerifiedPaymentModel: VerifiedPaymentModel object containing payment details.

        Raises
        -------
        ShurjopayAuthException if payment fails due to token expired or invalid token.
        ShurjopayException if payment fails due to any other reason.
        """
        try:
            # Check if token is valid or expired
            if self.AUTH_TOKEN is None or self.is_token_valid() is False:
                # Authenticate with shurjoPay
                self.AUTH_TOKEN = self.authenticate()
        except ShurjopayAuthException as ex:
            self.logger.error(self.AUTHENTICATION_FAILED, ex)
            raise
        # Create verify payment endpoint url
        url = requests.compat.urljoin(
            self.SP_ENDPOINT, Endpoints.VERIFIFICATION.value)
        headers = {'content-type': 'application/json',
                   'Authorization': f'{self.AUTH_TOKEN.token_type} {self.AUTH_TOKEN.token}'}
        payloads = {'order_id': order_id}
        if self.is_token_valid():
            try:
                response = requests.post(
                    url, headers=headers, data=json.dumps(payloads))
                response = response.json()
                response = response[0]
                if (response['sp_code'] == ShurjopayStatus.INVALID_ORDER_ID.code):
                    self.logger.info(
                        f'sp_code:{response["sp_code"]}, sp_message:{response["message"]}')
                    return None
                elif (response['sp_code'] != ShurjopayStatus.TRANSACTION_SUCCESS.code):
                    self.logger.info(
                        f'sp_code:{response["sp_code"]}, sp_message:{response["sp_message"]}')
                    # Raise exception if payment verification fails
                    raise ShurjopayException(
                        self.PAYMENT_VERIFICATION_FAILED, response['sp_message'])
                self.logger.info(
                    f'sp_code:{response["sp_code"]}, sp_message:{response["sp_message"]}')
                # Return  verified payment detais object
                return VerifiedPaymentDetailsModel(**response)
            except ShurjopayException as ex:
                self.logger.error(f'{self.PAYMENT_VERIFICATION_FAILED}: {ex}')
                raise ShurjopayException(self.PAYMENT_VERIFICATION_FAILED, ex)
        else:
            self.logger.error(
                f'{self.AUTHENTICATION_FAILED}: {self.AUTHENTICATION_TOKEN_EXPIRED}')
            raise ShurjopayAuthException(
                self.AUTHENTICATION_FAILED, self.AUTHENTICATION_TOKEN_EXPIRED)

    def _map_payment_request(self, payment_req):
        """ This method is used to map additional parameters to payment request details.
        Args
        ----
        payment_req (PaymentRequestModel): Payment request object

        Returns
        -------
        payment_req (dict) : a dictionary containing complete payment request details.
        """
        return {
            'token': self.AUTH_TOKEN.token,
            'return_url': self.SP_RETURN,
            'cancel_url': self.SP_CANCEL,
            'store_id': self.AUTH_TOKEN.store_id,
            'prefix': self.SP_PREFIX,
            'amount': payment_req.amount,
            'order_id':  payment_req.order_id,
            'currency': payment_req.currency,
            'customer_name':  payment_req.customer_name,
            'customer_address': payment_req.customer_address,
            'customer_phone': payment_req.customer_phone,
            'customer_city':  payment_req.customer_city,
            'customer_post_code':  payment_req.customer_post_code,
            'client_ip': get_client_ip(),
        }
