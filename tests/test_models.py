from shurjopay_plugin import *
import json
import unittest
import os
import environ
import logging

LOGGER = logging.getLogger(__name__)
ROOT_DIR = os.getcwd()

# load payemnt request data from json file
with open(os.path.join(ROOT_DIR, "tests/sample_message/PaymentRequest.json"), "r") as read_file:
    payment_request_json = json.load(read_file)
with open(os.path.join(ROOT_DIR, "tests/sample_message/TokenDetails.json"), "r") as read_file:
    token_details_json = json.load(read_file)
with open(os.path.join(ROOT_DIR, "tests/sample_message/PaymentDetails.json"), "r") as read_file:
    payment_details_json = json.load(read_file)
with open(os.path.join(ROOT_DIR, "tests/sample_message/VeriifiedPaymentDetails.json"), "r") as read_file:
    verified_payemnt_json = json.load(read_file)


# loading environment variables
env = environ.Env()
env.read_env(os.path.join(ROOT_DIR, '.env'))


class TestShurjopayModels(unittest.TestCase):

    def test_payment_request(self):
        payment_request = PaymentRequestModel(**payment_request_json)
        self.assertEqual(5.0, payment_request.amount, "Amount is not same")
        self.assertIsInstance(payment_request.amount,
                              float, "Amount type is not same")

    def test_token_details(self):
        token_details = ShurjoPayTokenModel(**token_details_json)
        self.assertEqual("2023-05-29 12:46:01pm",
                         token_details.token_create_time, "Token creation is not same")

    def test_payment_details(self):
        payment_details = PaymentDetailsModel(**payment_details_json)
        self.assertEqual(
            "192.168.0.46", payment_details.merchant_server_ip, "IP is not same")

    def test_verified_payment_details(self):
        verified_payment_details = VerifiedPaymentDetailsModel(
            **verified_payemnt_json)
        self.assertEqual(5.0, verified_payment_details.amount,
                         "Amount is not same")
        self.assertIsInstance(verified_payment_details.amount,
                              float, "Amount type is not same")


if __name__ == '__main__':
    unittest.main()
