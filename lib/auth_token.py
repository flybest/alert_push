import json
import time
import hashlib
from lib.util import Util


class AuthToken:

    def __init__(self):
        return

    def getAuthToken(self):
        auth_json = None
        try:
            with open('./cache/push_auth.json', 'r') as json_file:
                auth_json = json.load(json_file)
        except Exception as err:
            # print(err)
            return self.__requestAuthToken()

        if auth_json is None or int(round(time.time() * 1000)) > int(auth_json['expire_time']):
            return self.__requestAuthToken()

        return auth_json['auth_token']

    def __setAuthToken(self, tokenString):
        with open('./cache/push_auth.json', 'w') as json_file:
            json_file.write(json.dumps(tokenString))
        return

    def __requestAuthToken(self):
        util = Util()
        config = util.getPushConfig()
        if config is None:
            return None

        requestTime = str(int(round(time.time() * 1000)))
        sign = config['AppKey'] + requestTime + config['MasterSecret']
        sh = hashlib.sha256()
        sh.update(sign.encode("utf8"))
        payload = {
            "sign": sh.hexdigest(),
            "timestamp": requestTime,
            "appkey": config['AppKey']
        }

        try:
            url = "https://restapi.getui.com/v1/" + config['AppId'] + "/auth_sign"
            ret = util.httpsPost(url, params=payload)
            if ret['result'] == 'ok':
                self.__setAuthToken(ret)
            return ret['auth_token']
        except Exception as err:
            print(err)
            return None
