class AuthException(Exception):
    def __init__(self, *args: object) -> None:
        if args:
            self.message = args[0]
        else:
            self.message = None
    
    def __str__(self) -> str:
        if self.massage:
            return 'Shurjopay AuthException , {0} '.format(self.message)
        else:
            return 'Shurjopay Authentication Exception Raised!'

class PaymentException(Exception):
    def __init__(self, *args: object) -> None:
        if args:
            self.message = args[0]
        else:
            self.message = None
    
    def __str__(self) -> str:
        if self.massage:
            return 'Shurjopay PaymentException: {0} '.format(self.message)
        else:
            return 'Shurjopay PaymentException Raised!'
       