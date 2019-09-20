'''
md5 utilities
'''

import hashlib

def encode(raw_string):
    '''
    Encode a string to md5
    '''
    return hashlib.md5(str(raw_string).encode()).hexdigest()
