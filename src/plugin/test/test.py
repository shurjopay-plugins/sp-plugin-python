from shurjopay_plugin import ShurjoPayPlugin
from models import *
import json
import unittest

with open("test/PaymentRequest.json", "r") as read_file:
    payment_request_json = json.load(read_file)


with open("test/VerifiedPaymentDetails.json", "r") as read_file:
    verified_payment_json = json.load(read_file)


class TestShurjoPayPlugin(unittest.TestCase):
    '''
    Unit tests for ShurjopayPlugin : Make Payment, Verify Payment, Check Payment Status
    '''

    def setUp(self):
        self.plugin = ShurjoPayPlugin()
        self._make_payment = PaymentRequestModel(**payment_request_json)
        self._verified_payment = VerifiedPaymentDetailsModel(
            **verified_payment_json)

    def test_make_payment(self):
        payment_details = self.plugin.make_payment(self._make_payment)
        print(payment_details.checkout_url)
        self.assertIsInstance(payment_details, PaymentDetailsModel,
                              "payment_details is not an instance of PaymentDetails")

        self.assertEqual(payment_details.amount,
                         self._make_payment.amount, "amount is not equal")
        self.assertEqual(self._make_payment.currency,
                         'BDT', " currency  is not equal")
        self.assertEqual(payment_details.customer_name,
                         self._make_payment.customer_name, "customer_name is not equal")
        self.assertEqual(payment_details.customer_phone,
                         self._make_payment.customer_phone, "customer_phone is not equal")
        self.assertEqual(payment_details.customer_address,
                         self._make_payment.customer_address, "customer_address is not equal")
        self.assertEqual(payment_details.customer_city,
                         self._make_payment.customer_city, "customer_city is not equal")
        self.assertEqual(payment_details.client_ip,
                         self._make_payment.client_ip, "client_ip is not equal")
        self.assertEqual(payment_details.customer_order_id,
                         self._make_payment.order_id, "customer_order_id is not equal")

    def test_verify_payment(self):
        verified_payment_details = self.plugin.verify_payment(
            self._verified_payment.order_id)

        self.assertIsInstance(verified_payment_details, VerifiedPaymentDetailsModel,
                              "verified_order_details is not an instance of VerifiedOrderDetails")
        self.assertEqual(verified_payment_details.id,
                         self._verified_payment.id, 'id is not equal')
        self.assertEqual(verified_payment_details.order_id,
                         self._verified_payment.order_id, 'order_id is not equal')
        self.assertEqual(verified_payment_details.amount,
                         self._verified_payment.amount, 'amount is not equal')
        self.assertEqual(verified_payment_details.discsount_amount,
                         self._verified_payment.discsount_amount, 'discount amount is not equal')
        self.assertEqual(verified_payment_details.payable_amount,
                         self._verified_payment.payable_amount, 'payable_amount amount is not equal')
        self.assertEqual(verified_payment_details.disc_percent,
                         self._verified_payment.disc_percent, 'disc_percent is not equal')
        self.assertEqual(verified_payment_details.usd_amt,
                         self._verified_payment.usd_amt, 'usd_amt is not equal')
        self.assertEqual(verified_payment_details.usd_rate,
                         self._verified_payment.usd_rate, 'usd_rate is not equal')
        self.assertEqual(verified_payment_details.card_holder_name,
                         self._verified_payment.card_holder_name, 'card_holder_name is not equal')
        self.assertEqual(verified_payment_details.card_number,
                         self._verified_payment.card_number, 'card number is not equal')
        self.assertEqual(verified_payment_details.phone_no,
                         self._verified_payment.phone_no, 'phone_no is not equal')
        self.assertEqual(verified_payment_details.bank_trx_id,
                         self._verified_payment.bank_trx_id, 'bank_trx_id is not equal')
        self.assertEqual(verified_payment_details.invoice_no,
                         self._verified_payment.invoice_no, 'invoice_no is not equal')
        self.assertEqual(verified_payment_details.bank_status,
                         self._verified_payment.bank_status, 'bank_status is not equal')
        self.assertEqual(verified_payment_details.customer_order_id,
                         self._verified_payment.customer_order_id, 'customer_order_id is not equal')
        self.assertEqual(verified_payment_details.sp_message,
                         self._verified_payment.sp_message, 'sp_massage is not equal')
        self.assertEqual(verified_payment_details.sp_code,
                         self._verified_payment.sp_code, 'sp_code is not equal')
        self.assertEqual(verified_payment_details.name,
                         self._verified_payment.name, 'name is not equal')
        self.assertEqual(verified_payment_details.email,
                         self._verified_payment.email, 'email is not equal')
        self.assertEqual(verified_payment_details.address,
                         self._verified_payment.address, 'address is not equal')
        self.assertEqual(verified_payment_details.city,
                         self._verified_payment.city, 'city is not equal')
        self.assertEqual(verified_payment_details.value1,
                         self._verified_payment.value1, 'value1 is not equal')
        self.assertEqual(verified_payment_details.value2,
                         self._verified_payment.value2, 'value2 is not equal')
        self.assertEqual(verified_payment_details.value3,
                         self._verified_payment.value3, 'value3 is not equal')
        self.assertEqual(verified_payment_details.value4,
                         self._verified_payment.value4, 'value4 is not equal')
        self.assertEqual(verified_payment_details.transaction_status,
                         self._verified_payment.transaction_status, 'value5 is not equal')
        self.assertEqual(verified_payment_details.method,
                         self._verified_payment.method, 'value6 is not equal')
        self.assertEqual(verified_payment_details.date_time,
                         self._verified_payment.date_time, 'date_time is not equal')

    def test_get_payment_status(self):
        verified_payment_status = self.plugin.check_payment_status(
            self._verified_payment.order_id)
        self.assertIsInstance(verified_payment_status, VerifiedPaymentDetailsModel,
                              "payment_status is not an instance of VerifiedPaymentDetails")
        self.assertEqual(verified_payment_status.id,
                         self._verified_payment.id, 'id is not equal')
        self.assertEqual(verified_payment_status.order_id,
                         self._verified_payment.order_id, 'order_id is not equal')
        self.assertEqual(verified_payment_status.amount,
                         self._verified_payment.amount, 'amount is not equal')
        self.assertEqual(verified_payment_status.discsount_amount,
                         self._verified_payment.discsount_amount, 'discount amount is not equal')
        self.assertEqual(verified_payment_status.payable_amount,
                         self._verified_payment.payable_amount, 'payable_amount amount is not equal')
        self.assertEqual(verified_payment_status.disc_percent,
                         self._verified_payment.disc_percent, 'disc_percent is not equal')
        self.assertEqual(verified_payment_status.usd_amt,
                         self._verified_payment.usd_amt, 'usd_amt is not equal')
        self.assertEqual(verified_payment_status.usd_rate,
                         self._verified_payment.usd_rate, 'usd_rate is not equal')
        self.assertEqual(verified_payment_status.card_holder_name,
                         self._verified_payment.card_holder_name, 'card_holder_name is not equal')
        self.assertEqual(verified_payment_status.card_number,
                         self._verified_payment.card_number, 'card number is not equal')
        self.assertEqual(verified_payment_status.phone_no,
                         self._verified_payment.phone_no, 'phone_no is not equal')
        self.assertEqual(verified_payment_status.bank_trx_id,
                         self._verified_payment.bank_trx_id, 'bank_trx_id is not equal')
        self.assertEqual(verified_payment_status.invoice_no,
                         self._verified_payment.invoice_no, 'invoice_no is not equal')
        self.assertEqual(verified_payment_status.bank_status,
                         self._verified_payment.bank_status, 'bank_status is not equal')
        self.assertEqual(verified_payment_status.customer_order_id,
                         self._verified_payment.customer_order_id, 'customer_order_id is not equal')
        self.assertEqual(verified_payment_status.sp_message,
                         self._verified_payment.sp_message, 'sp_massage is not equal')
        self.assertEqual(verified_payment_status.sp_code,
                         self._verified_payment.sp_code, 'sp_code is not equal')
        self.assertEqual(verified_payment_status.name,
                         self._verified_payment.name, 'name is not equal')
        self.assertEqual(verified_payment_status.email,
                         self._verified_payment.email, 'email is not equal')
        self.assertEqual(verified_payment_status.address,
                         self._verified_payment.address, 'address is not equal')
        self.assertEqual(verified_payment_status.city,
                         self._verified_payment.city, 'city is not equal')
        self.assertEqual(verified_payment_status.value1,
                         self._verified_payment.value1, 'value1 is not equal')
        self.assertEqual(verified_payment_status.value2,
                         self._verified_payment.value2, 'value2 is not equal')
        self.assertEqual(verified_payment_status.value3,
                         self._verified_payment.value3, 'value3 is not equal')
        self.assertEqual(verified_payment_status.value4,
                         self._verified_payment.value4, 'value4 is not equal')
        self.assertEqual(verified_payment_status.transaction_status,
                         self._verified_payment.transaction_status, 'value5 is not equal')
        self.assertEqual(verified_payment_status.method,
                         self._verified_payment.method, 'value6 is not equal')
        self.assertEqual(verified_payment_status.date_time,
                         self._verified_payment.date_time, 'date_time is not equal')


if __name__ == '__main__':
    unittest.main()
