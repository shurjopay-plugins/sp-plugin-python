from email.mime import base
import os
import logging
import datetime


class ShurjoPayConfig(object):
    '''
    Configurations class for Shurjopay
    Creates environment variable to retrive data from .env file
    Creates a logger instance to log the actions ,Defines file handeler and set formatter,Adds file handler to logger
    '''
    __basedir = os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.info("ShurjopayConfig initialized")
        self._log_fileName = os.path.join(
            self.__basedir, 'logs')+'/shurjopay.log'
        os.makedirs(os.path.dirname(self._log_fileName), exist_ok=True)
        logging.basicConfig(
            level=logging.DEBUG,
            format=" '%(asctime)s : %(levelname)s :gs %(name)s : %(funcName)s  %(message)s'",
            handlers=[
                logging.FileHandler(self._log_fileName,
                                    mode="a", encoding=None),
                logging.StreamHandler()
            ]
        )
