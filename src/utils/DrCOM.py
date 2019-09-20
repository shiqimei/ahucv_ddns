'''
Auhui University Dr.COM User Self-service System
'''

from re import MULTILINE, findall
import requests
from utils import md5

URL = 'http://172.16.254.19:8080/Self/nav_login'
LOGIN_URL = 'http://172.16.254.19:8080/Self/LoginAction.action'
CHECK_CODE_URL = 'http://172.16.254.19:8080/Self/RandomCodeAction.action'
LOGGED_URL = 'http://172.16.254.19:8080/Self/nav_offLine'
IP_REGEX = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

def get_ip_by_mac_address(username, password, mac_address):
    '''
    Get current online IP by mac address
    '''
    auth = {
        'account': username,
        'password': md5.encode(password),
        'code': '',
        'checkcode': '',
        'Submit': 'Login'
    }

    s = requests.session()
    res = s.get(URL)
    s.get(CHECK_CODE_URL)

    # Get the checkcode
    try:
        auth['checkcode'] = findall(r'checkcode="(\d{4})"', res.text, MULTILINE)[0]
    except IndexError:
        return None
    
    # Get the logged page
    s.post(LOGIN_URL, params=auth)
    logged_page = s.get(LOGGED_URL)

    # Match the current online IP by mac address
    try:
        ip_list = findall(fr'<tr>[\s|\S]+?</tr>', logged_page.text)
        for raw in ip_list:
            matched_ip = findall(fr'({ IP_REGEX })[\s|\S]+?{ mac_address }', raw)
            if matched_ip:
                return matched_ip[0]
        return None
    except IndexError:
        return None