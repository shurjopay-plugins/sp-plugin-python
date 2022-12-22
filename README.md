![alt text](https://shurjopay.com.bd/dev/images/shurjoPay.png)
# shurjoPay python package (plugin)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Python](https://img.shields.io/pypi/pyversions/shurjopay-V2)](https://badge.fury.io/py/shurjopay-V2)
[![PyPI version](https://badge.fury.io/py/shurjopay-V2.svg)](https://badge.fury.io/py/shurjopay-V2)
[![Test Status](https://github.com/rust-random/rand/workflows/Tests/badge.svg?event=push)]()
[![PyPi license](https://badgen.net/pypi/license/pip/)](https://pypi.com/project/pip/)



Official shurjoPay python package (plugin) for merchants or service providers to connect with shurjoPay Payment Gateway v2.1 developed and maintained by shurjoMukhi Limited.

This plugin package can be used with any python application or framework (e.g. django, flask, FastAPI etc.).

This plugin package makes it easy for you to integrate with shurjoPay v2.1 with just three method calls:

- make_payment()
- verify_payment()
- check_payment()

Also reduces many of the things that you had to do manually

- Handles http request and errors
- JSON serialization and deserialization
- Authentication during checkout and verification of payments

## Audience

This document is intended for the developers and technical personnel of merchants and service providers who want to integrate the shurjoPay online payment gateway using python.

# Usage 

Use `pip` to install this plugin inside your project environment

```
pip install shurjopay-plugin
```


## Initialize the plugin with shurjoPay configuration
Create a .env file inside your projects root directory. Here is a sample .env configuration
```
SP_USERNAME=sp_sandbox
SP_PASSWORD=pyyk97hu&6u6
SP_ENDPOINT=https://sandbox.shurjopayment.com/api/
SP_CALLBACK=https://www.sandbox.shurjopayment.com/response/
SP_LOGDIR=var/log/shurjopay/shurjopay.log/
```
After that, you can start using our package the way you want based on your application. Here we are providing a basic example code snippet for you.

- Initialize the plugin with shurjoPay configuration
```python
import environ
from shurjopay_plugin import *
env = environ.Env()
environ.Env.read_env('.env')
sp_config = ShurjoPayConfigModel(
        SP_USERNAME = env('SP_USERNAME'),
        SP_PASSWORD = env('SP_PASSWORD'),
        SP_ENDPOINT = env('SP_ENDPOINT'),
        SP_CALLBACK = env('SP_CALLBACK'),
        SP_LOGDIR= env('SP_LOGDIR')
        )
shurjopay_plugin = ShurjopayPlugin(sp_config)
```
- Initiate the Payment with a payment request object
```python
payment_request = PaymentRequestModel(
            prefix='sp-plugin-python',
            amount=1000,
            order_id='001',
            currency='BDT',
            customer_name='Mahabubul Hasan',
            customer_address='Mohakhali',
            customer_phone='01311310975',
            customer_city='Dhaka',
            customer_post_code='1229',
        )
payment_details = shurjopay_plugin.make_payment(payment_request)
```
- Verify payment after each transaction

```python
shurjopay_plugin.verify_payment(order_id)
```
- Check the payment status
```python
shurjopay_plugin.check_payment(order_id)
```
That's all! Now you are ready to use the python plugin to seamlessly integrate with shurjoPay to make your payment system easy and smooth.

### Also, checkout our [Django Example](https://github.com/shurjopay-plugins/sp-plugin-usage-examples/tree/dev/django-app-python-plugin) application


## References

### [Plugin Development Guideline](DEVELOPER_GUIDE.md)

### [shurjopay Plugins](https://github.com/shurjopay-plugins)


## License
This code is under the [MIT open source License](LICENSE)
#### Please [contact](https://shurjopay.com.bd/#contacts) with shurjoPay team for more detail!
<hr>
Copyright ©️2022 Shurjomukhi Limited.
