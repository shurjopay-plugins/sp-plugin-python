class ShurjoPayConfigModel(object):
    '''This class is used to store Shurjopay configuration details'''

    def __init__(self, SP_USERNAME, SP_PASSWORD, SP_ENDPOINT, SP_RETURN, SP_CANCEL, SP_PREFIX, SP_LOGDIR):
        self.SP_USERNAME: str = SP_USERNAME  # shurjopay username
        self.SP_PASSWORD: str = SP_PASSWORD  # shurjopay password
        self.SP_ENDPOINT: str = SP_ENDPOINT  # shurjopay api endpoint
        self.SP_RETURN: str = SP_RETURN  # merchant retrun url
        self.SP_CANCEL: str = SP_CANCEL  # merchant cancel url
        self.SP_PREFIX: str = SP_PREFIX  # shurjopay store unique id
        self.SP_LOGDIR: str = SP_LOGDIR  # shurjopay log directory


class ShurjoPayTokenModel(object):
    '''This class is used to store Shurjopay authentication token details'''

    def __init__(self, **kwargs) -> None:

        self.token: str = kwargs.get('token')
        self.store_id: str = kwargs.get('store_id')
        self.execute_url: str = kwargs.get('execute_url')
        self.token_type: str = kwargs.get('token_type')
        self.sp_code: str = kwargs.get('sp_code')
        self.message: str = kwargs.get('message')
        self.token_create_time: str = kwargs.get('token_create_time')
        self.expires_in: int = kwargs.get('expires_in')


class PaymentRequestModel(object):
    '''This class is used to store payment request details'''

    def __init__(self, **kwargs) -> None:
        self.amount: float = kwargs.get('amount')
        self.order_id: str = kwargs.get('order_id')
        self.currency: str = kwargs.get('currency')
        self.customer_name: str = kwargs.get('customer_name')
        self.customer_address: str = kwargs.get('customer_address')
        self.customer_phone: str = kwargs.get('customer_phone')
        self.customer_city: str = kwargs.get('customer_city')
        self.customer_post_code: str = kwargs.get('customer_post_code')


class PaymentDetailsModel(object):
    '''This class is used to store payment details'''

    def __init__(self, **kwargs) -> None:
        # shurjopay checkout url to redirect to payment page
        self.checkout_url: str = kwargs.get('checkout_url')
        self.amount: float = kwargs.get('amount')
        self.currency: str = kwargs.get('currency')
        self.sp_order_id: str = kwargs.get('sp_order_id')
        self.customer_order_id: str = kwargs.get('customer_order_id')
        self.customer_name: str = kwargs.get('customer_name')
        self.customer_address: str = kwargs.get('customer_address')
        self.customer_city: str = kwargs.get('customer_city')
        self.customer_phone: str = kwargs.get('customer_phone')
        self.customer_email: str = kwargs.get('customer_email')
        self.client_ip: str = kwargs.get('client_ip')
        self.intent: str = kwargs.get('intent')
        self.transactionStatus: str = kwargs.get('transactionStatus')


class VerifiedPaymentDetailsModel(object):
    '''This class is used to store verified payment details'''

    def __init__(self, **kwargs):
        self.id: int = kwargs.get('id')  # shurjopay payment id
        self.order_id: str = kwargs.get('order_id')  # shurjopay order id
        self.currency: str = kwargs.get('currency')  # payment currency
        self.amount: float = kwargs.get('currency')  # payment amount
        self.payable_amount: float = kwargs.get('payable_amount')
        self.recived_amount: float = kwargs.get('recived_amount')
        self.discount_amount: float = kwargs.get('discount_amount')
        self.disc_percent: int = kwargs.get('disc_percent')
        self.usd_amt: float = kwargs.get('usd_amt')
        self.usd_rate: int = kwargs.get('usd_rate')
        self.card_holder_name: str = kwargs.get('card_holder_name')
        self.card_number: str = kwargs.get('card_number')
        self.phone_no: str = kwargs.get('phone_no')
        # payment is verified or not
        self.is_verify: bool = kwargs.get('is_verify')
        # merchant invoice no
        self.invoice_no: str = kwargs.get('invoice_no')
        self.bank_status: str = kwargs.get('bank_status')
        self.customer_order_id: str = kwargs.get('customer_order_id')
        self.sp_message: str = kwargs.get('sp_message')
        self.sp_message: str = kwargs.get('currency')
        self.sp_code: str = kwargs.get('sp_code')
        self.name: str = kwargs.get('name')
        self.email: str = kwargs.get('email')
        self.address: str = kwargs.get('address')
        self.city: str = kwargs.get('city')
        '''
        Sometime customer have to send additional data like studentId 
	    or any other information which have not any field given by shurjoPay.
	    value1, value2, value3, value4 is used for customer's additional info if needed
        '''
        self.value1: str = kwargs.get('value1')
        self.value2: str = kwargs.get('value2')
        self.value3: str = kwargs.get('value3')
        self.value4: str = kwargs.get('value4')
        self.transaction_status: str = kwargs.get('transaction_status')
        # payment method e.g.. bkash/rocket/nagad
        self.method: str = kwargs.get('method')
        self.date_time: str = kwargs.get('date_time')  # payment timestamp
