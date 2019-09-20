'''
AHUCV server dynamic DNS updater
'''

from re import MULTILINE, findall
from datetime import datetime
import json
import requests
from utils import config, simple_http as http, DrCOM

APP_VERSION = '0.4.0'
CONFIG_PATH = './config.ini'
record_list_url = 'https://dnsapi.cn/Record.List'
dnspod_update_url = 'https://dnsapi.cn/Record.Ddns'

username, password = config.load(CONFIG_PATH, 'AUTH')
dnspod_id, dnspod_token = config.load(CONFIG_PATH, 'DNSPOD')
sub_domain, domain = config.load(CONFIG_PATH, 'DOMAIN')
mac_address, *_ = config.load(CONFIG_PATH, 'CLIENT')

ip = DrCOM.get_ip_by_mac_address(username, password, mac_address)
need_update = False
update_result = ''

header = {
    'Content-type': 'application/x-www-form-urlencoded',
    'Accept': 'text/json',
    'User-Agent': f'ahucv_ddns/{ APP_VERSION } (lolimay@lolimay.cn)'
}

dnspod_payload = {
    'login_token': f'{ dnspod_id },{ dnspod_token }',
    'format': 'json',
    'lang': 'en',
    'error_on_empty': 'yes',
    'domain': domain,
    'sub_domain': sub_domain
}

res = http.post(record_list_url, data=dnspod_payload, headers=header)
record_id = json.loads(res.text)['records'][0]['id']
last_ip = json.loads(res.text)['records'][0]['value']
get_last_ip_time = datetime.now()

dnspod_update_payload = {
    **dnspod_payload,
    'record_id': record_id,
    'record_line_id': 0,
    'value': ip
}

if ip and ip != last_ip:
    need_update = True
    update_result = http.post(dnspod_update_url, dnspod_update_payload, header)
    res_code = json.loads(update_result.text)['status']['code']
    update_result = 'Success' if res_code else 'Failed'

# Print results
print(f'''
[{ get_last_ip_time }] { ip } -> { last_ip }
[{ datetime.now() }] { update_result if need_update else "No Need To Update" }
''')
