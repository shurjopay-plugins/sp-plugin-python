import os
import logging


class ShurjopayLoggerConfig(object):
    '''
    Logger configurations for Shurjopay plugin.
    Creates a logger instance to log the activities performed by the plugin.
    Defines file handeler and set formatter,
    Adds file handler to logger
    '''

    def __init__(self, log_file_path):
        ''' Initialize the logger config with a destination file path '''
        # TODO what happens if anyone inits this class without log file
        self.log_file_path = log_file_path

    def get_logger(self):
        ''' Retuns a logger instance '''
        logger = logging.getLogger(__name__)
        # TODO why info log this message always
        logger.DEBUG("ShurjopayConfig initialized")
        # create log file if it does not exist
        os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)
        logging.basicConfig(  # set basic config
            level=logging.INFO,
            format=" '%(asctime)s : %(levelname)s :gs %(name)s : %(funcName)s  %(message)s'",
            handlers=[
                logging.FileHandler(self.log_file_path,
                                    mode="a", encoding=None, delay=True),
                logging.StreamHandler()
            ]
        )
        return logger
