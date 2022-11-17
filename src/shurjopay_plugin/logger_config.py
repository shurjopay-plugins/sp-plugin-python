import os
import logging
from enum import Enum



def get_log_dir():
    #TODO test the log locations in windows and linux
    """
    Get the log directory based on different operating systems
    """
    log_dir = ""
    if os.name == 'nt':
        log_dir = os.path.expandvars(r'%APPDATA%\Local')
    else:
        log_dir = os.path.expanduser('~/var/')
    return log_dir


'''
    Logger configurations for Shurjopay
    Creates a logger instance to log the actions ,Defines file handeler and set formatter,Adds file handler to logger
'''

logger = logging.getLogger(__name__)
logger.info("ShurjopayConfig initialized")

log_fileName = os.path.join(get_log_dir(), 'logs')+'/shurjopay.log'
os.makedirs(os.path.dirname(log_fileName), exist_ok=True)
logging.basicConfig(
    level=logging.ERROR,
    format=" '%(asctime)s : %(levelname)s :gs %(name)s : %(funcName)s  %(message)s'",
    handlers=[
        logging.FileHandler(log_fileName, mode="a", encoding=None),
        logging.StreamHandler()
    ]
)

