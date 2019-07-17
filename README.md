# ahucv_ddns

## Setup

```bash
virtualenv venv -p python3 && source venv/bin/activate
pip install -r requirements.txt # Install denpendencies
```


## 计划任务
```bash
*/1 * * * * /root/dnspod_ddns.sh &> /home/lolimay/Logs/
```