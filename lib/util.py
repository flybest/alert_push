import json
import requests

class Util:

    def __init__(self):
        return

    def __loadConfig(self):
        auth_json = None
        try:
            with open('./config.json', 'r') as json_file:
                auth_json = json.load(json_file)
        except Exception as err:
            print(err)
            return None
        return auth_json

    def getConfigByAgentId(self, agentId):
        config = self.__loadConfig()
        if config is None:
            return None
        for app in config['AppsConfig']:
            if app['AgentId'] == agentId:
                app['CorpId'] = config['CorpId']
                return app
        return None

    def getPushConfig(self):
        config = self.__loadConfig()
        if config is None:
            return None
        return config['Push']

    def httpsPost(self, url, params, header={}):
        headers = {'content-type': 'application/json'}
        headers.update(header)
        ret = requests.post(url, data=json.dumps(params), headers=headers).json()
        return ret

    def httpsGet(self, url, header={}):
        headers = {'content-type': 'application/json'}
        headers.update(header)
        ret = requests.get(url, headers=headers).json()
        return ret
