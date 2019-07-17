"""
Load Configrations from ini file
@params path : String
@returns username : String, password : String
"""

import os
import configparser

def load_configrations(path):
    parser = configparser.ConfigParser()
    parser.read(path, encoding='utf-8')
    
    items = parser.items('DEFAULT')

    username = items[0][1]
    password = items[1][1]

    return username, password