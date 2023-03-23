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
    
    def get_file_logger(self,log_file,permissions=0o644):
        """ Creates a file logger (shurjopay.log) at the file path provided.
       Log level is set to INFO by default. 
       The log file is created if it does not exist 
       and the logs are appended using basic logger config. 

        Args:
            file_path (str): path of the log file.

        Returns:
            logger: file logger instance.
        """
        # Create the log file if it doesn't exist
        if not os.path.exists(log_file):
            with open(log_file, 'w') as f:
                f.write('Shurjopay Log file Generated\n')
        # Set the permissions on the log file
        os.chmod(log_file, permissions)
        # set basic configuration for logger
        logging.basicConfig(  
            level=self.loglevel,
            format=" '%(asctime)s : %(levelname)s :gs %(name)s : %(funcName)s  %(message)s'",
            handlers=[
                logging.FileHandler(log_file,
                                    mode="a", encoding=None, delay=True),
                logging.StreamHandler()
            ]
        )
        return self.logger
