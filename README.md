![alt text](https://shurjopay.com.bd/dev/images/shurjoPay.png)

# shurjoPay python package (plugin)
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

## Integration

ShurjoPay Online payment gateway has several API's which need to be integrated by merchants for accessing different services. The available services are:

- Authenticate users
- Making payment
- Verifying payment order
- Checking verified payment order status

## shurjoPay python plugin for django, flask, botle, cherrypy

## Installation

> 📝 **NOTE** Use `pip` to install the package in your python project environment for shuroPay python plugin
>

```
pip install shurjopay-plugin

```

Or `clone` the repository

```
git clone https://github.com/shurjopay-plugins/sp-plugin-python

```

Then install the plugin inside your project

```
python setup.py install

```

## Initialize the plugin with shurjoPay credentials & api-url, marchent's callback url and a log directory

Here is a sample .env configuration

```
SP_USERNAME=sp_sandbox
SP_PASSWORD=pyyk97hu&6u6
SP_ENDPOINT=https://sandbox.shurjopayment.com/api/
SP_CALLBACK=https://www.sandbox.shurjopayment.com/response
SP_LOGDIR=log/shurjopay/shurjopay.log
```

## Documentation

### [shurjoPay plugin developer guide / howto](DEVELOPER_GUIDE.md)

### [Github](https://github.com/shurjopay-plugins)

## Contacts

[Shurjopay](https://shurjopay.com.bd/#contacts)

## License

[MIT](LICENSE)
