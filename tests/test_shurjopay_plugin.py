import json
import unittest
import os
import sys
import environ


root_dir = os.getcwd()
sys.path.insert(0, os.path.join(root_dir, "src/shurjopay_plugin"))

from shurjopay_plugin.shurjopay_plugin import ShurjopayPlugin
from shurjopay_plugin.shurjopay_plugin import *

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
            SP_CALLBACK=env('SP_CALLBACK'),
            SP_LOGDIR=env('SP_LOGDIR')
        )
        self._plugin = ShurjopayPlugin(sp_config)
        self._payment_request = PaymentRequestModel(**payment_request_json)

    def test_make_payment(self):
        # unit testing for make payment
        self._payment_request_details = self._plugin.make_payment(
            self._payment_request)

        self.assertEqual(
            10, self._payment_request_details.amount, 'amount is not equal')

        self.assertEqual(
            'BDT', self._payment_request_details.currency, 'Currency  is not equal')

        self.assertEqual(
            'ATM Fahim', self._payment_request_details.customer_name, 'Customer Name is not equal')

        self.assertEqual(
            '01717302935', self._payment_request_details.customer_phone, 'Customer Phone is not equal')

        self.assertEqual(
            'mohakhali', self._payment_request_details.customer_address, "Customer Address is not equal")

        self.assertEqual(
            'Dhaka', self._payment_request_details.customer_city, 'Customer City is not equal')


    def test_verify_payment(self):
        #unit testing for verify payment
        verified_payment_details = self._plugin.verify_payment(
            '0000')

        if(verified_payment_details == None):
            print(ShurjopayStatus.INVALID_ORDER_ID.message)
            return

        self.assertEqual(1, verified_payment_details.id, "ID is not equal")
        self.assertEqual(
            "spay612b73a935ab1", verified_payment_details.order_id, "Order ID is not equal")
        self.assertEqual(
            "BDT", verified_payment_details.currency, "Currency is not equal")
        self.assertEqual(7, verified_payment_details.amount,
                         "Amount is not equal")
        self.assertEqual(
            "visa", verified_payment_details.card_holder_name, "Card Holder Name is not equal")
        self.assertEqual(
            "4444xxxxxxxx4444", verified_payment_details.card_number, "Card Number is not equal")
        self.assertEqual(
            7, verified_payment_details.payable_amount, "Payable Amount is not equal")
        self.assertEqual(0, verified_payment_details.disc_percent,
                         "Discount Percent is not equal")
        self.assertEqual(0, verified_payment_details.usd_amt,
                         "USD Amount is not equal")
        self.assertEqual(0, verified_payment_details.usd_rate,
                         "USD Rate is not equal")

        self.assertEqual(
            'spay612b73a935ab1', verified_payment_details.invoice_no, "Invoice No is not equal")
        self.assertEqual(
            'Failed', verified_payment_details.bank_status, "Bank Status is not equal")
        self.assertEqual('spay612b73a12c88e', verified_payment_details.customer_order_id,
                         "Customer Order ID is not equal")
        self.assertEqual('Bank Response Failed',
                         verified_payment_details.sp_message, "SP Message is not equal")
        self.assertEqual(
            1005, verified_payment_details.sp_code, "SP Code is not equal")

        self.assertEqual("Abu tayeb md fahim",
                         verified_payment_details.name, "Name is not equal")
        self.assertEqual('Gulshan 1,Dhaka 1212',
                         verified_payment_details.address, "Address is not equal")
        self.assertEqual(
            'Dhaka', verified_payment_details.city, "City is not equal")
        self.assertEqual(
            'Ebl Visa', verified_payment_details.method, "Method is not equal")
        self.assertEqual('2021-08-29 17:47:06',
                         verified_payment_details.date_time, "Date Time is not equal")

    def test_get_payment_details(self):
        #unit testing for check payment status
        verified_payment_status = self._plugin.get_payment_details(
            '00sdfsfsdfsdf')
        if verified_payment_status == None:
            print(ShurjopayStatus.INVALID_ORDER_ID.message)
            return
        self.assertEqual(1, verified_payment_status.id, "ID is not equal")
        self.assertEqual(
            "spay612b73a935ab1", verified_payment_status.order_id, "Order ID is not equal")
        self.assertEqual(
            "BDT", verified_payment_status.currency, "Currency is not equal")
        self.assertEqual(7, verified_payment_status.amount,
                         "Amount is not equal")
        self.assertEqual(
            "visa", verified_payment_status.card_holder_name, "Card Holder Name is not equal")
        self.assertEqual(
            "4444xxxxxxxx4444", verified_payment_status.card_number, "Card Number is not equal")
        self.assertEqual(
            7, verified_payment_status.payable_amount, "Payable Amount is not equal")
        self.assertEqual(0, verified_payment_status.disc_percent,
                         "Discount Percent is not equal")
        self.assertEqual(0, verified_payment_status.usd_amt,
                         "USD Amount is not equal")
        self.assertEqual(0, verified_payment_status.usd_rate,
                         "USD Rate is not equal")

        self.assertEqual(
            'spay612b73a935ab1', verified_payment_status.invoice_no, "Invoice No is not equal")
        self.assertEqual(
            'Failed', verified_payment_status.bank_status, "Bank Status is not equal")
        self.assertEqual('spay612b73a12c88e', verified_payment_status.customer_order_id,
                         "Customer Order ID is not equal")
        self.assertEqual('Bank Response Failed',
                         verified_payment_status.sp_message, "SP Message is not equal")
        self.assertEqual(
            1005, verified_payment_status.sp_code, "SP Code is not equal")

        self.assertEqual("Abu tayeb md fahim",
                         verified_payment_status.name, "Name is not equal")
        self.assertEqual('Gulshan 1,Dhaka 1212',
                         verified_payment_status.address, "Address is not equal")
        self.assertEqual(
            'Dhaka', verified_payment_status.city, "City is not equal")
        self.assertEqual(
            'Ebl Visa', verified_payment_status.method, "Method is not equal")
        self.assertEqual('2021-08-29 17:47:06',
                         verified_payment_status.date_time, "Date Time is not equal")


if __name__ == '__main__':
    unittest.main()
