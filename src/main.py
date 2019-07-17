from utils.load_configrations import load_configrations
from utils.post import post
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from re import match, MULTILINE
import re
import json

sub_domain = 's1'
domain = 'lolimay.cn'

config_path = './config.ini'
dnspod_config_path = './dnspod.ini'
chrome_driver_path = './chromedriver'
username, password = load_configrations(config_path)
dnspod_id, dnspod_token = load_configrations(dnspod_config_path)
ip_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"

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

browser.get(login_url)

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
ip = re.findall(ip_regex, logged_page, MULTILINE)[0]

print(f'Current IP: { ip }')

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

print(f'Last IP: { last_ip }')

dnspod_update_payload = {
    **dnspod_payload,
    'record_id': record_id,
    'record_line_id': 0,
    'value': ip
}



if ip != last_ip:
    update_result = post(dnspod_update_url, dnspod_update_payload, header)
    print(json.dumps(json.loads(update_result.text), indent=4))

print('There is no need to update!')