import os
import logging


class ShurjopayLoggerConfig(object):
    '''Shurjopay logger can be initialized by using one of the following methods: 
        -default logger. 
        -file logger.  
    '''
    logger = logging.getLogger(__name__)
    loglevel = logging.INFO
   
    def get_logger(self):
        """Returns: default logger instance."""
        return self.logger
    
    def get_file_logger(self,file_path):
        """ Creates a file logger (shurjopay.log) at the file path provided.
       Log level is set to INFO by default. 
       The log file is created if it does not exist 
       and the logs are appended using basic logger config. 

        Args:
            file_path (str): path of the log file.

        Returns:
            logger: file logger instance.
        """
        # create log file if it does not exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # set basic configuration for logger
        logging.basicConfig(  
            level=self.loglevel,
            format=" '%(asctime)s : %(levelname)s :gs %(name)s : %(funcName)s  %(message)s'",
            handlers=[
                logging.FileHandler(file_path,
                                    mode="a", encoding=None, delay=True),
                logging.StreamHandler()
            ]
        )
        return self.logger
