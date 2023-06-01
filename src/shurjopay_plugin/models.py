class ShurjoPayConfigModel():
    '''This class is used to store Shurjopay configuration details'''

    def __init__(self, SP_USERNAME, SP_PASSWORD, SP_ENDPOINT,
                 SP_RETURN, SP_CANCEL, SP_PREFIX, SP_LOGDIR):
        self.SP_USERNAME = str(SP_USERNAME)  # shurjopay username
        self.SP_PASSWORD = str(SP_PASSWORD)  # shurjopay password
        self.SP_ENDPOINT = str(SP_ENDPOINT)  # shurjopay api endpoint
        self.SP_RETURN = str(SP_RETURN)  # merchant return url
        self.SP_CANCEL = str(SP_CANCEL)  # merchant cancel url
        self.SP_PREFIX = str(SP_PREFIX)  # shurjopay store unique id
        self.SP_LOGDIR = str(SP_LOGDIR)  # shurjopay log directory


class ShurjoPayTokenModel():
    '''This class is used to store Shurjopay authentication token details'''

    def __init__(self, **kwargs):
        self.token = str(kwargs.get('token'))
        self.store_id = str(kwargs.get('store_id'))
        self.execute_url = str(kwargs.get('execute_url'))
        self.token_type = str(kwargs.get('token_type'))
        self.sp_code = str(kwargs.get('sp_code'))
        self.message = str(kwargs.get('message'))
        self.token_create_time = str(kwargs.get('token_create_time'))
        self.expires_in = int(kwargs.get('expires_in'))


class PaymentRequestModel():
    '''This class is used to store payment request details'''

    def __init__(self, amount, order_id, currency, customer_name,
                 customer_address, customer_phone, customer_city,
                 customer_post_code):
        self.amount = float(amount)  # request amount
        self.order_id = str(order_id)  # merchant order id
        self.currency = str(currency)  # payment currency
        self.customer_name = str(customer_name)  # customer name
        self.customer_address = str(customer_address)  # customer address
        self.customer_phone = str(customer_phone)  # customer phone
        self.customer_city = str(customer_city)  # customer city
        self.customer_post_code = str(customer_post_code)  # customer post code


class PaymentDetailsModel():
    '''This class is used to store payment details'''

    def __init__(self, **kwargs):
        # shurjopay checkout url to redirect to payment page
        self.checkout_url = str(kwargs.get('checkout_url'))
        self.amount = float(kwargs.get('amount'))
        self.currency = str(kwargs.get('currency'))
        self.sp_order_id = str(kwargs.get('sp_order_id'))
        self.customer_order_id = str(kwargs.get('customer_order_id') or '')
        self.customer_name = str(kwargs.get('customer_name') or '')
        self.customer_address = str(kwargs.get('customer_address') or '')
        self.customer_city = str(kwargs.get('customer_city') or '')
        self.customer_phone = str(kwargs.get('customer_phone') or '')
        self.customer_email = str(kwargs.get('customer_email') or '')
        self.merchant_server_ip = str(kwargs.get('client_ip') or '')
        self.payment_intention = str(kwargs.get('intent') or '')
        self.transaction_status = str(kwargs.get('transactionStatus') or '')


class VerifiedPaymentDetailsModel():
    '''This class is used to store verified payment details'''

    def __init__(self, **kwargs):

        self.payment_id = int(kwargs.get('id'))
        self.shurjopay_order_id = str(kwargs.get('order_id'))
        self.merchant_invoice_no = str(kwargs.get('invoice_no'))

        self.currency = str(kwargs.get('currency'))  # payment currency
        self.amount = float(kwargs.get('amount'))  # payment amount
        self.payable_amount = float(kwargs.get('payable_amount'))
        self.received_amount = float(kwargs.get('recived_amount'))
        self.discount_amount = float(kwargs.get('discount_amount'))
        self.discount_percent = int(kwargs.get('disc_percent'))
        self.usd_amount = float(kwargs.get('usd_amt'))
        self.usd_rate = int(kwargs.get('usd_rate'))
        self.card_holder_name = str(kwargs.get('card_holder_name') or '')
        self.card_number = str(kwargs.get('card_number') or '')

        self.transaction_status = str(kwargs.get('transaction_status') or '')
        # payment method e.g.. bkash/rocket/nagad
        self.payment_method = str(kwargs.get('method') or '')
        self.payment_confirmed_at = str(kwargs.get('date_time'))

        self.payment_verification_status = bool(kwargs.get('is_verify'))
        self.bank_status = str(kwargs.get('bank_status') or '')
        self.customer_order_id = str(kwargs.get('customer_order_id') or '')
        self.shurjopay_message = str(kwargs.get('sp_message') or '')
        self.shurjopay_code = str(kwargs.get('sp_code') or '')

        self.customer_phone_no = str(kwargs.get('phone_no') or '')
        self.customer_name = str(kwargs.get('name') or '')
        self.customer_email = str(kwargs.get('email') or '')
        self.customer_address = str(kwargs.get('address') or '')
        self.customer_city = str(kwargs.get('city') or '')
        '''
        Sometimes customers have to send additional data like studentId 
        or any other information which is not provided by shurjoPay.
        value1, value2, value3, value4 are used for customer's 
        additional info if needed.
        '''
        self.value1 = str(kwargs.get('value1') or '')
        self.value2 = str(kwargs.get('value2') or '')
        self.value3 = str(kwargs.get('value3') or '')
        self.value4 = str(kwargs.get('value4') or '')
