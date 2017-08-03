import json
import requests
import time
import datetime
import hashlib
import sys

inputmsg = '有新消息'
if len(sys.argv) > 1:
    inputmsg = sys.argv[1]

MASTERSECRET = 'kYKOhKzQEh99uPSnDC6601'
APPKEY = '0OnxPftmrW6hwYZAJg1SlA'
APPID = 'wIp15JmLqa9HF213g5kQ05'
TIMESTAMP = int(round(time.time() * 1000))
ENDTIME = (datetime.datetime.now() + datetime.timedelta(hours=24)
           ).strftime("%Y-%m-%d %H:%M:%S")


def checkToken():  # 判断auth_token是否过期

    AUTH_TOKEN = ""

    auth_json = None

    with open('auth.json', 'r') as json_file:
        auth_json = json.load(json_file)

    expire_time = int(auth_json['expire_time'])

    if expire_time < TIMESTAMP:

        new_auth_json = getToken()

        AUTH_TOKEN = new_auth_json['auth_token']

        with open('auth.json', 'w') as json_file:

            json_file.write(json.dumps(new_auth_json))

    else:
        AUTH_TOKEN = auth_json['auth_token']

    return AUTH_TOKEN


def getToken():  # 更新token签名
    sign = APPKEY + str(TIMESTAMP) + MASTERSECRET
    sh = hashlib.sha256()
    sh.update(sign.encode("utf8"))

    payload = {
        "sign": sh.hexdigest(),
        "timestamp": str(TIMESTAMP),
        "appkey": APPKEY
    }

    headers = {'content-type': 'application/json'}
    url = "https://restapi.getui.com/v1/" + APPID + "/auth_sign"

    ret = requests.post(url, data=json.dumps(payload), headers=headers).json()

    return ret


def pushMessage(title, content, token):  # 推送消息

    auth_json = None

    headers = {
        'content-type': 'application/json',
        "authtoken": token
    }

    message = {
        "message": {
            "appkey": APPKEY,
            "is_offline": True,
            "msgtype": "transmission"
        },
        "transmission": {
            "transmission_type": False,
            "transmission_content": "{title:" + title + ",content:" + content + ",payload:''}",
            "duration_end": ENDTIME
        },
        "requestid": str(TIMESTAMP)
    }

    url = "https://restapi.getui.com/v1/" + APPID + "/push_app"

    return requests.post(url, data=json.dumps(message), headers=headers).json()

#------------------------------------------------------------------------


AUTH_TOKEN = checkToken()

if AUTH_TOKEN == "":
    print('token 更新失败')
else:
    ret = pushMessage(title="玖天监控", content=inputmsg, token=AUTH_TOKEN)

print(ret)
