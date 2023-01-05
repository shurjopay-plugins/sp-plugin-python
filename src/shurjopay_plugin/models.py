class ShurjoPayConfigModel(object):
    '''This class is used to store Shurjopay configuration details'''
    def __init__(self, SP_USERNAME, SP_PASSWORD, SP_ENDPOINT, SP_CALLBACK,SP_PREFIX,SP_LOGDIR):
        self.SP_USERNAME:str = SP_USERNAME # shurjopay username
        self.SP_PASSWORD:str = SP_PASSWORD # shurjopay password
        self.SP_ENDPOINT:str = SP_ENDPOINT # shurjopay api endpoint
        self.SP_CALLBACK:str = SP_CALLBACK # marchent callback url
        self.SP_PREFIX:str = SP_PREFIX # shurjopay store unique id 
        self.SP_LOGDIR:str = SP_LOGDIR # shurjopay log directory  

class ShurjoPayTokenModel(object):
    '''This class is used to store Shurjopay authentication token details'''
    def __init__(self, token, store_id, execute_url, token_type, sp_code, message, token_create_time, expires_in) -> None:
        self.token:str = token # authentication token
        self.store_id:str = store_id # store id of marchent
        self.execute_url:str = execute_url # payment execute url
        self.token_type:str = token_type # token type - Bearer
        self.sp_code:str = sp_code # shurjopay  status code
        self.message:str = message # shurjopay status message
        self.token_create_time:str = token_create_time # shurjopay token create time
        self.expires_in:int = expires_in # shurjopay token expire time (in seconds)

class PaymentRequestModel(object):
    '''This class is used to store payment request details'''
    def __init__(self, amount, order_id,  currency, customer_name, customer_address, customer_phone, customer_city, customer_post_code) -> None:
        #self.prefix:str = prefix # payment prefix
        self.amount:float = amount # request amount
        self.order_id:str = order_id # marchent order id
        self.currency:str = currency # payment currency
        self.customer_name:str = customer_name # customer name
        self.customer_address:str = customer_address # customer address
        self.customer_phone:str = customer_phone # customer phone
        self.customer_city:str = customer_city # customer city 
        self.customer_post_code:str = customer_post_code # customer post code


class PaymentDetailsModel(object):
    '''This class is used to store payment details'''
    def __init__(self, checkout_url, amount, currency, sp_order_id, customer_order_id,sp_code, customer_name, customer_address, customer_city, customer_phone, customer_email, client_ip, intent, transactionStatus) -> None:
        self.checkout_url:str = checkout_url # shurjopay checkout url to redirect to payment page
        self.amount:float = amount # payment amount
        self.currency:str = currency # payment currency
        self.sp_code:str = sp_code # shurjopay status code
        self.sp_order_id:str = sp_order_id # shurjopay order id
        self.customer_order_id:str = customer_order_id # marchent order id
        self.customer_name:str = customer_name # customer name
        self.customer_address:str = customer_address # customer address
        self.customer_city:str = customer_city # customer city
        self.customer_phone:str = customer_phone # customer phone
        self.customer_email:str = customer_email # customer email
        self.client_ip:str = client_ip # client ip
        self.intent:str = intent # payment intent
        self.transactionStatus:str = transactionStatus # payment transaction status


class VerifiedPaymentDetailsModel(object):
    '''This class is used to store verified payment details'''
    def __init__(self, id, order_id, currency, amount, payable_amount, recived_amount, discount_amount, disc_percent, usd_amt, usd_rate, card_holder_name, card_number, phone_no, bank_trx_id, invoice_no, bank_status, customer_order_id, sp_massage,sp_message, sp_code, name, email, address, city, value1, value2, value3, value4, transaction_status, method, date_time):
        self.id:int = id # shurjopay payment id
        self.order_id:str = order_id # shurjopay order id
        self.currency:str = currency # payment currency
        self.amount:float = amount # payment amount
        self.payable_amount:float = payable_amount # payment payable amount
        self.recived_amount:str = recived_amount # payment received amount
        self.discount_amount:float = discount_amount # payment discount amount
        self.disc_percent:int = disc_percent # payment discount percent
        self.usd_amt:int = usd_amt # payment usd amount
        self.usd_rate:int = usd_rate # payment usd rate
        self.card_holder_name:str = card_holder_name # card holder name
        self.card_number:str = card_number # payment card number
        self.phone_no :str= phone_no # customer phone number
        self.bank_trx_id:str = bank_trx_id # bank transaction id
        self.invoice_no:str = invoice_no # invoice number
        self.bank_status:str = bank_status # bank status
        self.customer_order_id:str = customer_order_id # marchent order id
        self.sp_massage:str = sp_massage # shurjopay message
        self.sp_message:str=sp_message
        self.sp_code:str = sp_code # shurjopay status code
        self.name:str = name # customer name
        self.email:str = email # customer email
        self.address:str = address  # customer address
        self.city:str = city # customer city
        '''
        Sometime customer have to send additional data like studentId 
	    or any other information which have not any field given by shurjoPay.
	    value1, value2, value3, value4 is used for customer's additional info if needed
        '''
        self.value1:str = value1
        self.value2:str = value2
        self.value3:str = value3
        self.value4:str = value4
        self.transaction_status:str = transaction_status # payment transaction status
        self.method:str = method # payment method
        self.date_time:str = date_time # payment date time
