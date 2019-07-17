"""
Load Configrations from ini file
@params path : String
@returns username : String, password : String
"""

import os
import configparser

def load_configrations(path, key='DEFAULT'):
    parser = configparser.ConfigParser()
    parser.read(path, encoding='utf-8')
    
    items = parser.items(key)

    return items[0][1], items[1][1]