# from lib import Util
#
# util = Util()
# print(util.getConfigByAgentId(1000002))
# print(util.httpsGet('https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=ww3fc297c3ee304618&corpsecret=MNSW-Toyr07PP38Fttr1-5G0JsrKpsJkyInS_LaZed0'))

#
# import time
#
# # 打印当前时间戳(毫秒)
# t = time.time()
# print(t)
#
# from lib import AccseeToken
# at = AccseeToken(1000002)
# print(at.getAccessToken())

# from lib import AuthToken
# at = AuthToken()
# print(at.getAuthToken())


import sys
from app_api import AppApi


def sendTextMsgTest():
    msg = {
        'touser': '@all',
        'msgtype': 'text',
        'agentid': agentId,
        'text': {
            'content': msgContent
        }
    }

    api = AppApi(agentId)
    return api.sendMsgToUser(msg)


def sendCardsMsgTest():
    msg = {
        "touser": "@all",
        "msgtype": "textcard",
        "agentid": agentId,
        "textcard": {
            "title": msgTitle,
            "description": "<div class=\"highlight\">"+ msgContent +"</div>",
            "url": "http://47.93.246.230/alertlist/?type="+ ((agentId==1000004) and "%E9%80%9A%E7%9F%A5" or "%E5%BC%82%E5%B8%B8")
        }
    }
    # print(msg['textcard']['url'])
    api = AppApi(agentId)
    return api.sendMsgToUser(msg)


def pushMessageTest():
    msg = {
        "title": "玖天监控",
        "content": msgTitle
    }

    api = AppApi()
    return api.pushMessage(msg)

agentId = 1000002
msgTitle = ''
msgContent = ''
if len(sys.argv) >= 4:
    agentId = int(sys.argv[1])
    msgTitle = sys.argv[2]
    msgContent = sys.argv[3]

print(sendCardsMsgTest())
print(pushMessageTest())
