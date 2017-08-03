import time
import json
import datetime
from lib import *


class AppApi:

    def __init__(self, agentId=None):
        self.agentId = agentId
        if agentId is not None:
            self.accessToken = AccessToken(agentId)
        self.authToken = AuthToken()
        self.util = Util()

    def sendMsgToUser(self, msg):
        if self.agentId is not None:
            url = "https://qyapi.weixin.qq.com/cgi-bin/message/send"
            return self.util.httpsPost(self.__appendToken(url), msg)
        else:
            return "push only"

    def pushMessage(self, msg):
        token = self.authToken.getAuthToken()
        config = self.util.getPushConfig()

        try:
            headers = {
                "authtoken": token
            }

            message = {
                "message": {
                    "appkey": config['AppKey'],
                    "is_offline": True,
                    "msgtype": "transmission"
                },
                "transmission": {
                    "transmission_type": False,
                    "transmission_content": "{title:" + msg['title'] + ",content:" + msg['content'] + ",payload:''}",
                    "duration_end": (datetime.datetime.now() + datetime.timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
                },
                "requestid": str(int(round(time.time() * 1000)))
            }
        except Exception as err:
            print(err)
            return err

        url = "https://restapi.getui.com/v1/" + config['AppId'] + "/push_app"
        return self.util.httpsPost(url, params=message, header=headers)

    def __appendToken(self, url):
        token = str(self.accessToken.getAccessToken())
        if url.find("?") > -1:
            return url + "&access_token=" + token
        else:
            return url + "?access_token=" + token
