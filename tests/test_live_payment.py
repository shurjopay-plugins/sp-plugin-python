import json
import unittest
import os
import sys
import environ


root_dir = os.getcwd()
sys.path.insert(0, os.path.join(root_dir, "src/shurjopay_plugin"))

from shurjopay_plugin import ShurjopayPlugin
from shurjopay_plugin import *

#load payemnt request data from json file
with open(os.path.join(root_dir,"tests/sample_message/PaymentRequest.json"), "r") as read_file:
    payment_request_json = json.load(read_file)

#loading environment variables
env = environ.Env()
env.read_env(os.path.join(root_dir, '.env'))
#Shurjopay config for Instatiating ShurjopayPlugin
sp_config = ShurjoPayConfigModel(
    SP_USERNAME=env('SP_USERNAME'),
    SP_PASSWORD=env('SP_PASSWORD'),
    SP_ENDPOINT=env('SP_ENDPOINT'),
    SP_CALLBACK=env('SP_CALLBACK'),
    SP_PREFIX=env('SP_PREFIX'),
    SP_LOGDIR=env('SP_LOGDIR')
)
plugin = ShurjopayPlugin(sp_config)
payment_request = PaymentRequestModel(**payment_request_json)
payment_details=plugin.make_payment(payment_request)
verifyPayment = plugin.verify_payment("APSJK63b717accbc04")
checkPayment = plugin.check_payment("APSJK63b717accbc04")