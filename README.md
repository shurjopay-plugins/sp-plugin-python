![alt text](https://shurjopay.com.bd/dev/images/shurjoPay.png)
# shurjoPay python package (plugin)
[![Test Status](https://github.com/rust-random/rand/workflows/Tests/badge.svg?event=push)]()
[![Python](https://img.shields.io/pypi/pyversions/shurjopay-V2)](https://badge.fury.io/py/tensorflow)
[![PyPI version](https://badge.fury.io/py/shurjopay-V2.svg)](https://badge.fury.io/py/shurjopay-V2)


Official shurjoPay python package (plugin) for merchants or service providers to connect with shurjoPay Payment Gateway v2.1 developed and maintained by shurjoMukhi Limited.

This plugin package can be used with any python application or framework (e.g. django, flask, FastAPI etc.).

This plugin package makes it easy for you to integrate with shurjoPay v2.1 with just two method calls:

- make_payment()
- verify_payment()

## Audience

This document is intended for the developers and technical personnel of merchants and service providers who want to integrate the shurjoPay online payment gateway using python.

# Usage 

Use `pip` to install this plugin inside your project environment

```
pip install shurjopay-plugin
```
Or `clone` the repository and install the package

```
git clone https://github.com/shurjopay-plugins/sp-plugin-python
python setup.py install
```


## Initialize the plugin with shurjoPay configuration

Here is a sample .env configuration

```
SP_USERNAME=sp_sandbox
SP_PASSWORD=pyyk97hu&6u6
SP_ENDPOINT=https://sandbox.shurjopayment.com/api/
SP_CALLBACK=https://www.sandbox.shurjopayment.com/response
SP_LOGDIR=var/log/shurjopay/shurjopay.log
```
After that, you can start using our package the way you want based on your application. Here we are providing a basic example code snip for you.

Example

```
import environ
import shurjopay_plygin
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')
BASE_DIR = Path(__file__).resolve().parent.parent
sp_config = ShurjoPayConfigModel(
        SP_USERNAME = env('SP_USERNAME'),
        SP_PASSWORD = env('SP_PASSWORD'),
        SHURJOPAY_API = env('SP_ENDPOINT'),
        SP_CALLBACK = env('SP_CALLBACK'),
        SP_LOG_DIR = BASE_DIR / 'logs' / 'shurjopay.log'
        )
shurjopay = ShurjopayPlugin(sp_config)
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
        payment_details = shurjopay.make_payment(payment_request)
```


That's all! Now you are ready to use our shurjoPay python package to make your payment system easy and smooth.

## Checkout our [Django Example](https://github.com/shurjopay-plugins/sp-plugin-usage-examples/tree/dev/django-app-python-plugin) application



### [Plugin Development Guideline](DEVELOPER_GUIDE.md)

### [shurjopay Plugins](https://github.com/shurjopay-plugins)

## [Contact US](https://shurjopay.com.bd/#contacts)

## License

[MIT](LICENSE)
