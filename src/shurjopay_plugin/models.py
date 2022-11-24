class ShurjoPayConfigModel(object):
    '''ShurjoPayConfigModel class is used to store shurjoPay configuration details'''
    def __init__(self, SP_USERNAME, SP_PASSWORD, SHURJOPAY_API, SP_CALLBACK,SP_LOG_DIR):
        self.SP_USERNAME = SP_USERNAME # shurjopay username
        self.SP_PASSWORD = SP_PASSWORD # shurjopay password
        self.SHURJOPAY_API = SHURJOPAY_API # shurjopay api url
        self.SP_CALLBACK = SP_CALLBACK # marchent callback url
        self.SP_LOG_DIR = SP_LOG_DIR # shurjopay log directory  


class ShurjoPayTokenModel(object):
    '''ShurjoPayTokenModel class is used to store shurjoPay authentication token details'''
    def __init__(self, token, store_id, execute_url, token_type, sp_code, message, token_create_time, expires_in) -> None:
        self.token = token # shurjopay authentication token
        self.store_id = store_id # shurjopay store id
        self.execute_url = execute_url # shurjopay execute url for payment
        self.token_type = token_type # shurjopay token type
        self.sp_code = sp_code # shurjopay  status code
        self.message = message # shurjopay message
        self.token_create_time = token_create_time # shurjopay token create time
        self.expires_in = expires_in # shurjopay token expires in


class PaymentRequestModel(object):
    '''PaymentRequestModel class is used to store payment request details'''
    def __init__(self, prefix, amount, order_id,  currency, customer_name, customer_address, customer_phone, customer_city, customer_post_code) -> None:
        self.prefix = prefix # payment prefix
        self.amount = amount # request amount
        self.order_id = order_id # marchent order id
        self.currency = currency # payment currency
        self.customer_name = customer_name # customer name
        self.customer_address = customer_address # customer address
        self.customer_phone = customer_phone # customer phone
        self.customer_city = customer_city # customer city 
        self.customer_post_code = customer_post_code # customer post code


class PaymentDetailsModel(object):
    '''PaymentDetailsModel class is used to store payment details'''
    def __init__(self, checkout_url, amount, currency, sp_order_id, customer_order_id, customer_name, customer_address, customer_city, customer_phone, customer_email, client_ip, intent, transactionStatus) -> None:
        self.checkout_url = checkout_url # shurjopay checkout url to redirect to payment page
        self.amount = amount # payment amount
        self.currency = currency # payment currency
        self.sp_order_id = sp_order_id # shurjopay order id
        self.customer_order_id = customer_order_id # marchent order id
        self.customer_name = customer_name # customer name
        self.customer_address = customer_address # customer address
        self.customer_city = customer_city # customer city
        self.customer_phone = customer_phone # customer phone
        self.customer_email = customer_email # customer email
        self.client_ip = client_ip # client ip
        self.intent = intent # payment intent
        self.transactionStatus = transactionStatus # payment transaction status


class VerifiedPaymentDetailsModel(object):
    '''VerifiedPaymentDetailsModel class is used to store verified payment details'''
    def __init__(self, id, order_id, currency, amount, payable_amount, received_amount, discsount_amount, disc_percent, usd_amt, usd_rate, card_holder_name, card_number, phone_no, bank_trx_id, invoice_no, bank_status, customer_order_id, sp_message, sp_code, name, email, address, city, value1, value2, value3, value4, transaction_status, method, date_time):
        self.id = id # shurjopay payment id
        self.order_id = order_id # shurjopay order id
        self.currency = currency # payment currency
        self.amount = amount # payment amount
        self.payable_amount = payable_amount # payment payable amount
        self.received_amount = received_amount # payment received amount
        self.discsount_amount = discsount_amount # payment discount amount
        self.disc_percent = disc_percent # payment discount percent
        self.usd_amt = usd_amt # payment usd amount
        self.usd_rate = usd_rate # payment usd rate
        self.card_holder_name = card_holder_name # card holder name
        self.card_number = card_number # payment card number
        self.phone_no = phone_no # customer phone number
        self.bank_trx_id = bank_trx_id # bank transaction id
        self.invoice_no = invoice_no # invoice number
        self.bank_status = bank_status # bank status
        self.customer_order_id = customer_order_id # marchent order id
        self.sp_message = sp_message # shurjopay message
        self.sp_code = sp_code # shurjopay status code
        self.name = name # customer name
        self.email = email # customer email
        self.address = address  # customer address
        self.city = city # customer city
        self.value1 = value1
        self.value2 = value2
        self.value3 = value3
        self.value4 = value4
        self.transaction_status = transaction_status # payment transaction status
        self.method = method # payment method
        self.date_time = date_time # payment date time
