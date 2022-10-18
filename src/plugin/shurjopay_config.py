import os
import environ
import logging
import datetime


class ShurjopayConfig(object):
    '''
        Creates a logger instance.
        Set Log level to DEBUG, INFO, WARNING, ERROR, CRITICAL
        Define file handeler and set formatter
        Add file handler to logger
    '''
    __basedir = os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))

    def __init__(self):
        self._env = environ.Env()
        self._env.read_env(os.path.join(self.__basedir, '.env'))
        self._logger = logging.getLogger(__name__)
        self._logger.info("ShurjopayConfig initialized")
        self._log_fileName = os.path.join(self.__basedir, self._env(
            'SP_LOG'))+'shurjopay.log'
        os.makedirs(os.path.dirname(self._log_fileName), exist_ok=True)
        logging.basicConfig(
            level=logging.DEBUG,
            format=" '%(asctime)s : %(levelname)s : %(name)s : %(funcName)s  %(message)s'",
            handlers=[
                logging.FileHandler(self._log_fileName,
                                    mode="a", encoding=None),
                logging.StreamHandler()
            ]
        )


sp = ShurjopayConfig()
