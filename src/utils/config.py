'''
Load Configrations from ini file
'''

import configparser

def load_configrations(path, key='DEFAULT'):
    '''
    load configrations by specifying config file path and the section
    '''
    parser = configparser.ConfigParser()
    parser.read(path, encoding='utf-8')

    items = parser.items(key)

    return items[0][1], items[1][1]
