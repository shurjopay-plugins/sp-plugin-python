class ShurjoPayConfigModel(object):
    '''ShurjoPayConfigModel class is used to store shurjoPay configuration details'''
    def __init__(self, SP_USERNAME, SP_PASSWORD, SHURJOPAY_API, SP_CALLBACK):
        self.SP_USERNAME = SP_USERNAME
        self.SP_PASSWORD = SP_PASSWORD
        self.SHURJOPAY_API = SHURJOPAY_API
        self.SP_CALLBACK = SP_CALLBACK


class ShurjoPayTokenModel(object):
    '''ShurjoPayTokenModel class is used to store shurjoPay authentication token details'''
    def __init__(self, token, store_id, execute_url, token_type, sp_code, message, token_create_time, expires_in) -> None:
        self.token = token
        self.store_id = store_id
        self.execute_url = execute_url
        self.token_type = token_type
        self.sp_code = sp_code
        self.message = message
        self.token_create_time = token_create_time
        self.expires_in = expires_in


class PaymentRequestModel(object):
    '''PaymentRequestModel class is used to store payment request details'''
    def __init__(self, prefix, amount, order_id,  currency, customer_name, customer_address, customer_phone, customer_city, customer_post_code) -> None:
        self.prefix = prefix
        self.amount = amount
        self.order_id = order_id
        self.currency = currency
        self.customer_name = customer_name
        self.customer_address = customer_address
        self.customer_phone = customer_phone
        self.customer_city = customer_city
        self.customer_post_code = customer_post_code


class PaymentDetailsModel(object):
    '''PaymentDetailsModel class is used to store payment details'''
    def __init__(self, checkout_url, amount, currency, sp_order_id, customer_order_id, customer_name, customer_address, customer_city, customer_phone, customer_email, client_ip, intent, transactionStatus) -> None:
        self.checkout_url = checkout_url
        self.amount = amount
        self.currency = currency
        self.sp_order_id = sp_order_id
        self.customer_order_id = customer_order_id
        self.customer_name = customer_name
        self.customer_address = customer_address
        self.customer_city = customer_city
        self.customer_phone = customer_phone
        self.customer_email = customer_email
        self.client_ip = client_ip
        self.intent = intent
        self.transactionStatus = transactionStatus


class VerifiedPaymentDetailsModel(object):
    '''VerifiedPaymentDetailsModel class is used to store verified payment details'''
    def __init__(self, id, order_id, currency, amount, payable_amount, received_amount, discsount_amount, disc_percent, usd_amt, usd_rate, card_holder_name, card_number, phone_no, bank_trx_id, invoice_no, bank_status, customer_order_id, sp_message, sp_code, name, email, address, city, value1, value2, value3, value4, transaction_status, method, date_time):
        self.id = id
        self.order_id = order_id
        self.currency = currency
        self.amount = amount
        self.payable_amount = payable_amount
        self.received_amount = received_amount
        self.discsount_amount = discsount_amount
        self.disc_percent = disc_percent
        self.usd_amt = usd_amt
        self.usd_rate = usd_rate
        self.card_holder_name = card_holder_name
        self.card_number = card_number
        self.phone_no = phone_no
        self.bank_trx_id = bank_trx_id
        self.invoice_no = invoice_no
        self.bank_status = bank_status
        self.customer_order_id = customer_order_id
        self.sp_message = sp_message
        self.sp_code = sp_code
        self.name = name
        self.email = email
        self.address = address
        self.city = city
        self.value1 = value1
        self.value2 = value2
        self.value3 = value3
        self.value4 = value4
        self.transaction_status = transaction_status
        self.method = method
        self.date_time = date_time
