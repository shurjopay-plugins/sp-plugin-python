from shurjopay_plugin import ShurjoPayPlugin
from models import *
import json
import unittest
import os
import environ

with open("test/PaymentRequest.json", "r") as read_file:
    payment_request_json = json.load(read_file)


basedir = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

env = environ.Env()
env.read_env(os.path.join(basedir, '.env'))

'''
{
    "prefix": "sp",
    "amount": 10,
    "order_id": "sp315689",
    "currency": "BDT",
    "customer_name": "ATM Fahim",
    "customer_address": "mohakhali",
    "customer_phone": "01717302935",
    "customer_city": "Dhaka",
    "customer_post_code": "1212",
    "client_ip": "102.101.1.1"
}
'''


class TestShurjoPayPlugin(unittest.TestCase):
    '''
    Unit tests for ShurjopayPlugin : Make Payment, Verify Payment, Check Payment Status
    '''

    def setUp(self):
        sp_config = ShurjoPayConfigModel(
            SP_USERNAME=env('SP_USERNAME'),
            SP_PASSWORD=env('SP_PASSWORD'),
            SHURJOPAY_API=env('SHURJOPAY_API'),
            SP_CALLBACK=env('SP_CALLBACK')
        )
        self._plugin = ShurjoPayPlugin(sp_config)
        self._payment_request = PaymentRequestModel(**payment_request_json)

    def test_make_payment(self):
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

        self.assertEqual(
            '102.101.1.1', self._payment_request_details.client_ip, "Client IP is not equal")

    def test_verify_payment(self):

        verified_payment_details = self._plugin.verify_payment(
            'spay612b73a935ab1')

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

    def test_get_payment_status(self):
        verified_payment_status = self._plugin.check_payment_status(
            'spay612b73a935ab1')

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
