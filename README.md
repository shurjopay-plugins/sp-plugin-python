![alt text](https://shurjopay.com.bd/dev/images/shurjoPay.png)

# ShurjoPay Online Payment API Integration:

This document has been prepared by Shurjomukhi Limited to enable the online merchants to integrate shurjoPay payment gateway. The information contained in this document is proprietary and confidential to Shurjomukhi Limited, for the product Shurjopay.

## Audience

This document is intended for the technical personnel of merchants and service providers that want to integrate a new online payment gateway using python plugin provided by shurjoPay.

## Integration

ShurjoPay Online payment gateway has several APIs which need to be integrated by merchants for accessing different services. The available services are:

- Authenticate users
- Making payment
- Verifying payment order
- Checking verified payment order status

## Shurjopay plugin (Python)

ShurjoMukhi Limited developed plugin for integration with java based. shurjoPay plugin helps merchants and service providers to integrate easity by using this plugin. Plugin provides 3 services mainly such as

- Make Payment
- Verify payment order
- Check verified order status

## How to implement

### Before All:

First of all, developers have to configure a .env file in their respective project with four variables, which are SP_USERNAME,
SP_PASSWORD, SHURJOPAY_API, SP_CALLBACK and use these to configure the ShurjopayConfigModel to create a instance of Shurjopay python plugin

- **Example Projcet**

```env
SP_USERNAME=sp_sandbox
SP_PASSWORD=pyyk97hu&6u6
SHURJOPAY_API=https://sandbox.shurjopayment.com/api/
SP_CALLBACK=https://sandbox.shurjopayment.com/response/
```

> 📝 **NOTE** For Shurjopay version 3 live engine integration all necessary credential will be given to merchant after subscription completed on Shurjopay gateway.

### Installation

> 📝 **NOTE** Install the package inside your python project environment

Use the package manager `pip` to install Shuropay python package

```
pip install shurjopay-v3
```

To install Python package from github, you need to clone the repository.

```
git clone https://github.com/shurjopay-plugins/sp-plugin-python
```

Then just run the setup.py file from that directory,

```
python setup.py install
```

### Configuration

Configure shurjoPay Config-Model to create an instance of surjoPay Class

```python

sp_config = ShurjoPayConfigModel(
        SP_USERNAME = settings.SP_USERNAME,
        SP_PASSWORD = settings.SP_PASSWORD,
        SHURJOPAY_API = settings.SHURJOPAY_API,
        SP_CALLBACK = settings.SP_CALLBACK)

shurjopay = ShurjoPayPlugin(sp_config)

```

---

# Use Case

## Make Payment

Merchants and service providers can make payment by calling this service. Developer should call make_payment() method with payment request parameter. Shurjopay needs some information to perform creating payment request. So that, this service requires request payment object. After calling this service, it returns response object containing payment URL and customer information.

**Example**

- Payment Request

```python
payment_request = PaymentRequestModel(
            prefix='sp',
            amount=1000.00,
            order_id='sp215689',
            currency='BDT',
            customer_name='Mahabubul Hasan',
            customer_address='Holding no-N/A, Road-16, Gulshan-1, Dhaka' ,
            customer_phone='01700000000',
            customer_city='Dhaka',
            customer_post_code='1212',
            client_ip='127.456.1.1'
        )
payment_details = shurjopay.make_payment(payment_request)
```

- Payment Request Response

```
    payment_url= <generated payment url by shurjoPay gateway>
	amount=1000.00
	currency=BDT
	sp_order_id=sp32aad7c6dad7a
	customer_order_id=sp215689
	customer_name=Mahabubul Hasan
	customer_address=Holding no-N/A, Road-16, Gulshan-1, Dhaka
	customer_phone=01766666666
	customer_city=Dhaka
	customer_email=Null
	client_ip=127.456.1.1
	intent=sale
	transactionStatus=Initiated
	sp_code=null
	message=null
```

## Verify payment order:

After a successful payment, merchants or service providers have to verify payment order. Developers must call verify_payment() method with Shurjopay order id parameter that is provided by payment response named "sp_order_id". A successful verification returns an order object.

**Example**

- Request verification of an order

```
Parameter: sp_order_id
```

- Response

```
order_id=sp32aad7c6dad7a
currency=BDT
amount=10
payable_amount=10
discount_amount=null
discpercent=0
usd_mmt=0
usd_rate=0
method=null
sp_msg=initiated
sp_code=1068
name=mahabubul
email=mahabubul@example.com
address=Holding no-N/A, Road-16, Gulshan-1, Dhaka
city=Dhaka
value1=value1
value2=value2
value3=value3
value4=value4

```

## Example Apps

### [Django](https://github.com/shurjopay-plugins/sp-plugin-usage-examples/tree/dev/django-app-python-plugin)

## Documentation

### [Developer-Guideline](doc/sp_plugin_developer_guideline.md)

### [Github](https://github.com/shurjopay-plugins)

## Contacts

[Shurjopay](https://shurjopay.com.bd/#contacts)

## License

[MIT](https://choosealicense.com/licenses/mit/)
