'''
Dnspod API Client
'''

import json
from utils import simple_http as http

RECORD_LIST_URL = 'https://dnsapi.cn/Record.List'
DNSPOD_UPDTAE_URL = 'https://dnsapi.cn/Record.Ddns'

class DnsPodClient:
    '''
    A simple DnsPod client for calling Dnspod APIs easily

    @params - (dnspod_id, dnspod_token, author_email, app_version, app_name='ahucv_ddns')
    '''
    def __init__(self, dnspod_id, dnspod_token, author_email, app_version, app_name='ahucv_ddns'):
        # Ref: https://www.dnspod.cn/docs/info.html#specification
        self.app_name = app_name
        self.author_email = author_email
        self.app_version = app_version
        self.header = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'text/json',
            'User-Agent': f'{ self.app_name }/{ self.app_version } ({ self.author_email })'
        }
        self.dnspod_base_payload = {
            'login_token': f'{ dnspod_id },{ dnspod_token }',
            'format': 'json',
            'lang': 'en',
            'error_on_empty': 'yes'
        }
    
    def get_record(self, sub_domain, domain):
        '''
        Get corresponding record by providing sub_domain and domain

        @return - (record_id, current_ip)
        '''
        payload = {
            **self.dnspod_base_payload,
            'sub_domain': sub_domain,
            'domain': domain
        }

        res = http.post(RECORD_LIST_URL, data=payload, headers=self.header)
        record_id = json.loads(res.text)['records'][0]['id']
        current_ip = json.loads(res.text)['records'][0]['value']

        return (record_id, current_ip)

    def update_ip(self, sub_domain, domain, record_id, new_ip):
        '''
        Update IP by providing the sub_domain, domain and record_id

        @return True if success else False
        '''
        dnspod_update_payload = {
                **self.dnspod_base_payload,
                'record_id': record_id,
                'record_line_id': 0,
                'value': new_ip,
                'sub_domain': sub_domain,
                'domain': domain
        }

        if new_ip:
            update_result = http.post(DNSPOD_UPDTAE_URL, dnspod_update_payload, self.header)
            res_code = json.loads(update_result.text)['status']['code']
            update_result = True if res_code else False

            return update_result