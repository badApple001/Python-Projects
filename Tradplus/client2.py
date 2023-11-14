#备用服务端口


import requests 
import time
import implant

api = 'https://www.geek7.top:8091/callApi'
adsChannel = ['UnityAds']
region = '2' # 1: 中国  2: 其它地区


adsChannel.clear()
def log( msg ):
    print( msg )

def InitChannel():
    adsChannel.clear()
    with open('./bin/ads','r') as fp:
        for line in fp.readlines():
            adsChannel.append(line.replace('\n',''))


def Run( sdk_version = "10.2.0.1" ):
    InitChannel()
    data = {
        'token' : time.time(),
        'channel':'tradplus_sdk_depends',
        'code':829,
        'adchannels': adsChannel,
        'version':sdk_version,
        'region' : region
    }
    res = requests.get(api,data) 
    j = res.json()
    if 'data' not in j:
        log('erro: data not in depends')
        return
    appGradleCode = j['data']
    if None == appGradleCode:
        log('GetDependencies fail')
    else:
        srcpath = input('input proj:\n')
        realpath = srcpath.replace('\\','/')
        implant.Run(realpath,appGradleCode)

if __name__ == "__main__":
    print('run...')
    Run()