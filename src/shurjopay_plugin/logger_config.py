import os
import logging
class ShurjopayLoggerConfig(object):
    '''
    Logger configurations for Shurjopay
    Creates a logger instance to log the actions, 
    Defines file handeler and set formatter,
    Adds file handler to logger
    '''
    def __init__(self, log_file_path):
        '''
        @param log_file_path: path to log file
        '''
        self.log_file_path = log_file_path
       
    def get_logger(self):
        '''
        @return: logger instance
        '''
        logger = logging.getLogger(__name__)
        logger.info("ShurjopayConfig initialized")
        os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True) # create log file if not exists
        logging.basicConfig( # set basic config
            level=logging.INFO,
            format=" '%(asctime)s : %(levelname)s :gs %(name)s : %(funcName)s  %(message)s'",
            handlers=[
                logging.FileHandler(self.log_file_path, mode="a", encoding=None,delay=True),
                logging.StreamHandler()
            ]
        )
        return logger

