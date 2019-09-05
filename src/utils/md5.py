'''
md5 utilities
'''

import hashlib

def md5_encode(raw_string):
    '''
    Encode a string to md5
    '''
    return hashlib.md5(str(raw_string).encode()).hexdigest()
