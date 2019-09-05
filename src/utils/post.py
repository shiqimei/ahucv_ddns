'''
A simple HTTP Post method
'''

import requests

def post(url, data, headers=None):
    '''
    Post data by sepcifying target url, payload data and headers
    '''
    session = requests.Session()
    session.keep_alive = False
    res = session.post(url, data=data, headers=headers)
    session.close()

    return res
