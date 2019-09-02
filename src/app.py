import requests
from subprocess import Popen, PIPE
from re import MULTILINE, findall
import json

url = 'http://172.16.254.19:8080/Self/nav_login'
login_url = 'http://172.16.254.19:8080/Self/LoginAction.action'
check_code_url = 'http://172.16.254.19:8080/Self/RandomCodeAction.action'
refresh_account = 'http://172.16.254.19:8080/Self/refreshaccount'
logged_url = 'http://172.16.254.19:8080/Self/nav_offLine'
auth = {
    'account': 'E21714049',
    'password': '131452',
    'code': '',
    'checkcode': '',
    'Submit': 'Login'
}

with Popen(['node', './tools/md5.js', auth['password']], stdout=PIPE) as proc:
    md5 = json.loads(proc.stdout.read())
    auth['password'] = md5['password']

    s = requests.session()
    res = s.get(url)
    s.get(check_code_url)
    auth['checkcode'] = findall('checkcode="(\d{4})"', res.text, MULTILINE)[0]

    logged_page = s.post(login_url, params=auth)
    result = s.get(refresh_account)

    print(auth)
    print(logged_page.text)

    