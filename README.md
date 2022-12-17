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
SP_LOGDIR=log/shurjopay/shurjopay.log
```
Example



That's all! Now you are ready to use our shurjoPay python package to make your payment system easy and smooth.

See our [Django Example](https://github.com/shurjopay-plugins/sp-plugin-usage-examples/tree/dev/django-app-python-plugin) application



### [Plugin Development Guideline](DEVELOPER_GUIDE.md)

### [shurjopay Plugins ](https://github.com/shurjopay-plugins)

## Contact  [shurjopay](https://shurjopay.com.bd/#contacts)

## License

[MIT](LICENSE)
