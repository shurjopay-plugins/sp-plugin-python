import os
import logging

'''
    Logger configurations for Shurjopay
    Creates a logger instance to log the actions ,Defines file handeler and set formatter,Adds file handler to logger
'''
basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
logger = logging.getLogger(__name__)
logger.info("ShurjopayConfig initialized")
log_fileName = os.path.join(basedir, 'logs')+'/shurjopay.log'
os.makedirs(os.path.dirname(log_fileName), exist_ok=True)
logging.basicConfig(
    level=logging.ERROR,
    format=" '%(asctime)s : %(levelname)s :gs %(name)s : %(funcName)s  %(message)s'",
    handlers=[
        logging.FileHandler(log_fileName, mode="a", encoding=None),
        logging.StreamHandler()
    ]
)
