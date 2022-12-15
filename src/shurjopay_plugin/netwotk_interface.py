from urllib.request import urlopen
from .shurjopay_exceptions import ShurjopayException
import re as r

def getIP():
    '''
    This method is used to get the IP address of the marchent server
    :return the IP address as string
    :raise ShurjoPayException if IP address is not found 
    '''
    try:
        data = str(urlopen('http://checkip.dyndns.com/').read()) # Open the oracle checkip url and read the data
        return r.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1) # Return the IP address by using regex
    except ShurjopayException as ex:
        raise ShurjopayException('Marchent IP Address not found!', ex) # Raise exception if IP address is not found