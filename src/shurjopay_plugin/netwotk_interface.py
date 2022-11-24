from urllib.request import urlopen
from shurjopay_exceptions import ShurjoPayException
import re as r

def getIP():
    '''
    @return the IP address of the marchents server
    @raise ShurjoPayException if IP address is not found 
    '''
    try:
        data = str(urlopen('http://checkip.dyndns.com/').read()) # Open the oracle checkip url and read the data
        return r.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1) # Return the IP address by using regex
    except ShurjoPayException as ex:
        raise ShurjoPayException('Marchent IP Address not found!', ex) # Raise exception if IP address is not found