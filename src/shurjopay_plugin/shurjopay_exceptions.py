class AuthException(Exception):
    '''This class is used to handle authentication exception'''
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


class PaymentException(Exception):
    '''This class is used to handle payment exception'''
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors
