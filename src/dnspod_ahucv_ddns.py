'''
AHUCV server dynamic DNS updater
'''

from re import MULTILINE, findall
from datetime import datetime
import json
import requests
from utils import config, md5, http

config_path = './config.ini'

username, password = config.load(config_path, 'AUTH')
dnspod_id, dnspod_token = config.load(config_path, 'DNSPOD')
sub_domain, domain = config.load(config_path, 'DOMAIN')

ip = ''
ip_regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
need_update = False
update_result = ''

url = 'http://172.16.254.19:8080/Self/nav_login'
login_url = 'http://172.16.254.19:8080/Self/LoginAction.action'
check_code_url = 'http://172.16.254.19:8080/Self/RandomCodeAction.action'
logged_url = 'http://172.16.254.19:8080/Self/nav_offLine'
ip_regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
ip = ''
auth = {
    'account': username,
    'password': md5.encode(password),
    'code': '',
    'checkcode': '',
    'Submit': 'Login'
}
record_list_url = 'https://dnsapi.cn/Record.List'
dnspod_update_url = 'https://dnsapi.cn/Record.Ddns'

s = requests.session()
res = s.get(url)
s.get(check_code_url)

try:
    auth['checkcode'] = findall(r'checkcode="(\d{4})"', res.text, MULTILINE)[0]
except IndexError:
    exit()

s.post(login_url, params=auth)
logged_page = s.get(logged_url)

# fetch current IP
try:
    ip = findall(ip_regex, logged_page.text, MULTILINE)[0]
    get_current_ip_time = datetime.now()
except IndexError:
    exit()

header = {
    'Content-type': 'application/x-www-form-urlencoded',
    'Accept': 'text/json',
    'User-Agent': 'ahucv_ddns/0.1.0 (lolimay@lolimay.cn)'
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

if ip != last_ip:
    need_update = True
    update_result = http.post(dnspod_update_url, dnspod_update_payload, header)
    res_code = json.loads(update_result.text)['status']['code']
    update_result = 'Success' if res_code else 'Failed'

# Print results
print(f'''
[{ get_current_ip_time }] Current IP: { ip }
[{ get_last_ip_time }] Last IP: { last_ip }
[{ datetime.now() }] { update_result if need_update else "No Need To Update" }
''')
