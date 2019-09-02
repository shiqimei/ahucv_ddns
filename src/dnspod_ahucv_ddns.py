from utils.load_configrations import load_configrations
from utils.post import post
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from re import MULTILINE, findall
from datetime import datetime
from json import loads, loads

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

login_url = 'http://172.16.254.19:8080/Self/LoginAction.action'
logged_url = 'http://172.16.254.19:8080/Self/nav_offLine'
record_list_url = 'https://dnsapi.cn/Record.List'
dnspod_update_url = 'https://dnsapi.cn/Record.Ddns'

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1024x1400")

browser = webdriver.Chrome(
    options=chrome_options,
    executable_path=chrome_driver_path
)

login_page = browser.get(login_url)

print(login_page)
exit()

username_input = browser.find_element_by_id('account')
password_input = browser.find_element_by_id('pass')
submit_button = browser.find_element_by_class_name('but')

# fill form and submit it
username_input.send_keys(username)
password_input.send_keys(password)
submit_button.click()

browser.get(logged_url)
logged_page = browser.page_source

# fetch current IP
try:
    ip = findall(ip_regex, logged_page, MULTILINE)[0]
    get_current_ip_time = datetime.now()
except:
    print('[ERROR] IP is not valid.')
    exit()

# close all chrome instances
browser.quit()

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
record_id = loads(res.text)['records'][0]['id']
last_ip = loads(res.text)['records'][0]['value']
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
    res_code = loads(update_result.text)['status']['code']
    update_result = 'Success' if res_code else 'Failed'

# Print results
print(f'''
[{ get_current_ip_time }] Current IP: { ip }
[{ get_last_ip_time }] Last IP: { last_ip }
[{ datetime.now() }] { update_result if need_update else "No Need To Update" }
''')
