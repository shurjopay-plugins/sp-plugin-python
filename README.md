# ![alt text](https://shurjopay.com.bd/dev/images/shurjoPay.png) Python package (plugin)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Python](https://img.shields.io/pypi/pyversions/shurjopay-plugin)](https://badge.fury.io/py/shurjopay-plugin)
[![PyPI version](https://badge.fury.io/py/shurjopay-plugin.svg)](https://badge.fury.io/py/shurjopay-plugin)
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

## How to use this shurjoPay Plugin

#### Use `pip` to install this plugin inside your project environment.

```
pip install shurjopay-plugin
```

#### Create a .env file inside your project's root directory. Here is a sample .env configuration.
```
SP_USERNAME=sp_sandbox
SP_PASSWORD=pyyk97hu&6u6
SP_ENDPOINT=https://sandbox.shurjopayment.com/api/
SP_CALLBACK=https://www.sandbox.shurjopayment.com/response/
SP_PREFIX=sp-plugin-python
SP_LOGDIR=/var/log/shurjopay/shurjopay.log (optional)
```
#### After that, you can initiate payment request to shurjoPay using our package the way you want based on your application. Here we are providing a basic example code snippet for you.


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
        SP_PREFIX = env('SP_PREFIX'),
        SP_LOGDIR= env('SP_LOGDIR')
        )
shurjopay_plugin = ShurjopayPlugin(sp_config)
payment_request = PaymentRequestModel(
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

#### Payment verification can be done after each transaction with shurjopay order id.

```python
shurjopay_plugin.verify_payment(order_id)
```

#### That's all! Now you are ready to use the python plugin to seamlessly integrate with shurjoPay to make your payment system easy and smooth.

## References
1. [Django example application](https://github.com/shurjopay-plugins/sp-plugin-usage-examples/tree/dev/django-app-python-plugin) showing usage of the python plugin.
2. [Sample applications and projects](https://github.com/shurjopay-plugins/sp-plugin-usage-examples) in many different languages and frameworks showing shurjopay integration.
3. [shurjoPay Postman site](https://documenter.getpostman.com/view/6335853/U16dS8ig) illustrating the request and response flow using the sandbox system.
4. [shurjopay Plugins](https://github.com/shurjopay-plugins) home page on github

## License
This code is under the [MIT open source License](LICENSE).
#### Please [contact](https://shurjopay.com.bd/#contacts) with shurjoPay team for more detail.
### Copyright ©️2022 [ShurjoMukhi Limited](https://shurjopay.com.bd/)
