class ShurjopayException(Exception):
    ''' Handles exceptions during payment process with ShurjoPay '''
    def __init__(self, message, errors):
        super().__init__(message, errors)
