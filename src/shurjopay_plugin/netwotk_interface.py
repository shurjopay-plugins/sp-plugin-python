from urllib.request import urlopen
import re as r
def getIP():
    '''Returns the IP address of the marchents server'''
    d = str(urlopen('http://checkip.dyndns.com/')
            .read())

    return r.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)

