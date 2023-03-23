import json
import unittest
import os
import sys
import environ


root_dir = os.getcwd()

from shurjopay_plugin import *
#load payemnt request data from json file
with open(os.path.join(root_dir,"tests/sample_message/PaymentRequest.json"), "r") as read_file:
    payment_request_json = json.load(read_file)

#loading environment variables
env = environ.Env()
env.read_env(os.path.join(root_dir, '.env'))
class TestShurjoPayPlugin(unittest.TestCase):
    '''
    Unit tests for ShurjopayPlugin : Make Payment, Verify Payment, Check Payment Status
    '''

    def setUp(self):
        #Shurjopay config for Instatiating ShurjopayPlugin
        sp_config = ShurjoPayConfigModel(
        SP_USERNAME=env('SP_USERNAME'),
        SP_PASSWORD=env('SP_PASSWORD'),
        SP_ENDPOINT=env('SP_ENDPOINT'),
        SP_RETURN=env('SP_RETURN'),
        SP_CANCEL=env('SP_CANCEL'),
        SP_PREFIX=env('SP_PREFIX'),
        SP_LOGDIR=env('SP_LOGDIR')
    )
        self._plugin = ShurjopayPlugin(sp_config)
        self._payment_request = PaymentRequestModel(**payment_request_json)

    def test_make_payment(self):
        # unit testing for make payment
        self._payment_request_details = self._plugin.make_payment(
            self._payment_request)

        print(json.dumps(self._payment_request_details.__dict__,indent=4))

        self.assertEqual(
            10, self._payment_request_details.amount, 'amount is not equal')

        self.assertEqual(
            'BDT', self._payment_request_details.currency, 'Currency  is not equal')

        self.assertEqual(
            'MD. ABDUL KARIM', self._payment_request_details.customer_name, 'Customer Name is not equal')

        self.assertEqual(
            '01111111111', self._payment_request_details.customer_phone, 'Customer Phone is not equal')

        self.assertEqual(
            'mohakhali', self._payment_request_details.customer_address, "Customer Address is not equal")

        self.assertEqual(
            'Dhaka', self._payment_request_details.customer_city, 'Customer City is not equal')


    def test_verify_payment(self):
        #unit testing for verify payment
        verified_payment_details = self._plugin.verify_payment(
            'sp6416d45992986')

        if(verified_payment_details == None):
            print(ShurjopayStatus.INVALID_ORDER_ID.message)
            return

        self.assertEqual(1759527, verified_payment_details.id, "ID is not equal")
        self.assertEqual(
            "sp6416d45992986", verified_payment_details.order_id, "Order ID is not equal")
       

if __name__ == '__main__':
    unittest.main()
