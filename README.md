![alt text](https://shurjopay.com.bd/dev/images/shurjoPay.png)

# ShurjoPay Online Payment API Integration

This document has been prepared by Shurjomukhi Limited to enable the online merchants to integrate shurjoPay payment gateway. The information contained in this document is proprietary and confidential to Shurjomukhi Limited, for the product Shurjopay.

## Audience

This document is intended for the technical personnel of merchants and service providers that want to integrate a new online payment gateway using python plugin provided by shurjoPay.

## Integration

ShurjoPay Online payment gateway has several API's which need to be integrated by merchants for accessing different services. The available services are:

- Authenticate users
- Making payment
- Verifying payment order
- Checking verified payment order status

## shurjoPay python plugin for django, flask, botle, cherrypy

**Example Applications**

### [Django](https://github.com/shurjopay-plugins/sp-plugin-usage-examples/tree/dev/django-app-python-plugin)

## Installation

> 📝 **NOTE** Install the package inside your project environment

Use `pip` to install shuroPay python plugin

>

```
pip install shurjopay-v3

```

Or `clone` the repository

```
git clone https://github.com/shurjopay-plugins/sp-plugin-python

```

Then instal the plugin inside your project

```
python setup.py install

```

## Initialize the shurjoPay python plugin with shurjoPay credentials & api-url, marchent's callback url and a log directory

Here is a sample .env configuration

```
SP_USERNAME=sp_sandbox
SP_PASSWORD=pyyk97hu&6u6
SHURJOPAY_API=https://sandbox.shurjopayment.com/api/
SP_CALLBACK=https://www.sandbox.shurjopayment.com/response
SP_LOG_DIR=/log/shurjopay/shurjopay.log
```

## Documentation

### [Developer-Guideline](doc/sp_plugin_developer_guideline.md)

### [Github](https://github.com/shurjopay-plugins)

## Contacts

[Shurjopay](https://shurjopay.com.bd/#contacts)

## License

[MIT](LICENSE)
