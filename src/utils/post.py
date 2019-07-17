"""
HTTP Post
"""

import requests

def post(url, data, headers):
    session = requests.Session()
    session.keep_alive = False
    res = session.post(url, data=data, headers=headers)
    session.close()

    return res