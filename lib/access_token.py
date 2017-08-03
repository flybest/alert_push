import json
import time
from lib.util import Util


class AccessToken:

    def __init__(self, agentId):
        self.agentId = agentId

    def getAccessToken(self):
        auth_json = None
        try:
            with open('./cache/' + str(self.agentId) + '.json', 'r') as json_file:
                auth_json = json.load(json_file)
        except Exception as err:
            # print(err)
            return self.__requestAccessToken()

        if auth_json is None or (int(time.time()) - int(auth_json['request_time'])) >= int(auth_json['expires_in']):
            return self.__requestAccessToken()

        return auth_json['access_token']

    def __setAccessToken(self, tokenString):
        with open('./cache/' + str(self.agentId) + '.json', 'w') as json_file:
            json_file.write(json.dumps(tokenString))
        return

    def __requestAccessToken(self):
        util = Util()
        config = util.getConfigByAgentId(self.agentId)
        if config is None:
            print('No configuration for '+ str(self.agentId) +' was found!')
            return None

        requestTime = str(int(time.time()))
        try:
            res = util.httpsGet('https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + config['CorpId'] + '&corpsecret=' + config['Secret'])
            self.__setAccessToken({'expires_in': res['expires_in'], 'access_token': res['access_token'], 'request_time': requestTime})
            return res['access_token']
        except Exception as err:
            print(err)
            return None
