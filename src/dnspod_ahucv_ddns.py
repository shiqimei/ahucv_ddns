from utils.load_configrations import load_configrations
from utils.post import post
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from re import MULTILINE, findall
from datetime import datetime
from subprocess import PIPE, Popen
import json
import requests

sub_domain = 's1'
domain = 'lolimay.cn'

config_path = './config.ini'
dnspod_config_path = './dnspod.ini'
chrome_driver_path = './chromedriver'
username, password = load_configrations(config_path)
dnspod_id, dnspod_token = load_configrations(dnspod_config_path)
ip = ''
ip_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
need_update = False
update_result = ''

url = 'http://172.16.254.19:8080/Self/nav_login'
login_url = 'http://172.16.254.19:8080/Self/LoginAction.action'
check_code_url = 'http://172.16.254.19:8080/Self/RandomCodeAction.action'
refresh_account = 'http://172.16.254.19:8080/Self/refreshaccount'
logged_url = 'http://172.16.254.19:8080/Self/nav_offLine'
ip_regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
ip = ''
auth = {
    'account': username,
    'password': password,
    'code': '',
    'checkcode': '',
    'Submit': 'Login'
}
record_list_url = 'https://dnsapi.cn/Record.List'
dnspod_update_url = 'https://dnsapi.cn/Record.Ddns'

with Popen(['node', './tools/md5.js', auth['password']], stdout=PIPE) as proc:
    md5 = json.loads(proc.stdout.read())
    auth['password'] = md5['password']

    s = requests.session()
    res = s.get(url)
    s.get(check_code_url)
    auth['checkcode'] = findall('checkcode="(\d{4})"', res.text, MULTILINE)[0]
    s.post(login_url, params=auth)
    logged_page = s.get(logged_url)

    # fetch current IP
    try:
        ip = findall(ip_regex, logged_page.text, MULTILINE)[0]
        get_current_ip_time = datetime.now()
    except:
        print('[ERROR] IP is not valid.')
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

res = post(record_list_url, data=dnspod_payload, headers=header)
record_id = json.loads(res.text)['records'][0]['id']
last_ip = json.loads(res.text)['records'][0]['value']
get_last_ip_time = datetime.now()

dnspod_update_payload = {
    **dnspod_payload,
    'record_id': record_id,
    'record_line_id': 0,
    'value': ip
}

print(ip)

if ip != last_ip:
    need_update = True
    update_result = post(dnspod_update_url, dnspod_update_payload, header)
    res_code = json.loads(update_result.text)['status']['code']
    update_result = 'Success' if res_code else 'Failed'

# Print results
print(f'''
[{ get_current_ip_time }] Current IP: { ip }
[{ get_last_ip_time }] Last IP: { last_ip }
[{ datetime.now() }] { update_result if need_update else "No Need To Update" }
''')
