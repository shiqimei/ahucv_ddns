'''
AHUCV server dynamic DNS updater
'''

from re import MULTILINE, findall
from datetime import datetime
import requests
from utils import config, DrCOM, DnsPod

APP_VERSION = '1.0.0'
CONFIG_PATH = 'config.ini'

username, password = config.load(CONFIG_PATH, 'AUTH')
dnspod_id, dnspod_token, author_email = config.load(CONFIG_PATH, 'DNSPOD')
sub_domain, domain = config.load(CONFIG_PATH, 'DOMAIN')
mac_address, *_ = config.load(CONFIG_PATH, 'CLIENT')

need_update = False
update_result = ''

new_ip = DrCOM.get_ip_by_mac_address(username, password, mac_address)
dnspod_client = DnsPod.DnsPodClient(dnspod_id, dnspod_token, author_email, APP_VERSION)
record_id, old_ip = dnspod_client.get_record(sub_domain, domain)

if new_ip and old_ip and new_ip != old_ip:
    need_update = True
    result = dnspod_client.update_ip(sub_domain, domain, record_id, new_ip)
    update_result = 'Success' if result else 'Failed'

print(f'''
[{ datetime.now() }] { old_ip } -> { new_ip }
[{ datetime.now() }] { update_result if need_update else "No Need To Update" }
''')
